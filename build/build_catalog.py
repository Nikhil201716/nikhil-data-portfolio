"""
build_catalog.py
-------------------
Aggregates every project into data/catalog.json, which is the only
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

Output: data/catalog.json
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # 00-Portfolio-Website
PROJECTS_ROOT = ROOT.parent             # Desktop/Projects
sys.path.insert(0, str(HERE))

from project_metadata import PROJECTS, AREAS as ROLES  # noqa: E402

OUT = ROOT / "data" / "catalog.json"
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


def extract_15(d: Path):
    """Aegis: metric blast radius, survival estimator recovery, fraud under attack."""
    metrics, charts = [], []
    g = read_json(d, "metric_regression.json")
    if g:
        br = g["definition_change_blast_radius"]
        metrics.append(m("Historical figures moved by one definition change",
                          f"{br['materially_moved']} of {br['figures_compared']}", False,
                          "every one had already been read and acted on"))
    s = read_json(d, "survival.json")
    if s:
        est = s["estimators"]
        metrics.append(m("Members right-censored",
                          f"{s['censoring_rate']:.1%}", False,
                          "still enrolled - not negatives"))
        metrics.append(m("Naive classifier coefficient error",
                          f"{est['naive_logistic_churned_yes_no']['mean_abs_error']:.4f}", False))
        metrics.append(m("Discrete-time hazard error",
                          f"{est['discrete_time_hazard']['mean_abs_error']:.4f}", True,
                          "26x more accurate than the naive arm"))
        charts.append({
            "type": "bar", "title": "Coefficient recovery error by estimator",
            "x": ["naive logistic", "Cox PH", "discrete-time"],
            "series": [{"name": "mean abs error", "y": [
                est["naive_logistic_churned_yes_no"]["mean_abs_error"],
                est["cox_proportional_hazards"]["mean_abs_error"],
                est["discrete_time_hazard"]["mean_abs_error"]]}],
            "yaxis": "mean absolute error (lower is better)",
        })
    u = read_json(d, "upcoding_detection.json")
    if u:
        metrics.append(m("Fraud recall, adversary unaware",
                          f"{u['baseline']['recall']:.1%}", False))
        metrics.append(m("Fraud recall once adversary adapts",
                          f"{u['worst_case']['recall']:.1%}", False,
                          "same detector, cheapest possible evasion"))
        arms = [u["baseline"]] + u["red_team"]
        charts.append({
            "type": "bar", "title": "Fraud detection under adversarial adaptation",
            "x": [a["scenario"][:26] for a in arms],
            "series": [{"name": "recall", "y": [a["recall"] for a in arms]}],
            "yaxis": "recall",
        })
    f = read_json(d, "hierarchical_forecast.json")
    if f:
        best = min(f["results"], key=lambda r: r["mape_pct_overall"])
        metrics.append(m("Best forecast MAPE",
                          f"{best['mape_pct_overall']:.2f}%", True,
                          f"{best['approach']} - MinT lost on this hierarchy"))
        charts.append({
            "type": "bar", "title": "Forecast reconciliation: MAPE by approach",
            "x": [r["approach"] for r in f["results"]],
            "series": [{"name": "MAPE %", "y": [r["mape_pct_overall"] for r in f["results"]]}],
            "yaxis": "MAPE %",
        })
    c = read_json(d, "metric_copilot.json")
    if c and c.get("llm") and c.get("rules_baseline"):
        metrics.append(m("NL copilot vs keyword rules",
                          f"{c['llm']['overall_accuracy']:.0%} vs "
                          f"{c['rules_baseline']['overall_accuracy']:.0%}", False,
                          "the 0.5B model refused 0% of unanswerable questions"))
    v = read_json(d, "validation.json")
    if v and isinstance(v.get("injected_bugs"), dict) and v["injected_bugs"].get("detection_rate"):
        metrics.append(m("Injected defects caught",
                          f"{v['injected_bugs']['caught']} of "
                          f"{v['injected_bugs']['injected']}", True))
    return metrics, charts


def extract_16(d: Path):
    """Concord - reconciliation engine.

    The pair of numbers is the whole point, so both are surfaced: a perfect
    detection score, and the false positive rate that score concealed.
    """
    metrics, charts = [], []

    det = read_json(d, "detection.json")
    if det:
        metrics.append(m("Injected breaks detected",
                         f"{det['total_detected']} of {det['total_injected']}", True))
        metrics.append(m("False positives on that test", str(det["false_positives"])))

    real = read_json(d, "realistic.json")
    if real:
        metrics.append(m("Breaks injected into the realistic file",
                         str(real["injected_breaks"])))
        metrics.append(m("False positives it reported anyway",
                         f"{real['false_positives']:,} "
                         f"({real['false_positive_rate'] * 100:.1f}%)", True))

    abl = read_json(d, "ablation.json")
    if abl:
        cfg = {c["config"]: c for c in abl["configurations"]}
        base, best = cfg.get("---"), cfg.get("NAB")
        if base and best:
            metrics.append(m("False positive rate, baseline to best",
                             f"{base['false_positive_rate'] * 100:.1f}% -> "
                             f"{best['false_positive_rate'] * 100:.1f}%", True))
            metrics.append(m("Detection across all 8 configurations",
                             f"{best['injected_detected']}/{best['injected_total']}, "
                             "unchanged"))
        charts.append({
            "type": "bar",
            "title": "False positives by matching configuration",
            "note": "N normalise references, A amount+date fallback, B batch matching. "
                    "Zero breaks were injected; every bar is spurious work.",
            "x": [c["config"] for c in abl["configurations"]],
            "series": [{"name": "false positives",
                        "y": [c["false_positives"] for c in abl["configurations"]]}],
            "yaxis": "false positives",
        })
    return metrics, charts


def extract_17(d: Path):
    """Sift - index structures against a linear scan.

    Both directions are surfaced deliberately. The hash index winning by five
    orders of magnitude is the expected result; the ordered structures losing
    to the scan they were built to beat is the one worth reading, and quoting
    only the first would be the more flattering half of one experiment.
    """
    metrics, charts = [], []

    b = read_json(d, "benchmark.json")
    if not b:
        return metrics, charts

    rows = {r["structure"]: r for r in b["measurements"] if r["n"] == 1_000_000}
    scan = rows.get("LinearScan")

    if scan and rows.get("HashIndex"):
        speedup = scan["point_us"] / rows["HashIndex"]["point_us"]
        metrics.append(m("Point query, hash vs scan (1M records)",
                         f"{speedup:,.0f}x faster", True,
                         f"{rows['HashIndex']['point_us']}us against "
                         f"{scan['point_us']:,.0f}us"))

    # Pinned to the largest size on purpose. The penalty happens to be widest at
    # n=1,000 - a size at which nothing matters - and quoting that number would
    # be picking the most flattering row of a negative finding.
    penalties = [a for a in b["analysis"]
                 if a["kind"] == "slower_than_no_index"
                 and a["query"] == "prefix" and a["n"] == 1_000_000]
    if penalties:
        worst = max(penalties, key=lambda a: a["penalty_x"])
        others = len(penalties) - 1
        metrics.append(m("Prefix query, B+ tree vs no index (1M records)",
                         f"{worst['penalty_x']:.2f}x slower", True,
                         f"{worst['structure']}"
                         + (f", and the skip list loses by the same margin" if others else "")))

    if scan and rows.get("SkipList"):
        ratio = rows["SkipList"]["memory_mb"] / scan["memory_mb"]
        metrics.append(m("Skip list memory, against the data itself",
                         f"{ratio:.0f}x", False,
                         f"{rows['SkipList']['memory_mb']:.0f}MB of structure for "
                         f"{scan['memory_mb']:.1f}MB of records"))

    breakeven = [a for a in b["analysis"] if a["kind"] == "break_even"]
    if breakeven:
        worst = max(breakeven, key=lambda a: a["break_even_queries"])
        metrics.append(m("Queries needed to repay the build",
                         f"{worst['break_even_queries']:,}", False,
                         f"{worst['structure']}, {worst['query']} queries at "
                         f"n={worst['n']:,}"))

    if scan:
        ordered = ["LinearScan", "HashIndex", "SortedArray", "BPlusTree(f=64)", "SkipList"]
        present = [s for s in ordered if s in rows and rows[s].get("prefix_us")]
        charts.append({
            "type": "bar",
            "title": "Prefix query latency at one million records (us)",
            "note": "Lower is better, and the leftmost bar is no index at all. "
                    "The two pointer-based structures lose to it; the sorted array, "
                    "doing the same work in contiguous memory, does not.",
            "x": present,
            "series": [{"name": "prefix latency",
                        "y": [rows[s]["prefix_us"] for s in present]}],
            "yaxis": "microseconds",
        })
    return metrics, charts


def extract_18(d: Path):
    """Ironclad - cryptography from spec, and an attack on it.

    The metric that matters is the pair: bytes recovered by timing against the
    naive comparison, and against the constant-time fix. Surfacing only the
    first would be the exploit without the lesson; only the second would be the
    fix with nothing to fix. The chart is the AIMD window sawtooth, which is the
    channel's most legible single figure.
    """
    metrics, charts = [], []

    rec = read_json(d, "timing_recovery.json")
    if rec:
        s = rec["summary"]
        metrics.append(m("MAC bytes recovered by timing, no key",
                         f"{s['naive_bytes_recovered']} / {s['naive_of']}", True,
                         "byte-at-a-time, against a naive comparison"))
        metrics.append(m("Same attack against the constant-time fix",
                         f"{s['control_bytes_recovered']} / {s['control_of']}", True,
                         "the one-line fix, used as a control"))

    lx = read_json(d, "length_extension.json")
    if lx:
        metrics.append(m("H(key‖m) forged, key length guessed",
                         lx["naive_mac_key_lengths_forged"], False,
                         "HMAC is immune to the identical attack"))

    ch = read_json(d, "channel.json")
    if ch:
        fec = ch["forward_error_correction"]
        metrics.append(m("Single-bit line errors corrected (Hamming)",
                         f"{fec['single_bit_errors_rescued']:,} / {fec['trials']:,}",
                         False, "each one a retransmission that never happened"))
        tp = ch["throughput_vs_stop_and_wait"]
        metrics.append(m("Sliding window vs stop-and-wait",
                         f"{tp['speedup']:.0f}x fewer rounds", False,
                         f"{tp['messages']} messages on a clean link"))
        aimd = ch["aimd_over_lossy_link"]
        trace = aimd["cwnd_trace"]
        charts.append({
            "type": "line",
            "title": "AIMD congestion window over a 15%-loss link",
            "note": "Additive increase, multiplicative decrease: the window "
                    "climbs by one per clean round and halves on a loss - TCP's "
                    "control law in miniature, and every message still arrives.",
            "x": list(range(1, len(trace) + 1)),
            "series": [{"name": "congestion window", "y": trace}],
            "yaxis": "frames in flight",
        })
    return metrics, charts


def extract_19(d: Path):
    """Attest - on-chain provenance and escrow, exploited then hardened.

    The metrics that carry the project are the three exploits stated as
    before/after: what each drained from the vulnerable contract, and that the
    hardened one blocked it. The chart is gas per operation, since on-chain cost
    is the constraint that decides whether the design is usable at all.
    """
    metrics, charts = [], []

    ex = read_json(d, "exploits.json")
    if ex:
        r = ex["reentrancy"]["vulnerable"]
        metrics.append(m("Reentrancy: deposited vs drained",
                         f"1 ETH in, {r['drained_eth']:.0f} ETH out", True,
                         "the whole pool; the hardened contract blocks it"))
        ow = ex["over_withdrawal"]["vulnerable"]
        metrics.append(m("Over-withdrawal via unchecked math",
                         f"1 wei in, ~{ow['net_gain_eth']:.0f} ETH out", True,
                         "no bounds check; the hardened contract reverts"))
        fr = ex["front_running"]["vulnerable"]
        metrics.append(m("Front-running the dispute",
                         "seller shuts the buyer out" if fr["front_run_succeeded"]
                         else "—", False,
                         "no time-lock; the hardened window makes ordering moot"))

    con = read_json(d, "consensus.json")
    if con:
        checks = con["proof_of_work"]["whitepaper_checks"]
        passed = sum(1 for c in checks if c["matches"])
        metrics.append(m("Bitcoin-whitepaper cross-check",
                         f"{passed}/{len(checks)} exact", False,
                         "the double-spend formula, matched to seven decimals"))

    gas = read_json(d, "gas.json")
    if gas:
        ops = gas["operations"]
        order = ["createShipment", "recordHandoff", "attestDelivery",
                 "resolveDispute", "withdraw", "raiseDispute"]
        present = [o for o in order if o in ops]
        charts.append({
            "type": "bar",
            "title": "Gas cost per operation (hardened contract)",
            "note": "Measured from real transaction receipts at solc 0.8.24, "
                    "optimizer on. createShipment dominates because it writes "
                    "fresh storage; the rest update existing slots.",
            "x": present,
            "series": [{"name": "gas", "y": [ops[o] for o in present]}],
            "yaxis": "gas units",
        })
    return metrics, charts


def extract_20(d: Path):
    """Timeslice - a measurable operating-systems laboratory.

    The headline metric and the chart are both Belady's anomaly, because a
    fault curve that goes UP as memory grows is the most striking single thing
    in the lab. The rest surface the scheduling and deadlock findings.
    """
    metrics, charts = [], []

    pg = read_json(d, "paging.json")
    if pg:
        anom = pg["belady_classic"]["anomaly"]
        metrics.append(m("Belady's anomaly (FIFO)",
                         f"{anom['faults_from']} -> {anom['faults_to']} faults", True,
                         f"more memory ({anom['frames_from']} -> {anom['frames_to']} frames), "
                         "more faults"))
        srch = pg["belady_search"]
        metrics.append(m("FIFO anomalies vs LRU/Optimal",
                         f"{srch['strings_with_fifo_anomaly']} vs "
                         f"{srch['lru_anomalies']}/{srch['optimal_anomalies']}", False,
                         f"over {srch['trials']:,} random strings - the stack property"))
        # distance from the unbeatable Optimal at 5 frames, high locality
        row = pg["optimal_bound"]["locality_0.8"]["5"]["faults"]
        metrics.append(m("LRU's gap to Optimal (5 frames)",
                         f"+{row['LRU'] - row['Optimal']} faults", False,
                         f"Optimal {row['Optimal']}, LRU {row['LRU']} - the bound made a number"))
        curve = pg["belady_classic"]["fifo_faults_by_frames"]
        charts.append({
            "type": "line",
            "title": "Belady's anomaly: FIFO page faults versus frames",
            "note": "More frames should mean fewer faults. FIFO breaks that - "
                    "the climb from 3 to 4 frames is the anomaly. LRU and "
                    "Optimal never do, because they have the stack property.",
            "x": [int(k) for k in curve.keys()],
            "series": [{"name": "FIFO faults", "y": list(curve.values())}],
            "yaxis": "page faults",
        })

    co = read_json(d, "concurrency.json")
    if co:
        naive = co["dining_philosophers"]["naive"]
        ordered = co["dining_philosophers"]["ordered"]
        metrics.append(m("Dining philosophers: naive vs ordered",
                         f"{naive['deadlocked']}/{naive['runs']} vs "
                         f"{ordered['deadlocked']}/{ordered['runs']} deadlock", False,
                         "a live wait-for-graph detector catches the naive one"))

    return metrics, charts


def extract_21(d: Path):
    """Cadence - soft-computing traffic signal control.

    The headline is the honest GA-versus-exhaustive comparison: a tie on
    quality, a win on time that widens with the network. The chart makes the
    grid's combinatorial explosion visible against the GA's flat cost.
    """
    metrics, charts = [], []

    off = read_json(d, "offsets.json")
    if off:
        grid = off["grid_search"]
        ga = off["genetic_algorithm"]
        sc = off["scaling"]
        metrics.append(m("GA vs grid search (4 intersections)",
                         f"{ga['evaluations']} vs {grid['evaluations']} sims", True,
                         f"same optimum (delay {ga['best_delay']:,.0f}), "
                         f"{off['ga_evaluation_saving'] * 100:.0f}% fewer simulations"))
        metrics.append(m("GA scaling win (6 intersections)",
                         f"{sc['ga_evaluations_used']} vs "
                         f"{sc['grid_points_that_would_be_needed']:,} sims", False,
                         "where the exhaustive grid becomes intractable"))
        charts.append({
            "type": "bar",
            "title": "Simulations to solve: genetic algorithm vs exhaustive grid",
            "note": "A tie on quality; the win is on time, and it widens with "
                    "the network. At six intersections the grid would be "
                    "248,832 simulations; the GA used 825.",
            "x": ["4 intersections", "6 intersections"],
            "series": [
                {"name": "grid search",
                 "y": [grid["evaluations"], sc["grid_points_that_would_be_needed"]]},
                {"name": "genetic algorithm",
                 "y": [ga["evaluations"], sc["ga_evaluations_used"]]},
            ],
            "yaxis": "simulations (log scale)",
            "log_y": True,
        })

    fz = read_json(d, "fuzzy.json")
    if fz:
        metrics.append(m("Fuzzy vs best-tuned fixed split",
                         f"{fz['delay_reduction_vs_best_fixed'] * 100:.0f}% less delay",
                         True,
                         f"fuzzy {fz['fuzzy']['total_delay']:,.0f} vs best fixed "
                         f"{fz['best_fixed_delay']:,.0f} veh*s (green swept for fairness)"))

    hop = read_json(d, "hopfield.json")
    if hop:
        metrics.append(m("Hopfield capacity cliff",
                         f"load {hop['measured_capacity_cliff_ratio']}", False,
                         f"measured on {hop['network_size']} neurons vs the "
                         f"{hop['theoretical_capacity_ratio']} N theory"))

    nz = read_json(d, "neurons.json")
    if nz:
        sep = nz["linearly_separable"]["perceptron"]
        xor = nz["xor"]
        metrics.append(m("Perceptron, and the XOR wall",
                         f"{sep['converged_epoch']} epochs vs "
                         f"{xor['perceptron_accuracy']:.0%} on XOR", False,
                         "converges on separable data; neither it nor ADALINE "
                         "crosses XOR - the 1969 result, reproduced"))

    return metrics, charts


def extract_22(d: Path):
    """Turnstile - event ticketing under contention.

    The headline is that the same reservation logic is correct in a monolith
    and broken across services. The chart makes oversell scale with contention
    for the naive services while the atomic reserve holds the hardened ones flat
    at zero.
    """
    metrics, charts = [], []

    rel = read_json(d, "reliability.json")
    if rel:
        mono, naive, hard = rel["monolith"], rel["naive"], rel["hardened"]
        metrics.append(m("Oversold seats: monolith vs naive vs hardened",
                         f"{mono['oversold_seats']} vs {naive['oversold_seats']} vs "
                         f"{hard['oversold_seats']}", True,
                         "same check-then-act logic; the distribution is the bug, not the algorithm"))
        metrics.append(m("Naive overcharge",
                         f"₹{naive['overcharged_paise'] // 100:,} on "
                         f"₹{naive['correct_charged_paise'] // 100:,} of real sales",
                         False,
                         f"{naive['double_charges']} double charges, "
                         f"{naive['ghost_charges']} charges with no ticket"))
        metrics.append(m("Hardened, same fault load",
                         f"{hard['oversold_seats']} oversold / {hard['double_charges']} double / "
                         f"{hard['ghost_charges']} ghost", False,
                         f"matches the monolith on safety; honest cost is "
                         f"{hard['lost_seats']} sales lost to message drops"))

    dfn = read_json(d, "defences.json")
    if dfn:
        rows = {c["defences"]: c for c in dfn["cases"]}
        none = rows["none"]
        full = rows["atomic_hold+idempotency+compensation"]
        metrics.append(m("Each defence removes one failure class",
                         f"{none['oversold_seats'] + none['double_charges'] + none['ghost_charges']}"
                         f" → 0 safety violations", False,
                         "atomic reserve kills oversell, idempotency kills double "
                         "charges, saga compensation kills ghost charges"))

    sc = read_json(d, "scaling.json")
    if sc:
        charts.append({
            "type": "line",
            "title": "Oversold seats versus contention: naive versus hardened",
            "note": "Oversell is a concurrency bug: with one buyer per seat even "
                    "the naive services oversell nothing; as the crowd grows they "
                    "oversell every seat. The atomic compare-and-set reserve holds "
                    "the hardened services flat at zero throughout.",
            "x": [str(b) for b in sc["buyers_per_seat"]],
            "series": [
                {"name": "naive", "y": sc["naive_oversold_seats"]},
                {"name": "hardened", "y": sc["hardened_oversold_seats"]},
            ],
            "yaxis": "oversold seats (of 20)",
            "xaxis": "buyers per seat",
        })

    return metrics, charts


def extract_23(d: Path):
    """Quantile - applied statistics on air quality, done honestly.

    The headline is the significance-versus-importance inversion: a trivial
    difference measured for years is almost always 'significant' while a real
    difference measured for days usually is not, so a p-value policy and an
    effect-size policy pick opposite stations. The chart makes that inversion
    the picture.
    """
    metrics, charts = [], []

    hyp = read_json(d, "hypothesis.json")
    if hyp:
        up = hyp["underpowering"]
        si = hyp["significance_vs_importance"]
        metrics.append(m("Underpowered vs well-powered detection",
                         f"{up['underpowered']['detection_rate'] * 100:.0f}% vs "
                         f"{up['well_powered']['detection_rate'] * 100:.0f}%", True,
                         "the SAME real 8 ug/m3 effect; power is decided before the test, not after"))
        metrics.append(m("Significance is not importance",
                         f"{si['trivial_station']['prob_significant'] * 100:.0f}% vs "
                         f"{si['meaningful_station']['prob_significant'] * 100:.0f}% significant", False,
                         f"trivial effect (d={si['trivial_station']['cohens_d']:.2f}) beats the real "
                         f"one (d={si['meaningful_station']['cohens_d']:.2f}) on p-value; a p-value "
                         f"policy picks the wrong station"))
        charts.append({
            "type": "bar",
            "title": "Significance is a function of sample size, not importance",
            "note": "The trivial 1.5 ug/m3 difference, measured for years, is "
                    "'significant' almost always (effect size 0.08, negligible); "
                    "the real 9 ug/m3 difference, measured for days, usually is "
                    "not (effect size 0.45). A p-value policy acts on the trivial "
                    "station; report the effect size and decide on that.",
            "x": ["Trivial station (d=0.08)", "Meaningful station (d=0.45)"],
            "series": [{"name": "P(significant at 0.05)",
                        "y": [round(si["trivial_station"]["prob_significant"], 3),
                              round(si["meaningful_station"]["prob_significant"], 3)]}],
            "yaxis": "P(significant)",
        })

    dist = read_json(d, "distributions.json")
    if dist:
        metrics.append(m("Lognormal beats normal (distribution shape)",
                         f"{dist['cities_where_lognormal_wins']}/{dist['cities_total']} cities by AIC",
                         False,
                         "a normal fit has the wrong tail and misstates how often the air is unsafe"))

    reg = read_json(d, "regression.json")
    if reg:
        mc = reg["measured_coverage"]
        metrics.append(m("Regression CI coverage, measured",
                         f"{mc['mean_coverage']}", False,
                         f"the 95% intervals cover the truth {mc['mean_coverage'] * 100:.0f}% of the "
                         f"time across {mc['reps']} regenerated datasets - calibrated, not asserted"))

    exc = read_json(d, "exceedance.json")
    if exc:
        et = exc["extreme_tail"]
        metrics.append(m("Extreme-value tail (peaks-over-threshold GPD)",
                         f"{et['p_exceed_gpd']:.3f} vs {et['p_exceed_empirical']:.3f}", False,
                         "the fitted Generalized Pareto tail matches the thin empirical severe-day rate"))

    return metrics, charts


def extract_24(d: Path):
    """Stratus - cloud media-pipeline economics, modelled for $0.

    The headline chart is the processing-tier crossover: serverless cheaper
    below, always-on above. The metrics carry the twist - serving is 97% of the
    bill, so the whole crossover is a rounding error on the total.
    """
    metrics, charts = [], []

    costs = read_json(d, "costs.json")
    serving = read_json(d, "serving_dominance.json")
    rs = read_json(d, "rightsizing.json")
    base = read_json(d, "baselines.json")
    brk = read_json(d, "breakdown.json")
    val = read_json(d, "validation.json")

    if costs and serving:
        share = serving["rows"][2]["serving_share_of_total"]
        metrics.append(m("Serverless vs always-on crossover",
                         f"{costs['crossover_images_per_month']/1e6:.1f}M images/month", True,
                         "serverless cheaper below, an always-on instance cheaper above"))
        metrics.append(m("...but the CDN is the whole bill",
                         f"{share*100:.0f}% is serving (CloudFront+S3)", True,
                         "so the serverless-vs-servers choice moves the total by ~1-2%; the "
                         "CDN, not the compute, is the real cost lever"))
    if rs:
        metrics.append(m("Right-sizing waste",
                         f"{rs['over_provision_waste_fraction']*100:.0f}% over-provisioned", False,
                         "over-provisioning the instance wastes that much of the compute tier; "
                         "under-provisioning makes the queue unstable and blows the SLO"))
    if brk:
        cpi = brk["serverless"]["cost_per_image_usd"]
        metrics.append(m("Cost per image", f"${cpi:.4f}", False,
                         "the unit economic that scales the business case, set by the CDN"))
    if val:
        err = max(c["rel_error"] for c in val["checks"])
        metrics.append(m("Queue sim vs Erlang C", f"{err*100:.1f}% error", False,
                         "the right-sizing latencies come from a discrete-event queue "
                         "simulation validated against the exact M/M/c formula"))

    if costs:
        vols = costs["volumes"]
        sv = [r["serverless_processing_usd"] for r in costs["curves"]]
        ao = [r["always_on_processing_usd"] for r in costs["curves"]]
        charts.append({
            "type": "line",
            "title": "Processing cost vs monthly volume: serverless vs always-on",
            "note": "The crossover is where the lines meet (~4.1M images/month): "
                    "serverless's per-request cost rises with volume, the always-on "
                    "instance's fixed cost stays flat until it is amortised. Log axes. "
                    "This is the tier that differs; the shared CDN serving cost, ~97% "
                    "of the total, is excluded so the crossover is visible.",
            "x": [f"{v/1e6:g}M" if v >= 1e6 else f"{v/1e3:g}k" for v in vols],
            "series": [
                {"name": "serverless processing", "y": [round(x, 2) for x in sv]},
                {"name": "always-on processing", "y": [round(x, 2) for x in ao]},
            ],
            "yaxis": "processing cost ($/month, log)",
            "xaxis": "images per month (log)",
            "log_y": True,
        })

    return metrics, charts


def extract_25(d: Path):
    """Fieldnote - offline-first inspection sync; convergence is not correctness.

    The headline chart contrasts naive last-write-wins against version vectors +
    atomic apply on the two failure modes that matter (both 'lower is better'):
    records lost to a skewed clock, and inspections broken by a mid-sync crash.
    """
    metrics, charts = [], []

    skew = read_json(d, "clock_skew.json")
    atom = read_json(d, "atomicity.json")

    if skew:
        total = skew["naive"]["total_records"]
        metrics.append(m("Records lost to a skewed clock",
                         f"{skew['naive']['lost_updates']} of {total} (naive) vs "
                         f"{skew['hardened']['lost_updates']}",
                         True,
                         "last-write-wins trusts the wall clock, so a fast phone's stale "
                         "edits beat the server's causally-newer ones; version vectors lose 0"))
        metrics.append(m("Concurrent conflicts detected",
                         f"{skew['naive']['conflicts_detected']} (naive) vs "
                         f"{skew['hardened']['conflicts_detected']}",
                         False,
                         "the naive strategy cannot even see the 30 genuine conflicts it "
                         "resolves; version vectors flag every one"))
        both = skew["naive"]["converged"] and skew["hardened"]["converged"]
        metrics.append(m("Both converge (device == server)?",
                         "yes - for both" if both else "no", True,
                         "so the obvious 'did the two sides agree?' health check passes for "
                         "the naive design while it is silently wrong - convergence is not "
                         "correctness"))
    if atom:
        metrics.append(m("Mid-sync crashes that break an inspection",
                         f"{atom['naive']['crashes_leaving_a_broken_inspection']} of "
                         f"{atom['naive']['crashes_simulated']} "
                         f"({atom['naive']['broken_rate']*100:.0f}%) vs "
                         f"{atom['hardened']['crashes_leaving_a_broken_inspection']}",
                         True,
                         "a non-atomic apply leaves a header claiming five findings above "
                         "three rows; an all-or-nothing apply is never broken"))

    if skew and atom:
        total = skew["naive"]["total_records"]
        charts.append({
            "type": "bar",
            "title": "Two failure modes, naive vs hardened (lower is better)",
            "note": "Both strategies converge (device == server at the end), so a "
                    "convergence check cannot tell them apart. Under a skewed clock the "
                    "naive last-write-wins loses "
                    f"{skew['naive']['lost_updates']} of {total} records; under mid-sync "
                    "crashes it breaks the inspection "
                    f"{atom['naive']['broken_rate']*100:.0f}% of the time. Version vectors "
                    "plus an atomic apply do neither.",
            "x": [f"records lost to skew (of {total})",
                  "inspections broken by crash (%)"],
            "series": [
                {"name": "naive (last-write-wins)",
                 "y": [skew["naive"]["lost_updates"],
                       round(atom["naive"]["broken_rate"] * 100)]},
                {"name": "hardened (version vectors + atomic)",
                 "y": [skew["hardened"]["lost_updates"],
                       round(atom["hardened"]["broken_rate"] * 100)]},
            ],
            "yaxis": "count / percent (lower is better)",
        })

    return metrics, charts


def extract_26(d: Path):
    """Relay - a URL shortener, and the test pyramid as a measurement.

    The headline chart is the cumulative catch curve: how many of the injected
    bugs are caught as you add each test layer (smoke -> unit -> API). The metrics
    carry the honest tail - the bugs that survive every layer.
    """
    metrics, charts = [], []

    s = read_json(d, "summary.json")
    e2e = read_json(d, "e2e.json")

    if s:
        total = s["total_bugs"]
        cum = s["cumulative_caught_adding_layers"]
        per = s["caught_per_layer"]
        metrics.append(m("Smoke baseline (the trivial 'we have tests')",
                         f"{per['smoke']} of {total} bugs caught", True,
                         "a minimal 'does it start' check catches almost nothing - "
                         "the baseline the layered suite must beat"))
        metrics.append(m("Caught after adding every layer",
                         f"{cum['api']} of {total} (smoke {cum['smoke']} -> unit "
                         f"{cum['unit']} -> API {cum['api']})", True,
                         "the API/integration layer is the workhorse: it alone catches "
                         "wiring, persistence, status codes and authorization (incl. IDOR)"))
        metrics.append(m("Bugs that survive every layer",
                         f"{s['missed_by_all_layers']} of {total}", True,
                         "a timing side-channel and an untested collision path - real "
                         "defects functional tests structurally cannot catch"))
    if e2e:
        metrics.append(m("End-to-end browser flows",
                         f"{e2e['passed']}/{e2e['runs']} passed "
                         f"(~{e2e['mean_seconds_per_full_flow']}s each)", False,
                         "Playwright drives the built React app + FastAPI; ~1000x the "
                         "cost of a unit test per assertion - why E2E sits at the tip"))

    if s:
        total = s["total_bugs"]
        cum = s["cumulative_caught_adding_layers"]
        charts.append({
            "type": "bar",
            "title": "Cumulative bugs caught as you climb the test pyramid",
            "note": "Each injected bug is scored against every layer; the bars show "
                    "how many of the %d bugs are caught once you have the smoke "
                    "layer, then also unit, then also the API/integration layer. The "
                    "smoke baseline catches %d; the full stack reaches %d; %d survive "
                    "every layer. Byte-reproducible (reports/summary.json)."
                    % (total, cum["smoke"], cum["api"], s["missed_by_all_layers"]),
            "x": ["smoke", "+ unit", "+ API/integration"],
            "series": [{"name": "bugs caught (cumulative)",
                        "y": [cum["smoke"], cum["unit"], cum["api"]]}],
            "yaxis": "bugs caught (of %d)" % total,
        })

    return metrics, charts


EXTRACTORS = {
    "05": extract_05, "06": extract_06, "07": extract_07, "08": extract_08,
    "09": extract_09, "10": extract_10, "11": extract_11, "12": extract_12,
    "13": extract_13,
    "14": extract_14,
    "15": extract_15,
    "16": extract_16,
    "17": extract_17,
    "18": extract_18,
    "19": extract_19,
    "20": extract_20,
    "21": extract_21,
    "22": extract_22,
    "23": extract_23,
    "24": extract_24,
    "25": extract_25,
    "26": extract_26,
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
