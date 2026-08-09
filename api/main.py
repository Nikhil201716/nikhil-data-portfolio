"""
main.py
----------
Optional backend for the portfolio site.

The site is designed to work WITHOUT this. Everything a visitor needs is in
site/data/catalog.json, so the static deploy on GitHub Pages is complete on
its own. This server exists to add the thing a static file cannot do: run
the actual models the projects trained, live, against input a visitor
types.

It also serves the static site itself, so `python api/main.py` gives you
the full experience on one port.

Live endpoints reuse Project 12's real artifacts rather than reimplementing
anything:
    /api/live/classify        the bigram ticket router (the model P12
                              measured as the one worth shipping)
    /api/live/price           the pricing guardrails, mutation-tested to
                              81.5%
    /api/live/impact/{id}     graph traversal over the supply-chain KG

Each is loaded lazily and degrades to a clear error if that project's
artifacts are absent, rather than failing at import time and taking the
whole site down with it.

Run:
    python api/main.py            # http://127.0.0.1:8200
"""

import json
import pickle
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                       # 00-Portfolio-Website
PROJECTS = ROOT.parent                   # Desktop/Projects
SITE = ROOT / "site"

P12 = PROJECTS / "12-Retail-Intelligence-Platform"

app = FastAPI(title="Portfolio API", version="1.0.0")

# The static site may be served from a different origin (e.g. `python -m
# http.server` on 8300 during development), so the browser needs CORS to
# reach this API. Local-only tooling, so the origin list is permissive.
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

_cache = {}


def load_catalog():
    if "catalog" not in _cache:
        with open(SITE / "data" / "catalog.json", encoding="utf-8") as f:
            _cache["catalog"] = json.load(f)
    return _cache["catalog"]


def load_classifier():
    if "clf" not in _cache:
        p = P12 / "nlp" / "artifacts" / "tfidf_bigram.pkl"
        if not p.exists():
            raise HTTPException(503, "Project 12 classifier artifact not found — "
                                      "run nlp/baselines.py in that project first")
        with open(p, "rb") as f:
            _cache["clf"] = pickle.load(f)
    return _cache["clf"]


def load_graph():
    if "graph" not in _cache:
        p = P12 / "database" / "knowledge_graph.gpickle"
        if not p.exists():
            raise HTTPException(503, "Project 12 knowledge graph not found — "
                                      "run knowledge_graph/build_graph.py first")
        with open(p, "rb") as f:
            _cache["graph"] = pickle.load(f)
    return _cache["graph"]


def pricing_module():
    if "pricing" not in _cache:
        if str(P12) not in sys.path:
            sys.path.insert(0, str(P12))
        try:
            from pricing.pricing_rules import PricingError, decide_price
        except Exception as e:
            raise HTTPException(503, f"Project 12 pricing rules unavailable: {e}")
        _cache["pricing"] = (decide_price, PricingError)
    return _cache["pricing"]


# ------------------------------------------------------------ schemas
class ClassifyIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)

    @field_validator("text")
    @classmethod
    def not_blank(cls, v):
        if not v.strip():
            raise ValueError("text must not be blank")
        return v


class PriceIn(BaseModel):
    product_id: str = "PRD001"
    unit_cost: float = Field(gt=0)
    proposed_multiplier: float
    discount_pct: float = Field(default=0.0, ge=0, le=100)


# ---------------------------------------------------------- endpoints
@app.get("/api/health")
def health():
    cat = load_catalog()
    return {"status": "ok", "projects": cat["n_projects"],
            "metrics": cat["n_metrics_extracted"],
            "live_endpoints": ["/api/live/classify", "/api/live/price", "/api/live/impact/{id}"]}


@app.get("/api/catalog")
def catalog():
    return load_catalog()


@app.get("/api/projects/{pid}")
def project(pid: str):
    cat = load_catalog()
    p = next((x for x in cat["projects"] if x["id"] == pid), None)
    if not p:
        raise HTTPException(404, f"unknown project {pid}")
    return p


@app.post("/api/live/classify")
def live_classify(body: ClassifyIn):
    b = load_classifier()
    pred = str(b["classifier"].predict(b["vectorizer"].transform([body.text]))[0])
    return {"text": body.text, "predicted_category": pred,
            "model": "TF-IDF bigram + logistic regression (Project 12)",
            "note": "chosen over a fine-tuned transformer that scored identically "
                    "while being 36.7x slower and 7,580x larger"}


@app.post("/api/live/price")
def live_price(body: PriceIn):
    decide_price, PricingError = pricing_module()
    try:
        d = decide_price(body.product_id, body.unit_cost, body.proposed_multiplier,
                          body.discount_pct)
    except PricingError as e:
        raise HTTPException(422, str(e))
    return {"product_id": d.product_id, "unit_cost": d.unit_cost, "multiplier": d.multiplier,
            "price": round(d.price, 2), "margin": round(d.margin, 2),
            "clamped": d.clamped, "reason": d.reason,
            "note": "guardrails mutation-tested to 81.5% (Project 12)"}


@app.get("/api/live/impact/{incident_id}")
def live_impact(incident_id: str):
    G = load_graph()
    if incident_id not in G or G.nodes[incident_id].get("kind") != "Incident":
        raise HTTPException(404, f"unknown incident {incident_id}")
    comps = sorted({v for _, v, d in G.out_edges(incident_id, data=True) if d["rel"] == "AFFECTS"})
    prods = sorted({u for c in comps for u, _, d in G.in_edges(c, data=True)
                    if d["rel"] == "CONTAINS"})
    sups = sorted({v for c in comps for _, v, d in G.out_edges(c, data=True)
                   if d["rel"] == "SUPPLIED_BY"})
    return {"incident_id": incident_id, "components": comps, "suppliers": sups,
            "affected_products": prods, "n_affected": len(prods),
            "note": "derived by graph traversal; no single document states this "
                    "(text retrieval scored 0.000 F1 on these questions)"}


# Mount the static site last so /api/* wins.
app.mount("/", StaticFiles(directory=str(SITE), html=True), name="site")


if __name__ == "__main__":
    import uvicorn
    print("Portfolio site  ->  http://127.0.0.1:8200")
    print("API health      ->  http://127.0.0.1:8200/api/health")
    uvicorn.run(app, host="127.0.0.1", port=8200, log_level="warning")
