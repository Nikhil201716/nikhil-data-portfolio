# Run the projects live from the portfolio

The published site at **nikhil201716.github.io/nikhil-data-portfolio** can *show*
a real run (the in-page "▶ Run" replays captured output) and can open a project
in **GitHub Codespaces** (real execution, in the cloud). What a public web page
**cannot** do — ever — is run commands on a visitor's own computer. Browsers
forbid it, and no site should be trusted that claims otherwise.

To actually run a project **on this machine** and watch the real output stream
into the page, use the bundled local runner.

## One command

```bash
python run_local.py
```

Then open **http://localhost:8800**, go to any project, open the **Run & replay**
tab, and click **▶ Run on this machine (live)**. It asks for confirmation (showing
the exact command), runs that project in its own folder, and streams the real
stdout into the terminal on the page.

## What it needs

- The project folders must sit next to this one (the default layout —
  `Desktop/Projects/00-Portfolio-Website` beside `Desktop/Projects/<project>`).
  Point elsewhere with `PORTFOLIO_PROJECTS_ROOT=/path python run_local.py`.
- That project's dependencies must be installed. If a project has a `.venv`, the
  runner uses it automatically; otherwise tick **install deps first** (or run the
  install command once yourself). Projects that need another runtime (Node, R,
  JDK) use that runtime's command as-is.

## Safety

- Binds to **127.0.0.1 only** — nothing is exposed to your network.
- Runs **only the fixed, known command** for each project (listed in
  `run_local.py`), never anything from the request.
- Accepts run requests only from this local site or the published portfolio
  origin, so another website can't trigger a run.
- Change the port with `PORTFOLIO_RUNNER_PORT=9000 python run_local.py`.

Stop it with Ctrl+C.
