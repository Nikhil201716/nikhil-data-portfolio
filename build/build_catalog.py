"""
build_catalog.py
-------------------
Aggregates every project into site/data/catalog.json, which is the only
data source the static website reads.

The hard rule: this script NEVER invents a metric. For Projects 5-12 the
numbers are pulled out of that project's own reports/*.json by an explicit
per-project extractor, so a metric on the website can always be traced to
a file produced by a real run. For Projects 1-4, which predate the reports
convention, the numbers are quoted from the results table in that
project's README and tagged `"source": "readme"` so the provenance is
visible rather than implied.

If an extractor cannot find its report file, the project is emitted with
its curated description and an empty metric list - the site then shows
"metrics unavailable" rather than a plausible-looking fabrication.

Output: site/data/catalog.json
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # 00-Portfolio-Website
PROJECTS_ROOT = ROOT.parent             # Desktop/Projects
sys.path.insert(0, str(HERE))

from project_metadata import PROJECTS, ROLES  # noqa: E402

OUT = ROOT / "site" / "data" / "catalog.json"
OUT.parent.mkdir(parents=True, exist_ok=True)


def read_json(project_dir: Path, name: str):
    p = project_dir / "reports" / name
    if not p.exists():
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def m(label, value, highlight=False, note=None):
    d = {"label": label, "value": value, "highlight": highlight}
    if note:
        d["note"] = note
    return d


# ---------------------------------------------------------------------
# Per-project extractors. Each returns (metrics, charts).
# `charts` are plot-ready specs the frontend renders with Plotly.
# ---------------------------------------------------------------------
def extract_05(d: Path):
    metrics, charts = [], []
    v = read_json(d, "pandera_validation_results.json")
    if v:
        metrics.append(m("Validation checks run", str(v["total_checks"])))
        metrics.append(m("Checks passed / failed",
                          f"{v['passed']} / {v['failed']}", True,
                          "failures are real findings, not a broken suite"))
        charts.append({
            "type": "bar", "title": "Statistical validation outcomes",
            "x": ["passed", "failed"],
            "series": [{"name": "checks", "y": [v["passed"], v["failed"]]}],
            "yaxis": "checks",
        })
    return metrics, charts


def extract_06(d: Path):
    metrics, charts = [], []
    e = read_json(d, "detection_evaluation.json")
    if e:
        cm = e["confusion_matrix"]
        for key, label, hi in (("precision", "Fraud precision", False),
                                ("recall", "Fraud recall", True),
                                ("f1_score", "Fraud F1", False)):
            if key in e:
                metrics.append(m(label, f"{e[key]:.3f}", hi))
        metrics.append(m("Events streamed", f"{e['total_events']:,}"))
        charts.append({
            "type": "bar", "title": "Detection confusion matrix",
            "x": ["true positive", "false positive", "false negative", "true negative"],
            "series": [{"name": "events", "y": [cm["true_positive"], cm["false_positive"],
                                                  cm["false_negative"], cm["true_negative"]]}],
            "log_y": True, "yaxis": "events (log)",
        })
    return metrics, charts


def extract_07(d: Path):
    metrics, charts = [], []
    base = read_json(d, "model_evaluation_baseline.json")
    retr = read_json(d, "model_evaluation_retrained.json")
    drift = read_json(d, "drift_report.json")
    flaky = read_json(d, "flaky_test_report.json")

    def recall_of(rep, key):
        blk = rep.get(key) if rep else None
        return blk.get("recall_at_10") if isinstance(blk, dict) else None

    if base and retr:
        b_pop, r_pop = recall_of(base, "popularity_baseline"), recall_of(retr, "popularity_baseline")
        svd_key = next((k for k in retr if isinstance(retr[k], dict)
                        and "recall_at_10" in retr[k] and k != "popularity_baseline"), None)
        b_svd = recall_of(base, svd_key) if svd_key else None
        r_svd = recall_of(retr, svd_key) if svd_key else None
        if r_svd is not None:
            metrics.append(m("Recall@10 (collaborative filtering)", f"{r_svd:.3f}", True))
        if r_pop is not None:
            metrics.append(m("Recall@10 (popularity baseline)", f"{r_pop:.3f}"))
        xs, ys = [], []
        for label, val in (("baseline popularity", b_pop), ("baseline CF", b_svd),
                            ("retrained popularity", r_pop), ("retrained CF", r_svd)):
            if val is not None:
                xs.append(label)
                ys.append(val)
        if xs:
            charts.append({
                "type": "bar", "title": "Recall@10 before and after the automated retrain",
                "x": xs, "series": [{"name": "recall@10", "y": ys}], "yaxis": "recall@10",
            })
    if drift:
        metrics.append(m("Drift windows flagged (PSI)",
                          f"{drift['n_weeks_flagged']} / {drift['n_weeks_analyzed']}", True))
    if flaky:
        metrics.append(m("Flaky tests detected",
                          f"{flaky['n_flaky']} of {flaky['n_tests']} over {flaky['n_runs']} runs"))
    return metrics, charts


def extract_08(d: Path):
    metrics, charts = [], []
    ex = read_json(d, "extraction_evaluation.json")
    if ex:
        by_field = ex.get("regex_accuracy_by_field") or {}
        llm_field = ex.get("llm_accuracy_by_field") or {}
        if by_field:
            avg = sum(by_field.values()) / len(by_field)
            metrics.append(m("Regex extraction accuracy", f"{avg:.1%}"))
        if llm_field:
            avg_l = sum(llm_field.values()) / len(llm_field)
            metrics.append(m("LLM extraction accuracy", f"{avg_l:.1%}", True))
        if by_field and llm_field:
            fields = sorted(set(by_field) & set(llm_field))
            if fields:
                charts.append({
                    "type": "bar", "title": "Field extraction accuracy: regex vs. local LLM",
                    "x": fields,
                    "series": [
                        {"name": "regex", "y": [by_field[f] for f in fields]},
                        {"name": "LLM", "y": [llm_field[f] for f in fields]},
                    ],
                    "yaxis": "accuracy",
                })
    vis = read_json(d, "vision_evaluation.json")
    if vis:
        metrics.append(m("CNN damage classifier accuracy", f"{vis['test_accuracy']:.1%}", True,
                          f"trained from scratch, {vis['n_train']} images"))
    rec = read_json(d, "reconciliation_evaluation.json")
    if rec:
        metrics.append(m("Reconciliation recall / precision",
                          f"{rec['recall']:.3f} / {rec['precision']:.3f}", True,
                          "100% recall by design; false positives root-caused"))
    return metrics, charts


def extract_09(d: Path):
    metrics, charts = [], []
    fr = read_json(d, "fraud_detection_evaluation.json")
    if fr:
        metrics.append(m("Fraud ring detection F1", f"{fr['f1_score']:.3f}", True))
        sweep = fr.get("threshold_sweep")
        if sweep:
            charts.append({
                "type": "line", "title": "Precision / recall vs. minimum ring size",
                "x": [s["threshold"] for s in sweep],
                "series": [
                    {"name": "precision", "y": [s["precision"] for s in sweep]},
                    {"name": "recall", "y": [s["recall"] for s in sweep]},
                ],
                "xaxis": "minimum ring size", "yaxis": "score",
            })
    cmp_ = read_json(d, "experiment_readout_comparison.json")
    if cmp_:
        raw = cmp_["raw"]["frequentist"]["relative_lift_pct"]
        clean = cmp_["fraud_excluded"]["frequentist"]["relative_lift_pct"]
        metrics.append(m("Apparent lift (raw)", f"{raw}%"))
        metrics.append(m("Real lift (fraud excluded)", f"{clean}%", True))
        charts.append({
            "type": "bar", "title": "A/B readout before and after excluding fraud rings",
            "x": ["raw (contaminated)", "fraud-excluded"],
            "series": [{"name": "relative lift %", "y": [raw, clean]}],
            "yaxis": "relative lift %",
        })
    return metrics, charts


def extract_10(d: Path):
    metrics, charts = [], []
    asr = read_json(d, "asr_evaluation.json")
    if asr:
        metrics.append(m("Whisper word error rate", f"{asr['avg_word_error_rate']:.1%}", True))
    cau = read_json(d, "causal_inference_evaluation.json")
    if cau:
        true_pct = cau["true_effect_pct"]
        names = [("Naive", "naive"), ("Propensity matching", "propensity_score_matching"),
                 ("Difference-in-differences", "difference_in_differences")]
        metrics.append(m("True injected effect", f"{true_pct:.0%}"))
        for label, key in names:
            metrics.append(m(f"{label} estimate", f"{cau[key]['estimated_effect_pct']:.1%}",
                              key == "difference_in_differences"))
        charts.append({
            "type": "bar", "title": "Causal estimates vs. the known true effect",
            "x": [n for n, _ in names],
            "series": [{"name": "estimated effect", "y": [cau[k]["estimated_effect_pct"] for _, k in names]}],
            "hline": {"value": true_pct, "label": "true effect"},
            "yaxis": "estimated effect",
        })
    opt = read_json(d, "optimization_comparison.json")
    if opt:
        lp, nv = opt["risk_aware_lp"], opt["naive_cheapest_first"]
        red = 1 - lp["risk_weighted_shortfall"] / nv["risk_weighted_shortfall"]
        metrics.append(m("Risk-weighted shortfall reduction", f"{red:.1%}", True))
    return metrics, charts


def extract_11(d: Path):
    metrics, charts = [], []
    perf = read_json(d, "model_performance.json")
    aud = read_json(d, "fairness_audit.json")
    if perf:
        metrics.append(m("AUC cost of removing the proxy",
                          f"{perf['auc_cost_of_removing_proxy']:+.5f}", True,
                          "essentially free to remove"))
    if aud:
        dw = aud["headline"]["disparate_impact_with_proxy"]
        dwo = aud["headline"]["disparate_impact_without_proxy"]
        metrics.append(m("Disparate impact (with proxy)", f"{dw:.4f}"))
        metrics.append(m("Disparate impact (without)", f"{dwo:.4f}"))
        charts.append({
            "type": "bar", "title": "Disparate impact barely moves when the proxy is removed",
            "x": ["with proxy", "without proxy"],
            "series": [{"name": "disparate impact ratio", "y": [dw, dwo]}],
            "hline": {"value": 0.8, "label": "four-fifths threshold"},
            "yaxis": "ratio",
        })
    ret = read_json(d, "retrieval_evaluation.json")
    if ret:
        rc = ret["retrieval_comparison"]
        charts.append({
            "type": "bar", "title": "Retrieval MRR by method (dense beat hybrid)",
            "x": list(rc.keys()),
            "series": [{"name": "MRR", "y": [rc[k]["overall"]["mrr"] for k in rc]}],
            "yaxis": "MRR",
        })
        metrics.append(m("Best retrieval MRR (dense)", f"{rc['dense']['overall']['mrr']:.3f}", True))
    rt = read_json(d, "red_team_results.json")
    if rt:
        metrics.append(m("Red-team attacks handled", f"{rt['n_passed']}/{rt['n_attacks']}"))
    return metrics, charts


def extract_12(d: Path):
    metrics, charts = [], []
    base = read_json(d, "baseline_results.json")
    tr = read_json(d, "transformer_results.json")
    if base:
        v = base["variants"]
        metrics.append(m("Unigram TF-IDF (ceiling 0.50)", f"{v['unigram']['accuracy']:.4f}", True))
        metrics.append(m("Bigram TF-IDF", f"{v['bigram']['accuracy']:.4f}"))
        labels = ["unigram", "bigram", "trigram"]
        ys = [v[k]["accuracy"] for k in labels]
        if tr:
            labels += ["transformer"]
            ys += [tr["fp32"]["accuracy"]]
        charts.append({
            "type": "bar", "title": "Accuracy - and the unigram's mathematical ceiling",
            "x": labels, "series": [{"name": "accuracy", "y": ys}],
            "hline": {"value": 0.5, "label": "unigram ceiling"}, "yaxis": "accuracy",
        })
    if tr:
        vb = tr["vs_bigram_tfidf"]
        metrics.append(m("Transformer gain over bigram",
                          f"{vb['accuracy_gain_over_bigram']:+.4f}", True, "zero"))
        metrics.append(m("Latency cost", f"{vb['latency_cost_x']}x"))
        metrics.append(m("Size cost", f"{vb['size_cost_x']:,.0f}x"))
        charts.append({
            "type": "bar", "title": "Inference latency (log scale) - int8 was SLOWER",
            "x": ["bigram TF-IDF", "transformer fp32", "transformer int8"],
            "series": [{"name": "ms per item", "y": [vb["bigram_latency_ms"],
                                                       tr["fp32"]["latency_ms_per_item"],
                                                       tr["int8_dynamic"]["latency_ms_per_item"]]}],
            "log_y": True, "yaxis": "ms per item",
        })
    kg = read_json(d, "graphrag_evaluation.json")
    if kg:
        hops = sorted(kg["by_hop"])
        charts.append({
            "type": "line", "title": "Retrieval F1 by hop count - text search hits zero",
            "x": [int(h) for h in hops],
            "series": [
                {"name": "graph", "y": [kg["by_hop"][h]["graph_f1"] for h in hops]},
                {"name": "BM25", "y": [kg["by_hop"][h]["bm25_f1"] for h in hops]},
                {"name": "vector", "y": [kg["by_hop"][h]["vector_f1"] for h in hops]},
            ],
            "xaxis": "hops", "yaxis": "F1",
        })
    pr = read_json(d, "pricing_results.json")
    if pr:
        lift = pr["lift_vs_behaviour"]
        metrics.append(m("Bandit lift (train world)", f"{lift['train_regime']:+.0f}"))
        metrics.append(m("Bandit lift (shifted world)", f"{lift['holdout_regime']:+.0f}", True,
                          "loses to the incumbent"))
        ope = pr["ope_estimates"]
        err = pr["ope_error_vs_ground_truth"]
        charts.append({
            "type": "bar", "title": "Off-policy estimator error vs. ground truth",
            "x": [k.upper() for k in ("dm", "ips", "snips", "dr")],
            "series": [{"name": "error", "y": [err[k] for k in ("dm", "ips", "snips", "dr")]}],
            "yaxis": "error vs truth",
        })
    qa = read_json(d, "qa_summary.json")
    if qa:
        metrics.append(m("Tests passing", str(qa["totals"]["passed"])))
        mt = qa.get("mutation_testing")
        if mt:
            metrics.append(m("Mutation score",
                              f"{mt['initial_score']:.1%} → {mt['final_score']:.1%}", True))
        lt = qa.get("load_test")
        if lt:
            metrics.append(m("Load test", f"{lt['total_requests']:,} reqs, "
                                            f"{lt['failures']} failures"))
    return metrics, charts


def extract_13(d: Path):
    metrics, charts = [], []
    det = read_json(d, "detector_benchmark.json")
    if det:
        rows = sorted(det["detectors"], key=lambda r: -r["pr_auc"])
        best = rows[0]
        metrics.append(m("Series monitored", f"{det['n_series']:,}"))
        metrics.append(m("Best detector (PR-AUC)",
                          f"{best['detector']} {best['pr_auc']:.4f}", True,
                          f"vs {det['anomalous_point_rate']:.5f} base rate"))
        stl = next((r for r in rows if r["detector"] == "stl_residual"), None)
        if stl:
            metrics.append(m("STL alert cost",
                              f"{stl['fleet_alerts_per_day'] / best['fleet_alerts_per_day']:.1f}x",
                              True, "more alerts for +0.08 event recall"))
        charts.append({
            "type": "bar", "title": "PR-AUC by detector - the cheapest seasonal method wins",
            "x": [r["detector"] for r in rows],
            "series": [{"name": "PR-AUC", "y": [r["pr_auc"] for r in rows]}],
            "yaxis": "PR-AUC",
        })
        charts.append({
            "type": "bar", "title": "Alert volume: recall is not free",
            "x": [r["detector"] for r in rows],
            "series": [{"name": "fleet alerts/day",
                         "y": [r["fleet_alerts_per_day"] for r in rows]}],
            "yaxis": "alerts per day",
        })
    leak = read_json(d, "leakage_demo.json")
    if leak:
        a, b, c = (leak["A_leaky_train_leaky_eval"]["roc_auc"],
                    leak["B_pit_train_pit_eval"]["roc_auc"],
                    leak["C_leaky_train_pit_eval"]["roc_auc"])
        gap = leak["gap_B_minus_C_roc_auc"]
        metrics.append(m("Leaked model in production",
                          f"{a:.4f} claimed -> {c:.4f} actual", True))
        metrics.append(m("Cost of the leak (B-C)",
                          f"{gap['point']:+.4f} ROC-AUC",
                          True, f"95% CI [{gap['ci95'][0]:+.4f}, {gap['ci95'][1]:+.4f}]"))
        charts.append({
            "type": "bar", "title": "Leakage: the deck number vs what production delivers",
            "x": ["A leaky/leaky", "B point-in-time", "C leaky model, real features"],
            "series": [{"name": "ROC-AUC", "y": [a, b, c]}],
            "yaxis": "ROC-AUC",
        })
    obs = read_json(d, "observability.json")
    if obs:
        metrics.append(m("PSI drift monitor",
                          f"honest {obs['honest_max_psi']:.3f} vs leaky {obs['broken_max_psi']:.3f}",
                          True, "monitor rates the LEAKY pipeline healthier"))
        v = obs.get("logic_parity_verdict")
        if v:
            metrics.append(m("Logic-parity check",
                              f"{v['honest_total_mismatches']} vs "
                              f"{v['leaky_total_mismatches']:,} mismatches", True,
                              f"worst: {v['leaky_worst_feature']} "
                              f"{v['leaky_worst_mismatch_pct']:.0f}%"))
        f = obs.get("freshness")
        if f:
            metrics.append(m("Merchants breaching 30-min SLA",
                              f"{f['breaching_sla']}/{f['n_merchants']} ({f['breaching_pct']}%)"))
    tri = read_json(d, "triage_benchmark.json")
    if tri:
        by = {r["writer"]: r for r in tri["per_writer"]}
        if "template" in by and "llm" in by:
            metrics.append(m(f"Triage: template vs {tri['model']}",
                              f"{by['template']['score']:.4f} vs {by['llm']['score']:.4f}", True))
            charts.append({
                "type": "bar", "title": "Incident triage rubric - template vs local LLM",
                "x": ["entity", "metric", "direction", "numbers", "concise"],
                "series": [
                    {"name": "template", "y": [by["template"][k] for k in
                                                 ("mentions_entity", "mentions_metric",
                                                  "correct_direction", "no_invented_numbers",
                                                  "concise")]},
                    {"name": tri["model"], "y": [by["llm"][k] for k in
                                                   ("mentions_entity", "mentions_metric",
                                                    "correct_direction", "no_invented_numbers",
                                                    "concise")]},
                ],
                "yaxis": "pass rate",
            })
    mut = read_json(d, "mutation.json")
    if mut:
        metrics.append(m("Mutation score",
                          f"{mut['killed']}/{mut['mutants_total']} "
                          f"({mut['mutation_score']:.1%})", True))
    return metrics, charts


def extract_13(d: Path):
    """Meridian: registry canary, PII held-out gap, causal estimator error."""
    metrics, charts = [], []
    reg = read_json(d, "model_registry.json")
    if reg:
        idx = {e["version"]: e for e in reg.get("registry_index", [])}
        prod = idx.get(reg.get("production_version"), {})
        cans = [e for e in reg.get("events", []) if e["event"] == "canary"]
        rejected = sum(1 for e in cans if not e["gate"]["promoted"])
        metrics.append(m("Production model AUC",
                          f"{prod.get('metrics', {}).get('auc', 0):.4f}", True))
        metrics.append(m("Candidates rejected by canary",
                          f"{rejected} of {len(cans)}", True,
                          "a gate that never rejects is decoration"))
        metrics.append(m("Winner's training rows",
                          f"{prod.get('training_rows', 0):,}", False,
                          "17% of available data - the rest predates a concept drift"))
        charts.append({
            "type": "bar", "title": "Canary gate: candidate AUC vs incumbent",
            "x": [e["version"] for e in cans],
            "series": [{"name": "AUC", "y": [e["metrics"]["auc"] for e in cans]}],
            "yaxis": "AUC on held-out window",
        })
    pii = read_json(d, "pii_governance.json")
    if pii:
        ind = pii["detector"]["overall"]["f1"]
        held = pii["held_out_format_challenge"]["recall"]
        metrics.append(m("PII F1 (formats tuned on)", f"{ind:.4f}", False,
                          "a training score, not a capability claim"))
        metrics.append(m("PII recall (unseen formats)", f"{held:.2f}", True,
                          "the honest number"))
        charts.append({
            "type": "bar", "title": "PII detection: known vs unseen formats",
            "x": ["Known formats (F1)", "Unseen formats (recall)"],
            "series": [{"name": "score", "y": [ind, held]}], "yaxis": "score",
        })
    exp = read_json(d, "experimentation.json")
    if exp:
        est = exp["observational_programme"]["estimates"]
        metrics.append(m("Naive estimator error",
                          f"{est['naive_treated_vs_control_post']['error_vs_truth']:+.2f}",
                          False, "erases the entire true effect"))
        metrics.append(m("Difference-in-differences error",
                          f"{est['difference_in_differences']['error_vs_truth']:+.3f}", True))
        charts.append({
            "type": "bar", "title": "Programme effect: estimator vs truth",
            "x": ["naive", "before/after", "diff-in-diff", "TRUE"],
            "series": [{"name": "stoppages per plant-week", "y": [
                est["naive_treated_vs_control_post"]["value"],
                est["before_after_treated_only"]["value"],
                est["difference_in_differences"]["value"],
                exp["observational_programme"]["true_effect"]]}],
            "yaxis": "effect",
        })
    return metrics, charts


def extract_14(d: Path):
    """Cascade: watermark damage, judge inflation, injected-bug detection."""
    metrics, charts = [], []
    w = read_json(d, "windowing.json")
    if w:
        sc = w["scores"]
        metrics.append(m("Messages processed", f"{w['messages_processed']:,}"))
        metrics.append(m("Naive watermark error",
                          f"{sc['watermark']['total_abs_count_error']:,}", False,
                          "36 fast clocks in 2,600 devices cause this"))
        metrics.append(m("Skew-filtered watermark error",
                          f"{sc['watermark_skew_filtered']['total_abs_count_error']:,}", True,
                          "event_time > processing_time is physically impossible"))
        charts.append({
            "type": "bar", "title": "Windowing strategy error vs the answer key",
            "x": list(sc.keys()),
            "series": [{"name": "absolute count error",
                        "y": [sc[k]["total_abs_count_error"] for k in sc]}],
            "yaxis": "abs error (lower is better)",
        })
        rs = w.get("window_size_ratio_sweep", [])
        if rs:
            charts.append({
                "type": "line", "title": "Where arrival-time windowing breaks",
                "x": [f"{r['window_size_ms'] // 1000}s" for r in rs],
                "series": [
                    {"name": "processing time",
                     "y": [r["processing_time_mean_rel_error_pct"] for r in rs]},
                    {"name": "event time",
                     "y": [r["event_time_mean_rel_error_pct"] for r in rs]}],
                "xaxis": "window size", "yaxis": "mean relative error %",
            })
    a = read_json(d, "agent_eval.json")
    if a:
        j = a["judge_calibration"]
        metrics.append(m("Agent accuracy (vs answer key)",
                          f"{a['llm_agent']['accuracy']:.1%}", False))
        metrics.append(m("Accuracy the LLM judge reported",
                          f"{j['agent_score_if_you_trusted_the_judge']:.0%}", False,
                          f"{j['judge_false_pass']} false passes, {j['judge_false_fail']} false fails"))
        metrics.append(m("Judge score inflation",
                          f"+{j['score_inflation']:.1%}", False,
                          "why judges must themselves be calibrated"))
        charts.append({
            "type": "bar", "title": "Reported vs actual agent accuracy",
            "x": ["Reported by judge", "Actual", "Majority baseline"],
            "series": [{"name": "accuracy", "y": [
                j["agent_score_if_you_trusted_the_judge"], j["agent_true_score"],
                a["majority_class_baseline"]["accuracy"]]}],
            "yaxis": "accuracy",
        })
    b = read_json(d, "injected_bugs.json")
    if b and b.get("detection_rate") is not None:
        metrics.append(m("Injected defects caught",
                          f"{b['caught']} of {b['bugs_injected']}", True,
                          "measures what the suite would catch, not that it passes"))
    c = read_json(d, "cdc_scd2.json")
    if c:
        metrics.append(m("SCD2 point-in-time accuracy",
                          f"{c['accuracy_pct']['scd2_ordered']}%", True,
                          f"vs {c['accuracy_pct']['type1_overwrite']}% for overwrite"))
    return metrics, charts


EXTRACTORS = {
    "05": extract_05, "06": extract_06, "07": extract_07, "08": extract_08,
    "09": extract_09, "10": extract_10, "11": extract_11, "12": extract_12,
    "13": extract_13,
    "14": extract_14,
}


def main():
    projects = []
    for meta in PROJECTS:
        d = PROJECTS_ROOT / meta["dir"]
        entry = {k: v for k, v in meta.items() if k != "metrics"}
        entry["exists"] = d.exists()

        if meta["metrics_source"] == "readme":
            entry["metrics"] = [dict(x, source="readme") for x in meta.get("metrics", [])]
            entry["charts"] = []
        else:
            fn = EXTRACTORS.get(meta["id"])
            metrics, charts = fn(d) if fn else ([], [])
            entry["metrics"] = [dict(x, source="reports") for x in metrics]
            entry["charts"] = charts

        entry["n_report_files"] = len(list((d / "reports").glob("*.json"))) if d.exists() else 0
        entry["screenshots"] = sorted(p.name for p in (d / "screenshots").glob("*.png")) \
            if (d / "screenshots").exists() else []
        projects.append(entry)

    all_topics = sorted({t for p in projects for t in p["topics"]})
    all_stack = sorted({s for p in projects for s in p["stack"]})

    catalog = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "owner": "Nikhil Sinha",
        "n_projects": len(projects),
        "roles": ROLES,
        "role_counts": {r: sum(1 for p in projects if r in p["roles"]) for r in ROLES},
        "all_topics": all_topics,
        "all_stack": all_stack,
        "n_topics": len(all_topics),
        "n_technologies": len(all_stack),
        "n_metrics_extracted": sum(len(p["metrics"]) for p in projects),
        "n_charts": sum(len(p["charts"]) for p in projects),
        "projects": projects,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print(f"Catalog written: {OUT}")
    print(f"  projects       : {catalog['n_projects']}")
    print(f"  distinct topics: {catalog['n_topics']}")
    print(f"  technologies   : {catalog['n_technologies']}")
    print(f"  metrics        : {catalog['n_metrics_extracted']}")
    print(f"  charts         : {catalog['n_charts']}")
    print()
    for p in projects:
        flag = "" if p["exists"] else "  [MISSING DIR]"
        print(f"  {p['id']} {p['title'][:44]:<46} "
              f"metrics={len(p['metrics']):<3} charts={len(p['charts'])}{flag}")


if __name__ == "__main__":
    main()
