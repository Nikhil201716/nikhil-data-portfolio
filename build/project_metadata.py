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
    {
        "id": "18",
        "slug": "ironclad",
        "dir": "Ironclad-Secure-Channel",
        "title": "Ironclad - Verified Cryptography and a Secure Channel",
        "pitch": "A MAC comparison that returns on the first wrong byte leaks how many "
                  "matched. Timing alone recovers 14 of 32 tag bytes with no key; the "
                  "one-line constant-time fix yields 0.",
        "roles": ["Testing & QA", "Data Engineering"],
        "topics": ["AES-128 from FIPS-197", "SHA-256 from FIPS 180-4",
                    "HMAC and RFC 2104", "RSA, Miller-Rabin, PKCS#1 v1.5",
                    "GF(2^8) and the derived S-box", "Timing side channels",
                    "Welch's t-test and Cohen's d", "Length-extension forgery",
                    "Encrypt-then-MAC", "Hamming(7,4) FEC",
                    "Sliding-window ARQ with AIMD", "NIST/RFC known-answer testing"],
        "stack": ["Python 3.11+", "no dependencies", "stdlib statistics only"],
        "metrics_source": "reports",
        "headline_finding": "The primitives are written from their specifications and checked "
                             "against published NIST and RFC vectors - external ground truth, "
                             "not self-agreement - and then the project attacks its own code. A "
                             "byte-by-byte timing attack against a naive MAC comparison recovers "
                             "14 of 32 tag bytes with no knowledge of the key, degrading with "
                             "depth as the base comparison time grows; the one-line "
                             "constant-time comparison, run as a control, recovers 0 of 10 and "
                             "leaks nothing significant at any position. A length-extension "
                             "forgery breaks H(key||m) at all 32 guessed key lengths while HMAC "
                             "stays immune. The timing magnitudes are machine-dependent by "
                             "nature; the direction - naive leaks and is exploitable, "
                             "constant-time does neither - reproduces, and is what the channel "
                             "is built on.",
    },
    {
        "id": "19",
        "slug": "attest",
        "dir": "Attest-Onchain-Provenance",
        "title": "Attest - On-Chain Provenance and Escrow",
        "pitch": "A deliberately vulnerable escrow contract and three working exploits that "
                  "drain it - reentrancy, unchecked-arithmetic over-withdrawal, front-running "
                  "- then the hardened version where each exploit is run again and stopped.",
        "roles": ["Testing & QA", "Data Engineering"],
        "topics": ["Solidity 0.8.24", "Hardhat", "Reentrancy and the guard/CEI fix",
                    "Unchecked arithmetic and overflow", "Front-running and MEV",
                    "Checks-Effects-Interactions", "Escrow and dispute windows",
                    "Supply-chain provenance", "Gas measurement",
                    "Proof-of-work vs proof-of-stake finality",
                    "Nakamoto double-spend probability", "A no-wallet local DApp"],
        "stack": ["Solidity 0.8.24", "Hardhat", "ethers v6", "no testnet - local EVM only"],
        "metrics_source": "reports",
        "headline_finding": "Security is demonstrated, not asserted. A supply-chain escrow "
                             "contract is built twice - vulnerable and hardened - and three "
                             "exploits are run against both. Reentrancy turns a 1 ETH deposit "
                             "into an 11 ETH drain of the whole pool; unchecked arithmetic turns "
                             "1 wei into ~10 ETH; a seller front-runs the buyer's dispute by "
                             "paying a higher fee. Each is blocked by the hardened contract - a "
                             "reentrancy guard with checks-effects-interactions, a bounds check "
                             "with checked math, and a mandatory dispute window. Gas is measured "
                             "per operation from real receipts, and a consensus simulator "
                             "reproduces the Bitcoin whitepaper's double-spend figures exactly "
                             "(5/5), with a seeded Monte Carlo showing the formula is a mild "
                             "lower bound. 18 tests, all passing; runs entirely on a local EVM.",
    },
    {
        "id": "20",
        "slug": "timeslice",
        "dir": "Timeslice-OS-Lab",
        "title": "Timeslice - A Measurable Operating-Systems Laboratory",
        "pitch": "Belady's anomaly, demonstrated not recited: FIFO page replacement faults "
                  "MORE with more memory - 9 on three frames, 10 on four - while LRU and "
                  "Optimal never do, across 5,000 random strings.",
        "roles": ["Testing & QA", "Data Engineering"],
        "topics": ["CPU scheduling (FCFS/SJF/SRTF/RR/MLFQ)",
                    "Page replacement (FIFO/LRU/Clock/Optimal)", "Belady's anomaly",
                    "The stack property", "Optimal as an unbeatable bound",
                    "Deadlock detection (wait-for graph)", "Dining philosophers",
                    "Producer/consumer", "File allocation and fragmentation",
                    "fork/exec/pipe and Unix sockets", "getrusage kernel accounting",
                    "Jain's fairness index"],
        "stack": ["Python 3.11+", "no dependencies", "threading", "os.fork (Linux/WSL)"],
        "metrics_source": "reports",
        "headline_finding": "Five operating-systems areas, each a comparison of algorithms on "
                             "identical seeded workloads, with the textbook claims measured "
                             "rather than recited. Belady's anomaly is reproduced (FIFO faults "
                             "9 then 10 as frames go 3 then 4) and found in 13 of 5,000 random "
                             "strings for FIFO and 0 for LRU and Optimal - the stack property. "
                             "SRTF minimises average waiting time but has the worst fairness, "
                             "because it starves long jobs to rush short ones. A live wait-for "
                             "graph detector catches the dining philosophers deadlocking (10 of "
                             "10 naive runs) while ordered acquisition never does (0 of 10). "
                             "Contiguous file allocation fails on a fragmented disk with free "
                             "space to spare. And a genuinely native component - a fork/exec/pipe "
                             "shell, a Unix-domain socket, kernel resource accounting - runs on "
                             "real syscalls. Pure standard library; 61 tests pass.",
    },
    {
        "id": "21",
        "slug": "cadence",
        "dir": "Cadence-Traffic-Control",
        "title": "Cadence - Soft-Computing Traffic Signal Control",
        "pitch": "Does a genetic algorithm beat exhaustive grid search at coordinating "
                  "traffic signals? On a four-intersection arterial it finds the SAME "
                  "optimum in 177 simulations against the grid's 1,728 - a tie on quality, "
                  "a win on time that widens with the network.",
        "roles": ["Machine Learning", "Testing & QA"],
        "topics": ["Mamdani fuzzy inference", "Triangular/shoulder membership",
                    "Centroid defuzzification", "Genetic algorithm",
                    "Tournament selection", "Uniform crossover", "Elitism",
                    "Exhaustive grid search baseline", "Hopfield associative memory",
                    "Hebbian storage", "Capacity cliff (0.138 N)", "Perceptron",
                    "ADALINE / delta rule", "The XOR wall",
                    "Store-and-forward traffic model", "Green-wave progression"],
        "stack": ["Python 3.11+", "NumPy only", "from scratch"],
        "metrics_source": "reports",
        "headline_finding": "Five soft-computing methods, each written from scratch on NumPy "
                             "and measured against an honest baseline on a deterministic traffic "
                             "simulator. The genetic algorithm reaches grid search's exact "
                             "offset optimum (a green wave, delay 24,480) in 177 simulations "
                             "versus 1,728 - it does not beat the baseline on quality, it ties, "
                             "and the README says so; the win is on time-to-solution and it "
                             "widens with the network (at six intersections the grid would be "
                             "248,832 simulations, the GA used 825). A Mamdani fuzzy controller "
                             "cuts delay 58% against the BEST-tuned fixed split (the green was "
                             "swept so the baseline is fair, not a strawman). A Hopfield network "
                             "recovers corrupted detector readings until the capacity cliff, "
                             "measured at load 0.156 on 64 neurons against the 0.138 N theory. "
                             "And a perceptron converges in 4 epochs on separable data while "
                             "neither it nor ADALINE crosses XOR - the 1969 result reproduced, "
                             "not recounted. NumPy only; 31 tests pass.",
    },
    {
        "id": "22",
        "slug": "turnstile",
        "dir": "Turnstile-Event-Ticketing",
        "title": "Turnstile - Event Ticketing Under Contention",
        "pitch": "The SAME reservation logic sells every seat once in a monolith and "
                  "oversells 15 of 20 the moment you split it across four microservices - "
                  "overcharging ₹16,000 on ₹10,000 of real sales. The bug is the "
                  "distribution, not the algorithm.",
        "roles": ["Testing & QA", "Data Engineering"],
        "topics": ["Microservices", "Distributed transactions", "Saga pattern",
                    "Event sourcing", "CQRS", "Idempotency keys",
                    "Compare-and-set reservation", "At-least-once delivery",
                    "Message reordering", "Partial failure & compensation",
                    "Fault injection", "Deterministic simulation",
                    "Spring Boot", "Apache Kafka", "Docker Compose",
                    "Safety vs liveness"],
        "stack": ["Java 17", "no dependencies (measured core)",
                   "Spring Boot + Kafka reference stack"],
        "metrics_source": "reports",
        "headline_finding": "Four services - inventory, order, payment, notification - "
                             "coordinating a purchase saga with event sourcing and CQRS, "
                             "measured against a known answer key under a deterministic, seeded "
                             "fault bus that duplicates, drops and reorders messages. The "
                             "headline is an honest indictment of distribution, not of "
                             "microservices: the identical check-then-act reservation sells "
                             "every seat exactly once in a monolith and oversells 15 of 20 "
                             "seats across four services, overcharging ₹16,000 on ₹10,000 "
                             "of real sales with 9 double charges and 2 ghost charges. Three "
                             "defences each remove exactly one failure class - an atomic "
                             "compare-and-set reserve kills oversell, idempotency keys kill "
                             "double charges, saga compensation kills ghost charges - and "
                             "together they match the monolith on every safety measure. The "
                             "unflattering parts are kept: hardening guarantees safety but not "
                             "liveness (2 of 20 sales lost to message drops that more retries "
                             "would recover), and the naive system oversells MORE with a perfect "
                             "network (20/20) than with faults (15/20), because dropped messages "
                             "accidentally prevent some double-confirmations. 45 tests pass; a "
                             "real Spring Boot + Kafka + Docker Compose stack implements the same "
                             "architecture (not required to reproduce any finding).",
    },
    {
        "id": "23",
        "slug": "quantile",
        "dir": "Quantile-Air-Quality-Statistics",
        "title": "Quantile - Applied Statistics on Air Quality",
        "pitch": "Run the power analysis BEFORE the test. An underpowered air-quality "
                  "study detects a real 8 µg/m³ effect only 28.5% of the time; a "
                  "trivial difference measured for years is 'significant' 91.8% of the time. "
                  "Significance is not importance.",
        "roles": ["Data Analysis", "Machine Learning"],
        "topics": ["Power analysis", "Effect size (Cohen's d)", "Confidence intervals",
                    "CI coverage simulation", "Hypothesis testing", "p-value misuse",
                    "Distribution fitting (MLE)", "Lognormal vs normal (AIC)",
                    "Log-linear regression", "Confounding & collinearity",
                    "Wilson intervals", "Extreme-value theory (GPD / peaks-over-threshold)",
                    "Bayesian updating (Beta-Binomial)", "Prior sensitivity",
                    "Replication crisis", "The winner's curse"],
        "stack": ["R 4.x", "base R only (measured core)", "optional tidyverse + ggplot2"],
        "metrics_source": "reports",
        "headline_finding": "Applied statistics on seeded synthetic Indian air-quality data "
                             "(PM2.5 across four cities and seasons, driven by meteorology), with "
                             "injected ground truth so every method is scored against a known "
                             "answer -- base R only for the measured core, no packages. The "
                             "headline is a discipline: run the power analysis before the test and "
                             "judge findings by effect size and interval, never the p-value alone. "
                             "An underpowered design detects a real 8 µg/m³ station "
                             "difference only 28.5% of the time versus 79.6% for a properly-sized "
                             "one; and a trivial 1.5 µg/m³ difference measured for years is "
                             "'significant' 91.8% of the time (effect size 0.08) while a real "
                             "9 µg/m³ difference measured for days is significant only "
                             "18.3% (effect size 0.45) -- so a p-value policy and an effect-size "
                             "policy pick opposite stations. Lognormal beats normal by AIC in all "
                             "four cities (the normal fit has the wrong tail); the regression "
                             "recovers the injected coefficients with measured 95% CI coverage of "
                             "0.949 over 200 datasets; a peaks-over-threshold Generalized Pareto "
                             "tail matches the empirical severe-day rate; and Beta-Binomial "
                             "updating converges to the Wilson interval under a flat prior. 43 "
                             "tests pass; reports bit-reproducible. An idiomatic tidyverse + "
                             "ggplot2 layer is included as reference (not run on the build machine, "
                             "whose application-control policy blocks the tidyverse's native "
                             "libraries).",
    },
    {
        "id": "24",
        "slug": "stratus",
        "dir": "Stratus-Cloud-Media-Pipeline",
        "title": "Stratus - Cloud Media-Pipeline Economics",
        "pitch": "Publish the serverless-vs-always-on crossover for an image pipeline - "
                  "then find that it barely matters, because the CDN is 97% of the bill. "
                  "Modelled from published AWS pricing for $0: no account, no spend.",
        "roles": ["Data Engineering", "Data Analysis"],
        "topics": ["Cloud economics / FinOps", "AWS pricing model", "Serverless vs always-on",
                    "Cost-per-image / unit economics", "Fixed vs variable cost crossover",
                    "Right-sizing", "Queueing theory (M/M/c, M/D/c)", "Erlang C",
                    "Discrete-event simulation", "Utilisation & headroom", "Egress economics",
                    "Terraform (reference IaC)", "Billing alarm & teardown",
                    "Lambda / EC2 / CloudFront / S3", "Reproducible modelling"],
        "stack": ["Python 3.11+", "standard library only", "no cloud account",
                   "Terraform (reference, never applied)"],
        "metrics_source": "reports",
        "headline_finding": "Models the cost of an image pipeline (upload, resize + watermark, "
                             "serve via CDN) from AWS's published on-demand price list - in pure "
                             "Python, locally, with NO AWS account and NO spend (a hard "
                             "requirement). Publishes what the plan asked for and then subverts "
                             "it: serverless processing is cheaper below ~4.1M images/month and an "
                             "always-on instance above it (the crossover), but CloudFront + S3 "
                             "serving is ~97% of the bill at every volume, so the whole "
                             "serverless-vs-servers decision moves the total by only 1-2% - the "
                             "CDN, not the compute architecture, is the real cost lever. "
                             "Right-sizing is measured with a discrete-event queue simulation "
                             "validated against the exact Erlang C formula (<0.5% error): "
                             "over-provisioning the instance wastes 88% of the compute tier, while "
                             "under-provisioning makes the queue unstable and blows the latency "
                             "SLO. The cost-optimal choice beats 'always serverless' by 41% and "
                             "'always the biggest instance' by 88%. Every figure is a MODELLED "
                             "cost from published pricing, not a real bill - the directions are "
                             "robust, the dollars drift as AWS changes prices. 33 tests pass; "
                             "reports bit-reproducible. A real, valid Terraform stack (S3, Lambda, "
                             "CloudFront, EC2/ALB) with a mandatory billing alarm and teardown "
                             "script ships in infra/ as reference - never applied, because "
                             "applying it would cost money and the analysis never does.",
    },
    {
        "id": "25",
        "slug": "fieldnote",
        "dir": "Fieldnote-Offline-Inspection",
        "title": "Fieldnote - Offline-First Inspection Sync",
        "pitch": "A naive last-write-wins sync loses 60 of 100 records to one skewed "
                  "device clock and breaks 85% of mid-sync crashes - yet it 'converges', "
                  "so it passes the obvious health check. Version vectors + atomic apply "
                  "lose 0 and break 0. Convergence is not correctness.",
        "roles": ["Data Engineering", "Testing & QA"],
        "topics": ["Offline-first sync", "Version vectors / vector clocks",
                    "Causal ordering (happens-before)", "Clock skew", "Last-write-wins",
                    "Conflict detection & resolution", "CRDTs",
                    "Strong eventual consistency", "Atomic apply / transactions",
                    "Idempotency", "Convergence vs correctness", "Known-correct oracle",
                    "Room / WorkManager / Compose (reference)", "Deterministic simulation",
                    "Reproducible reports"],
        "stack": ["Kotlin", "JVM 17", "Gradle", "no dependencies (measured core)",
                   "Android: Room + WorkManager + Compose (reference, not built)"],
        "metrics_source": "reports",
        "headline_finding": "A verified pure-Kotlin/JVM sync engine for an offline-first "
                             "inspection app, measuring the two failures such an app actually "
                             "hits against a known-correct oracle - no Android SDK, no emulator, "
                             "no network, no spend. The headline is a discipline: convergence is "
                             "not correctness. A naive last-write-wins sync loses 60 of 100 "
                             "records to a single skewed device clock (it trusts the wall clock, "
                             "so a fast phone's stale edits beat the server's causally-newer ones) "
                             "and detects 0 of the 30 genuine concurrent conflicts; version "
                             "vectors, which carry causal history instead of a timestamp, lose 0 "
                             "and flag all 30. Crucially BOTH strategies converge (device == "
                             "server at the end), so the obvious 'did the two sides agree?' health "
                             "check passes for the naive design while it is silently wrong 60% of "
                             "the time. On a mid-sync crash, a non-atomic apply is left with a "
                             "broken inspection at 50 of 59 interruption points (85%) - a header "
                             "claiming five findings above three rows; an atomic (all-or-nothing) "
                             "apply is broken at 0. The naive baseline is not a straw man: "
                             "last-write-wins is the common default, is trivially convergent, and "
                             "passes the health check. Every number is read from reports/*.json "
                             "written by a real run (./gradlew experiments) and reproduces "
                             "byte-for-byte; 17 scored tests pass. The real Room + WorkManager + "
                             "Compose Android app ships under app/ as faithful reference (not "
                             "built here, because the finding is a distributed-systems property "
                             "provable headless on a bare JVM and needs no device).",
    },
    {
        "id": "26",
        "slug": "relay",
        "dir": "Relay-URL-Shortener",
        "title": "Relay - URL Shortener & the Test Pyramid",
        "pitch": "A smoke test catches 0 of 20 injected bugs; unit reaches 8; the "
                  "API layer reaches 18. Two bugs survive every layer - a timing "
                  "side-channel and an untested collision path. A green suite is not "
                  "an empty bug list.",
        "roles": ["Testing & QA", "Data Engineering"],
        "topics": ["Test pyramid", "Fault injection", "Test automation",
                    "Unit / integration / E2E", "pytest", "Vitest",
                    "React Testing Library", "Playwright E2E", "FastAPI", "React",
                    "TypeScript", "REST API", "JWT auth", "Coverage vs correctness",
                    "Mutation-style catalog", "IDOR / broken access control",
                    "Allowlist vs blocklist", "CI/CD quality gate",
                    "Reproducible reports"],
        "stack": ["Python 3.12+", "FastAPI", "SQLite", "React + TypeScript + Vite",
                   "pytest", "Vitest", "Playwright", "GitHub Actions"],
        "metrics_source": "reports",
        "headline_finding": "A small but complete full-stack URL shortener (React + "
                             "TypeScript front end, FastAPI back end, SQLite, JWT) built "
                             "to turn the test pyramid into a measurement. A catalog of 20 "
                             "realistic, hand-written bugs (a weakened validator, an "
                             "off-by-one in expiry, a dropped owner check, a "
                             "non-constant-time password compare, a redirect that ignores "
                             "its target) is injected one at a time, and every test layer "
                             "is scored against each. The headline is a discipline: a green "
                             "suite is not an empty bug list. The smoke test - what many "
                             "projects ship as 'we have tests' - catches 0 of 20; adding "
                             "unit tests reaches 8; adding the API/integration layer reaches "
                             "18. The API layer is the workhorse: it alone catches wiring, "
                             "persistence, HTTP status codes and authorization (including "
                             "IDOR - one user reading another's data), which the unit layer "
                             "is structurally blind to. And 2 bugs survive EVERY "
                             "deterministic layer: a timing side-channel (== instead of a "
                             "constant-time compare - it changes no function's output, so "
                             "every functional assertion still passes) and a skipped "
                             "collision check (untested because the seeded RNG never "
                             "produces the collision) - each naming the instrument that "
                             "would catch it (a timing experiment; a property/load test). "
                             "Layers: smoke/unit/API via pytest (73 tests) + Vitest with "
                             "React Testing Library (10 tests) + Playwright E2E (8/8 full "
                             "browser flows at ~3.2s each - the cost that keeps E2E at the "
                             "tip). The catch matrix is byte-reproducible, verified by "
                             "re-running and diffing the reports. CI runs every layer plus "
                             "the fault-injection scoring on every push. Everything runs "
                             "free and locally: Python for the backend + measurement, Node "
                             "for the front end.",
    },
]

AREAS = ["Data Analysis", "Data Engineering", "Machine Learning", "AI & LLM Systems", "Testing & QA"]
