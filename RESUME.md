# Nikhil Sinha

nikhil.sinha16022003@gmail.com · github.com/Nikhil201716 ·
**Portfolio: https://nikhil201716.github.io/nikhil-data-portfolio/**

Data and AI engineer. I build systems that measure whether they actually
work — every project below scores itself against an injected ground truth,
and several of them report that the original hypothesis was wrong.

---

## Selected projects

All 14 are public on GitHub with runnable pipelines, test suites and
reports. Every number below comes from a JSON report the code produced.

### Cascade — Real-Time Intelligence Platform
`14-Cascade-Realtime-Intelligence-Platform` · Python, Redis Streams,
SQLite, FastAPI, Playwright, pytest, Hypothesis, Ollama

- Built an event-time stream processor (watermarks, allowed lateness,
  session/tumbling windows) over 40,877 messages carrying deliberate
  out-of-order delivery, duplicates and clock skew, scored against a
  separately generated answer key.
- **Found that 36 devices in 2,600 with fast clocks push a standard
  `max(event_time)` watermark 200s ahead of real time, causing it to
  discard 39,103 of 40,877 messages.** Fixed with a per-event physical
  check (`event_time ≤ processing_time`) requiring no tuning: error fell
  38,572 → 1,155.
- Implemented exactly-once as a sink property over at-least-once
  transport; swept dedup window against a 54-minute crash-replay lag to
  size it against the worst failure mode, not the typical one.
- **Calibrated an LLM-as-judge against ground truth and found it approved
  28 of 28 wrong answers — reporting 100% accuracy for an agent that was
  right 22.2% of the time.**
- Built injected-bug scoring that took the suite from 6/10 to 10/10
  detection; every survivor was a flaw in a test, not an unlucky mutation.
  Playwright E2E found a routing bug no API test could see.

### Meridian Operations Cloud
`13-Meridian-Operations-Cloud` · DuckDB, FastAPI, scikit-learn, pytest

- Shipped a 7-workspace operations **product** over one star-schema
  warehouse — asset health, commercial, service, risk, data platform,
  governance/MLOps — so two screens can never disagree about a number.
- Model registry with a canary gate that rejects: 2 of 3 candidates
  refused. **The promoted model trains on 17% of available rows** —
  discarding the pre-drift majority raised AUC 0.8313 → 0.8866 and doubled
  average precision.
- Fault injection proved the data-quality gates fire (3/3 caught after
  fixing a monitor that got quieter as breaks got larger).
- Privacy work measured rather than asserted: span-level PII scoring,
  k-anonymity, and a linkage attack that re-identified a subject **after**
  every direct identifier was removed.
- Difference-in-differences recovered a programme effect (−2.08 vs true
  −2.10) that naive comparison erased entirely (+0.03).

### Fair Lending Intelligence Platform
`11-Fair-Lending-Intelligence-Platform` · PySpark, SHAP, H3, scikit-learn

- 400k applications with an injected proxy variable of known **zero**
  causal effect; audited disparate impact against the four-fifths rule.
- Reported a refuted hypothesis: removing the proxy moved disparate impact
  0.8895 → 0.8870 and cost 0.0004 AUC — the proxy was not driving the gap
  once genuine financial signal was present.
- Benchmarked broadcast joins honestly after finding `/mnt/c` I/O variance
  exceeded the effect size and inverted the conclusion.

### Retail Intelligence Platform
`12-Retail-Intelligence-Platform` · Transformers, GraphRAG, pytest, Locust

- Fine-tuned a transformer against a TF-IDF baseline and found a **bigram
  bag-of-words matched MiniLM at 1/36th the latency and 1/7580th the
  size**; int8 quantisation made inference 3.7× *slower*.
- Off-policy evaluation (DM/IPS/SNIPS/DR) of a pricing policy against a
  known true value.
- Full QA/SDET layer: property, metamorphic, contract, mutation (65% →
  82%) and load testing — 6,474 requests, 0 failures.

### Earlier work (Projects 1–10)
SQL/Excel/Streamlit analytics · RFM & churn · demand forecasting with
inventory policy · **Airflow ETL** with quality gates proven by deliberate
failure · **dbt + DuckDB** warehouse with Pandera contracts and a local-LLM
RAG copilot · **Redis Streams** fraud detection over a live producer ·
recommenders, drift monitoring and a multi-agent ops loop · **document AI**
(OCR + LLM extraction + damage classification) · graph fraud rings, A/B
testing statistics and guardrailed NL-to-SQL · speech AI, supply-chain
optimisation, causal inference and MLOps.

---

## Skills

**Data engineering** — Airflow, dbt, DuckDB, PySpark, Redis Streams, CDC &
slowly changing dimensions, event-time processing, watermarks,
exactly-once semantics, star schemas, data contracts, lineage

**ML / AI** — scikit-learn, transformers, feature stores &
point-in-time correctness, concept drift, model registries & canary
deployment, off-policy evaluation, causal inference (DiD, PSM), SHAP,
fairness auditing, RAG, agent evaluation & LLM-judge calibration

**QA / SDET** — pytest, Hypothesis (property-based), metamorphic and
contract testing, mutation & injected-bug scoring, flaky-test detection,
Playwright E2E, Locust load testing

**Other** — Python, SQL, FastAPI, Streamlit, Plotly, Docker basics, Git,
WSL/Linux

---

## How I work

Three habits show up in every repository:

1. **Ground truth is injected, then scored against.** "It looks right" is
   not a result. Where a metric can be gamed, there is a control arm and a
   documented baseline to beat.
2. **A suspiciously good number is treated as a bug report.** Several
   projects contain a fix and a re-measurement because a first result was
   too clean — a 100% PII score that turned out to be a training score, a
   guardrail that passed a fabrication because it only checked digits.
3. **Refuted hypotheses are reported as results.** Reproducibility is
   verified by checksum in a fresh process, not by trusting a random seed —
   after two projects shipped fixed seeds that still weren't deterministic.
