"""
project_metadata.py
----------------------
Curated metadata for every project, kept separate from the numbers.

The split matters. METRICS are never written here - they are read from
each project's own reports/*.json by build_catalog.py, or (for Projects
1-4, which predate that convention) quoted from the results table in that
project's README with the source recorded. What lives here is only the
material a machine cannot infer: the one-line pitch, which subject areas the
work speaks to, the stack, and the honest finding worth leading with.

`headline_findings` are deliberately the UNFLATTERING ones where they
exist. A portfolio that only shows wins is not evidence of judgement.
"""

PROJECTS = [
    {
        "id": "01",
        "slug": "upi-complaint-sla",
        "dir": "01-UPI-Payments-Complaint-SLA-Dashboard",
        "title": "UPI Payments Complaint & SLA Dashboard",
        "pitch": "Where do payment complaints breach SLA, and what does that cost?",
        "roles": ["Data Analysis"],
        "topics": ["SQL", "SQLite star schema", "Excel reporting", "Streamlit", "Root-cause analysis"],
        "stack": ["Python", "Pandas", "SQLite", "Streamlit", "Plotly", "openpyxl"],
        "metrics_source": "readme",
        "metrics": [
            {"label": "Tickets analyzed", "value": "15,713"},
            {"label": "Overall SLA compliance", "value": "75.7%", "highlight": True},
            {"label": "Avg. resolution time", "value": "63.1 hrs (median 40.4)"},
            {"label": "Disputed transaction value", "value": "₹1.91 crore"},
        ],
        "headline_finding": "SLA compliance sits at 75.7%, and the breach concentration is not "
                             "uniform - it clusters by channel and agent, which is what makes the "
                             "root-cause analysis actionable rather than descriptive.",
    },
    {
        "id": "02",
        "slug": "churn-rfm",
        "dir": "02-Ecommerce-Customer-Churn-RFM-Segmentation",
        "title": "E-commerce Churn & RFM Segmentation",
        "pitch": "Which customers are about to leave, and how much revenue walks with them?",
        "roles": ["Data Analysis", "Machine Learning"],
        "topics": ["RFM segmentation", "K-Means", "Churn modeling", "Time-based holdout", "SQL"],
        "stack": ["Python", "Pandas", "Scikit-learn", "SQLite", "Streamlit"],
        "metrics_source": "readme",
        "metrics": [
            {"label": "Customers analyzed", "value": "15,000"},
            {"label": "Total historical revenue", "value": "R$ 8,297,917"},
            {"label": "High churn risk", "value": "3,747 (25.1%)", "highlight": True},
            {"label": "Revenue at risk", "value": "R$ 1,895,287", "highlight": True},
        ],
        "headline_finding": "Rule-based RFM quintiles and K-Means were cross-validated against "
                             "each other rather than one being assumed correct; churn was scored "
                             "on a time-based holdout, not a random split, because a random split "
                             "leaks the future.",
    },
    {
        "id": "03",
        "slug": "demand-forecasting",
        "dir": "03-Retail-Demand-Forecasting-Inventory-Dashboard",
        "title": "Retail Demand Forecasting & Inventory",
        "pitch": "What will sell next, and what should we reorder today?",
        "roles": ["Data Analysis", "Machine Learning"],
        "topics": ["Holt-Winters", "SARIMA", "Seasonal-naive baseline", "(s,S) inventory policy"],
        "stack": ["Python", "Statsmodels", "Pandas", "SQLite", "Streamlit"],
        "metrics_source": "readme",
        "metrics": [
            {"label": "Total historical sales", "value": "$516.8M"},
            {"label": "Holt-Winters MAPE", "value": "12.76% (vs 14.36% baseline)", "highlight": True},
            {"label": "Series beating baseline", "value": "92 / 120 (76.7%)", "highlight": True},
            {"label": "Recommended reorder value", "value": "$1,313,264"},
        ],
        "headline_finding": "The model beats the seasonal-naive baseline on only 77% of series - "
                             "reported as a fraction rather than an average, because an aggregate "
                             "MAPE hides the 28 series where the simpler baseline wins.",
    },
    {
        "id": "04",
        "slug": "airflow-etl",
        "dir": "04-Multi-Source-Sales-ETL-Pipeline-Airflow-AWS",
        "title": "Multi-Source Sales ETL Pipeline (Airflow)",
        "pitch": "Three source systems, one warehouse, and proof the pipeline fails safely.",
        "roles": ["Data Engineering"],
        "topics": ["Airflow DAGs", "ETL orchestration", "Data quality gates", "Idempotency", "WSL"],
        "stack": ["Apache Airflow", "Python", "Pandas", "SQLite", "WSL Ubuntu"],
        "metrics_source": "readme",
        "metrics": [
            {"label": "Daily batches loaded", "value": "13"},
            {"label": "Rows in fact_sales", "value": "764"},
            {"label": "Deliberate failures confirmed", "value": "2 / 2", "highlight": True},
            {"label": "Idempotency check", "value": "59 rows twice, no duplicates", "highlight": True},
        ],
        "headline_finding": "The pipeline was deliberately broken twice to prove the quality gates "
                             "actually fail the DAG rather than logging a warning - a passing "
                             "pipeline that has never been made to fail proves nothing.",
    },
    {
        "id": "05",
        "slug": "data-quality-rag",
        "dir": "05-AI-Augmented-Data-Quality-Validation-Framework",
        "title": "AI-Augmented Data Quality Framework",
        "pitch": "dbt models, statistical validation, and a local-LLM copilot over the results.",
        "roles": ["Data Engineering", "AI & LLM Systems"],
        "topics": ["dbt", "DuckDB", "Pandera", "RAG", "Local LLM (Ollama)"],
        "stack": ["dbt", "DuckDB", "Pandera", "Ollama qwen2.5:0.5b", "Streamlit"],
        "metrics_source": "reports",
        "headline_finding": "A retrieval copilot grounded strictly in the validation results, so "
                             "it can only report what the checks actually found.",
    },
    {
        "id": "06",
        "slug": "streaming-fraud",
        "dir": "06-Realtime-Transaction-Streaming-Pipeline",
        "title": "Real-Time Transaction Streaming Pipeline",
        "pitch": "Redis streams, live fraud scoring, and an explainable decision per transaction.",
        "roles": ["Data Engineering", "Machine Learning"],
        "topics": ["Redis Streams", "Real-time scoring", "Rules engine", "Explainability"],
        "stack": ["Redis (Memurai)", "Python", "Streamlit", "Plotly"],
        "metrics_source": "reports",
        "headline_finding": "Scoring is rules-based and fully explainable by design - in fraud "
                             "review, a decision nobody can justify is a decision nobody can act on.",
    },
    {
        "id": "07",
        "slug": "autonomous-ai-ops",
        "dir": "07-Autonomous-AI-Ops-Recommendation-Platform",
        "title": "Autonomous AI-Ops & Recommendation Platform",
        "pitch": "A recommender that monitors, diagnoses and retrains itself - with a rollback.",
        "roles": ["Machine Learning", "AI & LLM Systems", "Testing & QA"],
        "topics": ["SVD recommender", "PSI drift", "Multi-agent loop", "FastAPI",
                    "AI-augmented QA", "Playwright", "Self-healing locators"],
        "stack": ["Scikit-learn", "FastAPI", "Ollama", "Playwright", "pytest", "Streamlit"],
        "metrics_source": "reports",
        "headline_finding": "The LLM failed twice to generate genuinely novel test cases, and the "
                             "self-healing locator was redesigned after pure-LLM matching failed "
                             "5/5 - both reported rather than quietly dropped.",
    },
    {
        "id": "08",
        "slug": "autoclaim",
        "dir": "08-AutoClaim-Intelligence-Platform",
        "title": "AutoClaim Intelligence Platform",
        "pitch": "Read the claim PDF, look at the damage photo, and check whether they agree.",
        "roles": ["AI & LLM Systems", "Machine Learning", "Data Engineering"],
        "topics": ["Document AI", "OCR", "LLM extraction", "CNN from scratch", "Cross-modal agent",
                    "dbt semantic layer", "Data contracts"],
        "stack": ["pdfplumber", "PyTorch", "Ollama", "dbt", "DuckDB", "Streamlit"],
        "metrics_source": "reports",
        "headline_finding": "A prompt fix took LLM extraction failures from 3/3 to 0/80; the "
                             "reconciliation agent's false positives were root-caused to its own "
                             "thresholds being stricter than reality, not to pipeline errors.",
    },
    {
        "id": "09",
        "slug": "trust-experimentation",
        "dir": "09-Trust-Aware-Experimentation-Platform",
        "title": "Trust-Aware Experimentation Platform",
        "pitch": "Fraud rings quietly inflate your A/B test. Catch them before you ship the result.",
        "roles": ["Data Analysis", "Data Engineering", "AI & LLM Systems"],
        "topics": ["Graph fraud detection", "A/B testing", "Bayesian inference", "Sequential testing",
                    "PII detection", "k-anonymity", "Guardrailed NL-to-SQL"],
        "stack": ["NetworkX", "SciPy", "DuckDB", "Ollama", "Streamlit"],
        "metrics_source": "reports",
        "headline_finding": "Excluding detected fraud rings cut the apparent lift from 57.3% to "
                             "25.4% - both 'significant', but supporting very different decisions. "
                             "The local LLM scored 0% recall on name detection, reported as-is.",
    },
    {
        "id": "10",
        "slug": "delivery-ops",
        "dir": "10-Delivery-Operations-Intelligence-Platform",
        "title": "Delivery Operations Intelligence Platform",
        "pitch": "Speech, optimization, causal inference and MLOps for a delivery operator.",
        "roles": ["Machine Learning", "AI & LLM Systems", "Data Analysis"],
        "topics": ["Whisper ASR", "Offline TTS", "Linear programming", "Propensity score matching",
                    "Difference-in-differences", "Model registry", "Canary deployment"],
        "stack": ["OpenAI Whisper", "pyttsx3", "PuLP/CBC", "Scikit-learn", "FastAPI", "Docker"],
        "metrics_source": "reports",
        "headline_finding": "The naive impact estimate got the SIGN wrong (+34.6% vs a true -18%); "
                             "difference-in-differences landed within 1.7pp. A real train/serve "
                             "feature mismatch was found by actually calling the API.",
    },
    {
        "id": "11",
        "slug": "fair-lending",
        "dir": "11-Fair-Lending-Intelligence-Platform",
        "title": "Fair Lending Intelligence Platform",
        "pitch": "Spark at scale, SHAP explanations, and a fairness audit scored against ground truth.",
        "roles": ["Data Engineering", "Machine Learning", "AI & LLM Systems"],
        "topics": ["PySpark", "SHAP", "Disparate impact", "Equalized odds", "H3 geospatial",
                    "Hybrid retrieval", "Red-teaming", "Bootstrap CIs"],
        "stack": ["PySpark 4.2", "SHAP", "H3", "sentence-transformers", "Ollama", "Streamlit"],
        "metrics_source": "reports",
        "headline_finding": "The hypothesis was refuted: a proxy correlated 0.54 with the protected "
                             "group did NOT drive disparate impact. Three guardrail fixes were "
                             "measured and all three rejected.",
    },
    {
        "id": "12",
        "slug": "retail-intelligence",
        "dir": "12-Retail-Intelligence-Platform",
        "title": "Retail Intelligence Platform",
        "pitch": "A fine-tuned transformer, a knowledge graph, a pricing bandit - and tests with teeth.",
        "roles": ["AI & LLM Systems", "Machine Learning", "Testing & QA"],
        "topics": ["Transformer fine-tuning", "int8 quantization", "Knowledge graph", "GraphRAG",
                    "Contextual bandits", "Off-policy evaluation", "Property-based testing",
                    "Metamorphic testing", "Mutation testing", "Load testing"],
        "stack": ["PyTorch", "transformers", "NetworkX", "Hypothesis", "mutmut", "Locust", "FastAPI"],
        "metrics_source": "reports",
        "headline_finding": "The fine-tuned transformer bought nothing over an 11.8KB bigram model "
                             "(same accuracy, 36.7x slower, 7,580x larger), and int8 quantization "
                             "made inference 3.7x SLOWER, not faster.",
    },
    {
        "id": "13",
        "slug": "meridian-operations-cloud",
        "dir": "13-Meridian-Operations-Cloud",
        "title": "Meridian Operations Cloud",
        "pitch": "A product rather than another standalone script: one 7-workspace application over a single "
                  "warehouse, absorbing every skill from Projects 1-12.",
        "roles": ["Data Engineering", "Machine Learning", "AI & LLM Systems", "Data Analysis"],
        "topics": ["Star schema + declared grain", "Data quality SLAs", "Lineage & blast radius",
                    "Fault injection", "Point-in-time feature store", "Training-serving skew",
                    "Concept drift", "Anomaly shapes", "Model registry + canary gate",
                    "PII governance", "k-anonymity", "Difference-in-differences",
                    "Sequential testing", "Grounded LLM generation"],
        "stack": ["DuckDB", "FastAPI", "scikit-learn", "pandas", "Hypothesis", "pytest",
                   "Plotly", "Ollama qwen2.5:0.5b"],
        "metrics_source": "reports",
        "headline_finding": "The promoted model trains on 17% of the available rows. 83% of the "
                             "training window predates a concept drift, and discarding it raised "
                             "AUC 0.8313 -> 0.8866 and doubled average precision. Separately, a "
                             "grounded-LLM guardrail that scored 3/3 clean was passing a "
                             "fabrication - it checked numerals, and the model wrote 'only one "
                             "late delivery' where the fact was 14.2 percent.",
    },
    {
        "id": "14",
        "slug": "cascade-realtime",
        "dir": "14-Cascade-Realtime-Intelligence-Platform",
        "title": "Cascade Realtime Intelligence Platform",
        "pitch": "Event-time stream processing scored against an answer key, an LLM judge that "
                  "inflated a failing agent to 100%, and a test suite measured by what it catches.",
        "roles": ["Data Engineering", "AI & LLM Systems", "Testing & QA", "Machine Learning"],
        "topics": ["Event time vs processing time", "Watermarks", "Late-data policy",
                    "Clock skew", "At-least-once delivery", "Idempotent sinks",
                    "Exactly-once semantics", "CDC", "Slowly changing dimensions",
                    "Replay determinism", "LLM-as-judge calibration", "Agent trajectories",
                    "Prompt injection", "Mutation / injected-bug testing",
                    "Flaky-test detection", "Playwright E2E"],
        "stack": ["Redis Streams", "SQLite", "FastAPI", "pandas", "Playwright", "pytest",
                   "Hypothesis", "Plotly", "Ollama qwen2.5:0.5b"],
        "metrics_source": "reports",
        "headline_finding": "36 devices out of 2,600 with fast clocks pushed a max-based watermark "
                             "200 seconds ahead of the real clock, causing it to discard 39,103 of "
                             "40,877 messages. And an LLM judge approved 28 of 28 wrong answers, "
                             "reporting 100% accuracy for an agent that was right 22.2% of the "
                             "time - 77.8 points of pure inflation.",
    },
    {
        "id": "15",
        "slug": "aegis-health-plan",
        "dir": "15-Aegis-Health-Plan-Platform",
        "title": "Aegis Health Plan Intelligence Platform",
        "pitch": "A payer's analytics platform where every number compiles from one governed "
                  "definition - and a 'clarifying' definition change silently restates 33 "
                  "published historical figures.",
        "roles": ["Data Analysis", "Data Engineering", "Machine Learning", "AI & LLM Systems", "Testing & QA"],
        "topics": ["Semantic layer / metrics as code", "Metric regression testing",
                    "Survival analysis", "Right-censoring", "Competing risks",
                    "Cox proportional hazards", "Discrete-time hazard",
                    "Hierarchical forecasting", "Forecast reconciliation (MinT)",
                    "Upcoding detection", "Adversarial red-teaming",
                    "Risk adjustment", "Model calibration", "Fairness audit",
                    "NL-to-governed-metrics", "Requirement traceability",
                    "Hash-chained audit trail", "Injected-defect scoring"],
        "stack": ["DuckDB", "pandas", "NumPy", "SciPy", "scikit-learn", "FastAPI",
                   "pytest", "Hypothesis", "Plotly", "Ollama qwen2.5:0.5b"],
        "metrics_source": "reports",
        "headline_finding": "A fraud detector that scores 95.5% recall drops to 18.2% against "
                             "the cheapest possible adaptation. And on survival, the "
                             "discrete-time hazard recovers the injected coefficients 26x more "
                             "accurately than treating churn as a yes/no label - Cox, the "
                             "default choice, is 13x worse than the model that matches how the "
                             "data actually arrive.",
    },
    {
        "id": "16",
        "slug": "concord",
        "dir": "Concord-Reconciliation-Engine",
        "title": "Concord - Double-Entry Reconciliation Engine",
        "pitch": "It detects 175 of 175 injected breaks. On a statement file with no breaks "
                  "at all, it reports 690 of them.",
        "roles": ["Data Engineering", "Testing & QA"],
        "topics": ["Double-entry bookkeeping", "Exact decimal arithmetic",
                    "Constructor-enforced invariants", "JDBC transactions and rollback",
                    "Revalidation on load", "Reference normalisation",
                    "Subset-sum batch matching", "Injected-break scoring",
                    "False-positive measurement", "Full factorial ablation",
                    "Servlet lifecycle without a container"],
        "stack": ["Java 17", "SQLite (JDBC)", "javac only - no build tool",
                   "com.sun.net.httpserver"],
        "metrics_source": "reports",
        "headline_finding": "A perfect 175/175 detection score, produced by a test whose "
                             "injector and engine shared an author, hid a 36.5% false positive "
                             "rate on a statement file containing no breaks at all. Fixing it "
                             "as a full factorial showed reference normalisation contributes "
                             "exactly zero once amount-and-date matching exists, and that the "
                             "only NP-complete component was failing because of which 24 "
                             "candidates it was handed, not because of its search.",
    },
    {
        "id": "17",
        "slug": "sift",
        "dir": "Sift-Log-Search-Engine",
        "title": "Sift - Log Search Engine and Index Benchmark",
        "pitch": "A hash index answers a point query 72,000x faster than scanning. On a "
                  "low-selectivity prefix query, the B+ tree and the skip list are both "
                  "slower than having no index at all - in two independent runs.",
        "roles": ["Data Engineering", "Testing & QA"],
        "topics": ["Hash tables with separate chaining", "Sorted arrays and binary search",
                    "B+ trees with leaf chaining", "Skip lists and probabilistic balance",
                    "Inverted indexes and posting-list merges",
                    "Shunting-yard parsing", "Selectivity", "Break-even analysis",
                    "Cache locality and dependent loads",
                    "JVM microbenchmarking traps", "Oracle-based correctness testing"],
        "stack": ["Java 17", "javac only - no build tool", "no dependencies"],
        "metrics_source": "reports",
        "headline_finding": "Asymptotics predict the hash index winning point queries by five "
                             "orders of magnitude, and it does. They also predict tree "
                             "structures winning prefix queries, and there the B+ tree and the "
                             "skip list both lose to the scan they were built to replace - a "
                             "prefix matching half the data leaves almost nothing to skip, so "
                             "they pay for pointer-chasing and get nothing back. Running the "
                             "whole benchmark a second time before publishing cost one claim: "
                             "the sorted array beat the scan by 33% in the first run and lost "
                             "to it by 3% in the second, so it sits at parity rather than "
                             "ahead. The direction of the finding held both times; the "
                             "magnitude moved by a third.",
    },
]

AREAS = ["Data Analysis", "Data Engineering", "Machine Learning", "AI & LLM Systems", "Testing & QA"]
