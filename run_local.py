#!/usr/bin/env python3
"""Local runner for the portfolio — makes the "Run on this machine" button real.

A page served over the public internet can never execute commands on a visitor's
computer (browsers forbid it, for good reason). This small script is the honest
way to get that behaviour on a machine that actually has the projects: it serves
the portfolio locally AND exposes an endpoint that runs a project's real command
and streams the real output back to the page.

    python run_local.py
    # then open http://localhost:8800  and click "Run on this machine" on any project

It runs ONLY the fixed, known command for each project (never anything from the
request), binds to localhost only, and accepts run requests only from this local
site or the published portfolio origin. Nothing here reaches the open internet.

Requirements to actually run a given project: that project's folder must sit next
to this one (the default), and its dependencies must be installed (tick "install
deps first" in the UI, or it uses the project's .venv if present).
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("PORTFOLIO_RUNNER_PORT", "8800"))
HERE = Path(__file__).resolve().parent
PROJECTS_ROOT = Path(os.environ.get("PORTFOLIO_PROJECTS_ROOT", str(HERE.parent))).resolve()

ALLOWED_ORIGINS = {
    f"http://localhost:{PORT}", f"http://127.0.0.1:{PORT}",
    "https://nikhil201716.github.io",
}

# The exact command each project runs — identical to the site's RUN_CMD /
# INSTALL_CMD. Never taken from the request.
RUN_CMD = {
    "01": "python scripts/run_pipeline.py", "02": "python scripts/run_pipeline.py",
    "03": "python scripts/run_pipeline.py",
    "04": "airflow dags test sales_etl_pipeline 2026-07-20",
    "05": "python scripts/run_pipeline.py", "06": "python pipeline/consumer.py --duration 110",
    "07": "python scripts/run_pipeline.py", "08": "python scripts/run_pipeline.py",
    "09": "python scripts/run_pipeline.py", "10": "python scripts/run_pipeline.py",
    "11": "python scripts/run_pipeline.py", "12": "python scripts/run_pipeline.py",
    "13": "python run_all.py", "14": "python run_all.py", "15": "python run_all.py",
    "16": "./build.sh all", "17": "./build.sh all", "18": "python run.py --quick",
    "19": "npx hardhat test", "20": "python run.py", "21": "python run.py",
    "22": "./build.sh all", "23": "Rscript R/run_all.R", "24": "python run.py",
    "25": "./gradlew runTests experiments", "26": "python scoring/score.py",
    "27": "python scoring/score.py", "28": "python scoring/score.py",
    "29": "python scoring/score.py", "30": "python -m harness.score",
}
INSTALL_CMD = {
    "16": None, "17": None, "18": None, "19": "npm install", "20": None, "22": None,
    "23": None, "24": None, "25": None,
    "26": "pip install -r backend/requirements.txt",
    "27": "pip install -r provider/requirements.txt",
    "28": "pip install -r requirements.txt", "29": "pip install -r requirements.txt",
    "30": "pip install -r requirements.txt",
}


def _catalog_dirs() -> dict[str, str]:
    try:
        cat = json.loads((HERE / "data" / "catalog.json").read_text(encoding="utf-8"))
        return {p["id"]: p["dir"] for p in cat["projects"]}
    except Exception:
        return {}


ID_DIR = _catalog_dirs()


def _venv_python(project_dir: Path) -> str | None:
    for rel in (".venv/Scripts/python.exe", ".venv/bin/python"):
        cand = project_dir / rel
        if cand.exists():
            return str(cand)
    return None


def _install_for(pid: str) -> str | None:
    return INSTALL_CMD[pid] if pid in INSTALL_CMD else "pip install -r requirements.txt"


def _resolve(cmd: str, project_dir: Path) -> str:
    """Point a leading `python`/`pip` at the project's own .venv if it has one."""
    vpy = _venv_python(project_dir)
    if not vpy:
        return cmd
    if cmd.startswith("python "):
        return f'"{vpy}"' + cmd[len("python"):]
    if cmd.startswith("pip "):
        return f'"{vpy}" -m pip' + cmd[len("pip"):]
    return cmd


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *a):  # quieter console
        pass

    # ---- CORS / preflight
    def _cors(self):
        origin = self.headers.get("Origin", "")
        self.send_header("Access-Control-Allow-Origin", origin if origin in ALLOWED_ORIGINS else "null")
        self.send_header("Vary", "Origin")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            return self._health()
        if parsed.path.startswith("/api/run/"):
            return self._run(parsed)
        return super().do_GET()

    # ---- endpoints
    def _health(self):
        avail = {}
        for pid, d in ID_DIR.items():
            pdir = PROJECTS_ROOT / d
            avail[pid] = {
                "exists": pdir.is_dir(),
                "venv": bool(_venv_python(pdir)) if pdir.is_dir() else False,
            }
        body = json.dumps({
            "ok": True, "projects_root": str(PROJECTS_ROOT), "available": avail,
        }).encode()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _sse(self, event: str | None, data: str):
        chunk = ""
        if event:
            chunk += f"event: {event}\n"
        for line in data.split("\n"):
            chunk += f"data: {line}\n"
        chunk += "\n"
        self.wfile.write(chunk.encode("utf-8", "replace"))
        self.wfile.flush()

    def _run(self, parsed):
        origin = self.headers.get("Origin", "")
        # CSRF guard: only this local site or the published portfolio may trigger a run.
        if origin and origin not in ALLOWED_ORIGINS:
            self.send_response(403); self._cors(); self.end_headers(); return

        pid = parsed.path.rsplit("/", 1)[-1]
        if pid not in RUN_CMD:
            self.send_response(404); self._cors(); self.end_headers(); return
        want_install = parse_qs(parsed.query).get("install", ["0"])[0] == "1"

        project_dir = PROJECTS_ROOT / ID_DIR.get(pid, "")
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        if not project_dir.is_dir():
            self._sse(None, f"✗ project folder not found: {project_dir}")
            self._sse("done", "1"); return

        steps = []
        if want_install and _install_for(pid):
            steps.append(_resolve(_install_for(pid), project_dir))
        steps.append(_resolve(RUN_CMD[pid], project_dir))

        env = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8")
        rc = 0
        try:
            self._sse(None, f"▸ running in {project_dir}")
            for step in steps:
                self._sse(None, f"$ {step}")
                proc = subprocess.Popen(
                    step, cwd=str(project_dir), shell=True, env=env,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1, encoding="utf-8", errors="replace",
                )
                for line in proc.stdout:
                    try:
                        self._sse(None, line.rstrip("\n"))
                    except (BrokenPipeError, ConnectionResetError):
                        proc.terminate(); return
                rc = proc.wait()
                if rc != 0:
                    break
        except Exception as e:  # noqa: BLE001
            self._sse(None, f"✗ runner error: {e}")
            rc = 1
        try:
            self._sse("done", str(rc))
        except (BrokenPipeError, ConnectionResetError):
            pass


def main():
    os.chdir(HERE)  # serve the portfolio files
    handler = partial(Handler, directory=str(HERE))
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    print("=" * 66)
    print(" Portfolio local runner")
    print("=" * 66)
    print(f"  Serving   : http://localhost:{PORT}")
    print(f"  Projects  : {PROJECTS_ROOT}")
    print(f"  Live-run  : click 'Run on this machine' on any project page")
    print(f"  (bound to 127.0.0.1 only — nothing is exposed to the network)")
    print("=" * 66)
    print("  Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped.")


if __name__ == "__main__":
    main()
