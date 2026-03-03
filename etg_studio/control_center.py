"""
ETG Control Center — Dashboard web unificata v2 (02/03/2026)

Novità v2:
  - Tab system: Editor | Progresso | Esplora
  - Sidebar: sezioni "Per Notaio" e "Output Agenti"
  - Carlo.txt esclusa dalla lista scambio (ha pannello dedicato)
  - Endpoint: /api/progress, /api/fornotaio, /api/fornotaio/file, /api/output/file, /api/browse
  - Browser app mode (--app flag, no barra indirizzi)

Avvio: python etg_studio/control_center.py
Browser: http://localhost:8765
"""

import json
import logging
import os
import sqlite3
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

SCRIPT_DIR  = Path(__file__).parent
ETG_ROOT    = SCRIPT_DIR.parent
WORKSPACE   = (SCRIPT_DIR / "workspace").resolve()
SCAMBIO     = WORKSPACE / "scambio"
BOOTLOADERS = SCRIPT_DIR / "bootloaders"
FOR_NOTAIO  = WORKSPACE / "for_notaio"
CARLO_TXT   = SCAMBIO / "Carlo.txt"
DB_FILE     = SCAMBIO / "etg_registro.db"
PORT        = 8765

BROWSE_ROOTS = {
    "ClaudeETG":   ETG_ROOT / "ClaudeETG",
    "ETG_G":       ETG_ROOT / "ETG_G",
    "ETG_P":       ETG_ROOT / "ETG_P",
    "lab":         WORKSPACE / "lab",
    "bootloaders": SCRIPT_DIR / "bootloaders",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger("control_center")


# ── Funzioni dati ─────────────────────────────────────────────────────────────

def get_sessions():
    d = WORKSPACE / "sessions"
    if not d.exists():
        return []
    out = []
    for f in sorted(d.glob("session_*.json"), reverse=True):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            continue
    return out[:20]


def get_inbox_counts():
    base = WORKSPACE / "inbox"
    counts = {}
    for agent in ["gemini", "sonnet", "claude", "orchestrator"]:
        d = base / agent
        counts[agent] = len(list(d.glob("*.json"))) if d.exists() else 0
    return counts


def get_scambio_files():
    """File .md/.txt in scambio/ — Carlo.txt esclusa (ha pannello dedicato)."""
    if not SCAMBIO.exists():
        return []
    return sorted(
        [f.name for f in SCAMBIO.iterdir()
         if f.is_file() and f.suffix in (".md", ".txt") and f.name != "Carlo.txt"],
        reverse=True
    )


def get_bootloaders():
    if not BOOTLOADERS.exists():
        return []
    return sorted(f.name for f in BOOTLOADERS.glob("*.md"))


def get_agent_activity():
    now = datetime.now().timestamp()
    def lm(pat):
        fs = list(SCAMBIO.glob(pat))
        return max((f.stat().st_mtime for f in fs), default=None) if fs else None
    gm = lm("gemini_MSG_*.md")
    om = lm("opus_MSG_*.md")
    return {
        "gemini": (now - gm) < 86400 if gm else False,
        "sonnet": True,
        "opus":   (now - om) < 86400 if om else False,
    }


def get_for_notaio():
    """Sessioni pronte per notarizzazione in workspace/for_notaio/."""
    if not FOR_NOTAIO.exists():
        return []
    results = []
    for item in sorted(FOR_NOTAIO.iterdir()):
        if item.is_dir() and item.name.startswith("SESSION_"):
            if (item / "FINAL.md").exists():
                results.append({"dir": item.name, "file": "FINAL.md"})
        elif item.is_file() and item.suffix == ".md":
            results.append({"dir": "", "file": item.name})
    return results


def get_output_files():
    """File output agenti: AGENTE_*.md in workspace/output/ o scambio/."""
    results = []
    for base_dir, pattern in [(WORKSPACE / "output", "*.md"), (SCAMBIO, "AGENTE_*.md")]:
        if base_dir.exists():
            for f in sorted(base_dir.glob(pattern)):
                results.append({"src": base_dir.name, "file": f.name})
    return results


PROGRESS_FILE = WORKSPACE / "progress.json"

_PROGRESS_DEFAULTS = {
    "chain": [
        {"id": "H_C",       "st": "ok",      "desc": "Shannon | D — approvata"},
        {"id": "Z_C",       "st": "ok",      "desc": "H_C/(DH_D\u2212H_C) — approvata"},
        {"id": "F_C",       "st": "warn",    "desc": "Z_C\u00b2\u00b7DH_D/DH_\u2113 — candidata"},
        {"id": "\u0394_\u2113", "st": "pending", "desc": "Attende F_C definitiva"},
    ],
    "tasks": [
        {"text": "Notarizzare SESSION_002/003/004",            "p": "ALTA",  "who": "Carlo \u2192 Opus"},
        {"text": "F_C derivazione (\u0394 decomp, DH relazione)", "p": "ALTA",  "who": "Ag. Matematico"},
        {"text": "Verdict VOCABOLARIO v1.4",                    "p": "MEDIA", "who": "Carlo"},
        {"text": "Vocab: alfa / \u039b / \u0393 / nome spazio sopra L", "p": "MEDIA", "who": "Carlo"},
        {"text": "3 frasi ETG master (post-vocab)",              "p": "MEDIA", "who": "Post-vocab"},
    ],
}


def get_progress():
    """Stato catena ETG-P letto da workspace/progress.json (aggiornabile dagli agenti).
    Le sessioni sono sempre lette da disco (dinamiche).
    Fallback ai default se il file non esiste."""
    # Leggi progress.json
    logging.info("PROGRESS_FILE: %s  exists=%s", PROGRESS_FILE, PROGRESS_FILE.exists())
    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8-sig"))
            logging.info("progress.json letto: %d task, updated_by=%s",
                         len(data.get("tasks", [])), data.get("updated_by", "?"))
        except Exception as e:
            logging.warning("Errore lettura progress.json: %s", e)
            data = _PROGRESS_DEFAULTS.copy()
    else:
        logging.warning("progress.json non trovato — uso defaults")
        data = _PROGRESS_DEFAULTS.copy()
    chain = data.get("chain", _PROGRESS_DEFAULTS["chain"])
    tasks = data.get("tasks", _PROGRESS_DEFAULTS["tasks"])
    # Sessioni: sempre da disco
    sessions = []
    lab = WORKSPACE / "lab"
    if lab.exists():
        for sd in sorted(lab.iterdir()):
            if not (sd.is_dir() and sd.name.startswith("SESSION_")):
                continue
            in_fn = (FOR_NOTAIO / sd.name / "FINAL.md").exists()
            if sd.name == "SESSION_001":
                s = "abandoned"
            elif in_fn:
                s = "notaio"
            elif (sd / "FINAL.md").exists():
                s = "final"
            else:
                s = "progress"
            sessions.append({"name": sd.name, "status": s})
    result = {"chain": chain, "sessions": sessions, "tasks": tasks}
    if "updated" in data:
        result["updated"] = data["updated"]
    if "updated_by" in data:
        result["updated_by"] = data["updated_by"]
    return result


def read_carlo_txt():
    if not CARLO_TXT.exists():
        return "", 0
    return CARLO_TXT.read_text(encoding="utf-8"), CARLO_TXT.stat().st_mtime


def append_to_carlo(motivo: str, testo: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n\n---\nAutore: Carlo\nData: {ts}\n"
        f"Motivo: {motivo or '(nessuno)'}\n---\n{testo}\n"
    )
    CARLO_TXT.parent.mkdir(parents=True, exist_ok=True)
    with open(CARLO_TXT, "a", encoding="utf-8") as f:
        f.write(entry)


def get_registro(limit: int = 40):
    """Legge gli ultimi N messaggi da etg_registro.db."""
    if not DB_FILE.exists():
        return []
    try:
        con = sqlite3.connect(str(DB_FILE))
        con.row_factory = sqlite3.Row
        cur = con.execute(
            "SELECT id, autore, data_ora, motivo, contenuto "
            "FROM messaggi ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = [dict(r) for r in cur.fetchall()]
        con.close()
        return list(reversed(rows))
    except Exception as e:
        logger.warning("get_registro error: %s", e)
        return []


def insert_registro(autore: str, motivo: str, contenuto: str):
    """Inserisce un nuovo messaggio in etg_registro.db."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = sqlite3.connect(str(DB_FILE))
    con.execute(
        "INSERT INTO messaggi (autore, data_ora, motivo, contenuto) VALUES (?, ?, ?, ?)",
        (autore, ts, motivo, contenuto),
    )
    con.commit()
    con.close()


def browse(root_key: str, sub: str = "", fname: str = ""):
    """Naviga cartelle ETG approvate. Sicurezza: no path traversal."""
    if root_key not in BROWSE_ROOTS:
        return {"error": "invalid root"}
    base = BROWSE_ROOTS[root_key].resolve()
    if not base.exists():
        return {"error": "root not found"}
    # Normalizza sub
    sub_norm = sub.replace("\\", "/").strip("/")
    if any(p == ".." for p in sub_norm.split("/") if p):
        return {"error": "path traversal"}
    target = (base / sub_norm).resolve() if sub_norm else base
    try:
        target.relative_to(base)
    except ValueError:
        return {"error": "path traversal"}
    if fname:
        if ".." in fname or "/" in fname or "\\" in fname:
            return {"error": "invalid filename"}
        fp = (target / fname).resolve()
        try:
            fp.relative_to(base)
        except ValueError:
            return {"error": "path traversal"}
        if not fp.is_file():
            return {"error": "not found"}
        try:
            content = fp.read_text(encoding="utf-8")
        except Exception:
            content = fp.read_text(encoding="latin-1", errors="replace")
        return {"content": content}
    if not target.is_dir():
        return {"error": "not a directory"}
    EXTS = {".md", ".txt", ".py", ".json", ".html"}
    files = sorted(f.name for f in target.iterdir() if f.is_file() and f.suffix in EXTS)
    dirs  = sorted(d.name for d in target.iterdir() if d.is_dir() and not d.name.startswith("."))
    return {"root": root_key, "sub": sub_norm, "files": files, "dirs": dirs}


# ── Handler HTTP ──────────────────────────────────────────────────────────────

class ETGHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # silenzia i log di accesso HTTP

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html: str):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/":
            self.send_html(render_html())

        elif path == "/api/data":
            self.send_json({
                "sessions":     get_sessions(),
                "inbox":        get_inbox_counts(),
                "scambio_files": get_scambio_files(),
                "bootloaders":  get_bootloaders(),
                "agents":       get_agent_activity(),
                "for_notaio":   get_for_notaio(),
                "output_files": get_output_files(),
                "timestamp":    datetime.now().isoformat(),
            })

        elif path == "/api/file":
            fname = qs.get("f", [""])[0]
            if not fname or "/" in fname or "\\" in fname or ".." in fname:
                self.send_json({"error": "invalid"}, 400)
                return
            fpath = SCAMBIO / fname
            if not fpath.exists() or not fpath.is_file():
                self.send_json({"error": "not found"}, 404)
                return
            content = fpath.read_text(encoding="utf-8")
            self.send_json({"content": content, "mtime": fpath.stat().st_mtime})

        elif path == "/api/bootloader":
            fname = qs.get("f", [""])[0]
            if not fname or "/" in fname or "\\" in fname or ".." in fname:
                self.send_json({"error": "invalid"}, 400)
                return
            fpath = BOOTLOADERS / fname
            if not fpath.exists():
                self.send_json({"error": "not found"}, 404)
                return
            self.send_json({"content": fpath.read_text(encoding="utf-8")})

        elif path == "/api/progress":
            self.send_json(get_progress())

        elif path == "/api/fornotaio":
            self.send_json(get_for_notaio())

        elif path == "/api/fornotaio/file":
            dname = qs.get("d", [""])[0]
            fname = qs.get("f", [""])[0]
            if not fname or "/" in fname or "\\" in fname or ".." in fname:
                self.send_json({"error": "invalid"}, 400)
                return
            if dname and ("/" in dname or "\\" in dname or ".." in dname):
                self.send_json({"error": "invalid"}, 400)
                return
            fpath = (FOR_NOTAIO / dname / fname) if dname else (FOR_NOTAIO / fname)
            if not fpath.exists() or not fpath.is_file():
                self.send_json({"error": "not found"}, 404)
                return
            self.send_json({"content": fpath.read_text(encoding="utf-8")})

        elif path == "/api/output/file":
            fname = qs.get("f", [""])[0]
            if not fname or "/" in fname or "\\" in fname or ".." in fname:
                self.send_json({"error": "invalid"}, 400)
                return
            for base_dir in [WORKSPACE / "output", SCAMBIO]:
                fpath = base_dir / fname
                if fpath.exists() and fpath.is_file():
                    self.send_json({"content": fpath.read_text(encoding="utf-8")})
                    return
            self.send_json({"error": "not found"}, 404)

        elif path == "/api/browse":
            root_key = qs.get("d", [""])[0]
            sub      = qs.get("sub", [""])[0]
            fname    = qs.get("f", [""])[0]
            result   = browse(root_key, sub, fname)
            if "error" in result:
                code = 400 if result["error"] in (
                    "invalid root", "path traversal", "invalid filename"
                ) else 404
                self.send_json(result, code)
            else:
                self.send_json(result)

        elif path == "/api/registro":
            try:
                limit = int(qs.get("n", ["40"])[0])
            except ValueError:
                limit = 40
            self.send_json({"messaggi": get_registro(limit)})

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/send":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data  = json.loads(body)
                motivo = data.get("motivo", "").strip()
                testo  = data.get("testo", "").strip()
                if not testo:
                    self.send_json({"error": "empty"}, 400)
                    return
                append_to_carlo(motivo, testo)
                logger.info(f"[CARLO.TXT] messaggio inviato — motivo: {motivo or '(nessuno)'}")
                self.send_json({"ok": True})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)

        elif self.path == "/api/registro/send":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data      = json.loads(body)
                autore    = data.get("autore", "Carlo").strip() or "Carlo"
                motivo    = data.get("motivo", "").strip()
                contenuto = data.get("contenuto", "").strip()
                if not contenuto:
                    self.send_json({"error": "empty"}, 400)
                    return
                insert_registro(autore, motivo, contenuto)
                logger.info(f"[REGISTRO] {autore} — motivo: {motivo or '(nessuno)'}")
                self.send_json({"ok": True})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)

        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# ── HTML ──────────────────────────────────────────────────────────────────────

def render_html() -> str:
    return r"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ETG Control Center</title>
<style>
:root{--bg:#0d1117;--surface:#161b22;--surface2:#1c2128;--border:#30363d;--text:#c9d1d9;--muted:#8b949e;--accent:#58a6ff;--green:#3fb950;--yellow:#d29922;--red:#f85149;--purple:#bc8cff;}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{height:100%;overflow:hidden;}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);display:flex;flex-direction:column;font-size:13px;}

/* HEADER */
header{background:var(--surface);border-bottom:1px solid var(--border);padding:7px 14px;display:flex;align-items:center;gap:16px;flex-shrink:0;}
header h1{font-size:15px;color:var(--accent);letter-spacing:.5px;}
.pipeline{font-size:12px;color:var(--muted);flex:1;text-align:center;}
.pipeline b{color:var(--accent);}
#last-refresh{font-size:10px;color:#444;}

/* LAYOUT */
.layout{display:flex;flex:1;overflow:hidden;}

/* SIDEBAR */
.sidebar{width:190px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow-y:auto;padding:8px 6px;gap:2px;}
.sb-label{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#444;padding:6px 4px 2px;}
.agent-item{display:flex;align-items:center;gap:7px;padding:3px 4px;border-radius:3px;}
.dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.dot-on{background:var(--green);box-shadow:0 0 4px var(--green);}
.dot-idle{background:#333;}
.sb-btn{display:block;width:100%;text-align:left;background:var(--surface2);border:1px solid var(--border);color:var(--text);font-size:11px;padding:4px 7px;margin-bottom:2px;cursor:pointer;border-radius:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.sb-btn:hover{background:#2d333b;border-color:var(--accent);color:var(--accent);}
.sb-btn-notaio{border-color:var(--yellow)!important;color:var(--yellow)!important;}
.sb-btn-notaio:hover{background:#2d333b;color:var(--yellow);}
.session-item{font-size:11px;padding:2px 4px;color:var(--muted);line-height:1.4;}
.inbox-row{display:flex;flex-wrap:wrap;gap:3px;padding:2px 0;}
.ib{font-size:10px;padding:1px 6px;border-radius:10px;border:1px solid var(--border);background:var(--surface2);}
.ib.has{border-color:var(--yellow);color:var(--yellow);}
.sb-empty{font-size:10px;color:#333;padding:2px 4px;}

/* MAIN */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0;}

/* TAB STRIP */
.tab-strip{background:var(--surface);border-bottom:1px solid var(--border);display:flex;flex-shrink:0;}
.tab-btn{background:none;border:none;border-bottom:2px solid transparent;color:var(--muted);font-size:13px;padding:8px 18px;cursor:pointer;transition:color .15s;}
.tab-btn:hover{color:var(--text);}
.tab-btn.active{color:var(--accent);border-bottom-color:var(--accent);}

/* TAB PANELS */
.tab-panel{display:none;flex:1;flex-direction:column;overflow:hidden;}
.tab-panel.active{display:flex;}

/* SYMBOLS */
.sym-bar{background:var(--surface);border-bottom:1px solid var(--border);padding:5px 8px;flex-shrink:0;}
.sym-label{font-size:10px;color:#444;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;}
.sym-grid{display:flex;flex-wrap:wrap;gap:3px;}
.sym-btn{background:var(--surface2);border:1px solid var(--border);color:var(--text);font-size:12px;padding:2px 6px;cursor:pointer;border-radius:3px;position:relative;font-family:monospace;line-height:1.5;}
.sym-btn:hover{background:#2d333b;border-color:var(--accent);color:var(--accent);}
.tip{display:none;position:absolute;bottom:calc(100% + 4px);left:50%;transform:translateX(-50%);background:#111;color:#ccc;font-size:10px;padding:3px 7px;white-space:nowrap;border-radius:3px;border:1px solid var(--border);z-index:50;pointer-events:none;font-family:'Segoe UI',sans-serif;}
.sym-btn:hover .tip{display:block;}

/* EDITOR */
.editor{padding:8px 10px;border-bottom:1px solid var(--border);flex-shrink:0;background:var(--bg);}
.motivo-row{display:flex;align-items:center;gap:8px;margin-bottom:6px;}
.motivo-label{font-size:11px;color:var(--muted);white-space:nowrap;}
.motivo-input{flex:1;background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:4px 8px;font-size:12px;border-radius:3px;outline:none;}
.motivo-input:focus{border-color:var(--accent);}
#compose{width:100%;background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:8px;font-size:13px;font-family:'Consolas',monospace;resize:vertical;border-radius:3px;min-height:75px;outline:none;line-height:1.5;}
#compose:focus{border-color:var(--accent);}
.send-row{display:flex;align-items:center;gap:10px;margin-top:6px;}
.btn-send{background:var(--accent);border:none;color:#000;font-size:13px;font-weight:600;padding:6px 18px;cursor:pointer;border-radius:4px;flex-shrink:0;}
.btn-send:hover{opacity:.85;}
#status{font-size:11px;color:var(--muted);}
.s-ok{color:var(--green)!important;}
.s-err{color:var(--red)!important;}

/* HISTORY */
.history{flex:1;display:flex;flex-direction:column;overflow:hidden;padding:6px 10px 8px;}
.history-hdr{display:flex;align-items:baseline;gap:10px;margin-bottom:4px;flex-shrink:0;}
.history-hdr h4{font-size:12px;color:var(--accent);}
.history-ts{font-size:10px;color:#444;}
#history-box{flex:1;overflow-y:auto;background:#0a0e13;border:1px solid var(--border);padding:8px 10px;font-family:'Consolas',monospace;font-size:12px;white-space:pre-wrap;word-break:break-word;border-radius:3px;line-height:1.5;}

/* PROGRESS TAB */
.chain-row{display:flex;align-items:flex-start;gap:6px;padding:14px;flex-wrap:wrap;background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0;}
.cbox{background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:7px 11px;text-align:center;min-width:58px;}
.cbox.ok{border-color:var(--green);}
.cbox.warn{border-color:var(--yellow);}
.cbox.pending{border-color:#333;}
.cid{font-family:monospace;font-size:13px;font-weight:bold;}
.cid.ok{color:var(--green);}
.cid.warn{color:var(--yellow);}
.cid.pending{color:#555;}
.cdesc{font-size:10px;color:var(--muted);margin-top:3px;max-width:105px;line-height:1.3;}
.carr{color:#333;font-size:22px;align-self:center;}
.psec{padding:10px 14px;border-bottom:1px solid var(--border);overflow-y:auto;}
.psec h4{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#444;margin-bottom:6px;}
.srow{display:flex;gap:8px;align-items:center;padding:3px 0;font-size:12px;}
.badge{font-size:10px;padding:1px 7px;border-radius:10px;border:1px solid;}
.b-ok{border-color:var(--green);color:var(--green);}
.b-warn{border-color:var(--yellow);color:var(--yellow);}
.b-err{border-color:var(--red);color:var(--red);}
.b-idle{border-color:#444;color:#555;}
.trow{display:flex;gap:8px;align-items:baseline;padding:3px 0;font-size:12px;}
.palta{color:var(--red);font-size:10px;font-weight:bold;flex-shrink:0;min-width:36px;}
.pmedia{color:var(--yellow);font-size:10px;flex-shrink:0;min-width:36px;}
.twho{color:var(--muted);font-size:10px;margin-left:auto;}
#prog-tasks-wrap{flex:1;overflow-y:auto;padding:10px 14px;}
#prog-tasks-wrap h4{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#444;margin-bottom:6px;}

/* EXPLORER TAB */
.explorer{display:flex;flex:1;overflow:hidden;}
.exp-roots{width:132px;flex-shrink:0;border-right:1px solid var(--border);overflow-y:auto;padding:6px 4px;background:var(--surface);}
.exp-root-btn{display:block;width:100%;text-align:left;background:var(--surface2);border:1px solid var(--border);color:var(--muted);font-size:11px;padding:5px 8px;margin-bottom:3px;cursor:pointer;border-radius:3px;font-family:monospace;}
.exp-root-btn:hover,.exp-root-btn.sel{background:#2d333b;border-color:var(--accent);color:var(--accent);}
.exp-content{flex:1;overflow-y:auto;padding:0;}
.exp-breadcrumb{font-size:11px;color:#444;padding:5px 10px;border-bottom:1px solid var(--border);font-family:monospace;background:var(--surface);flex-shrink:0;}
.exp-list{padding:4px 6px;}
.exp-dir,.exp-file{padding:3px 8px;font-size:12px;cursor:pointer;border-radius:2px;font-family:monospace;}
.exp-dir{color:var(--accent);}
.exp-file{color:var(--muted);}
.exp-dir:hover,.exp-file:hover{background:var(--surface2);color:var(--text);}
.exp-ph{font-size:12px;color:#333;padding:20px 14px;}

/* MODAL */
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:200;align-items:center;justify-content:center;}
.overlay.open{display:flex;}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:6px;width:72%;max-height:82vh;display:flex;flex-direction:column;padding:14px 16px;}
.modal-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
.modal-title{color:var(--accent);font-size:13px;font-family:monospace;}
.modal-x{cursor:pointer;color:var(--muted);font-size:18px;line-height:1;}
.modal-x:hover{color:var(--red);}
#modal-body{overflow-y:auto;flex:1;font-family:'Consolas',monospace;font-size:12px;white-space:pre-wrap;word-break:break-word;color:var(--text);background:#0a0e13;padding:8px;border-radius:3px;line-height:1.5;}

/* REGISTRO TAB */
.reg-compose{padding:8px 10px;border-bottom:1px solid var(--border);flex-shrink:0;background:var(--bg);}
.reg-compose-row{display:flex;gap:6px;align-items:center;margin-bottom:5px;}
.reg-label{font-size:11px;color:var(--muted);white-space:nowrap;}
.reg-autore{background:var(--surface2);border:1px solid var(--border);color:var(--accent);font-size:12px;padding:3px 6px;border-radius:3px;outline:none;cursor:pointer;}
.reg-motivo{flex:1;background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:4px 8px;font-size:12px;border-radius:3px;outline:none;}
.reg-motivo:focus{border-color:var(--accent);}
#reg-compose{width:100%;background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:8px;font-size:13px;font-family:'Consolas',monospace;resize:vertical;border-radius:3px;min-height:60px;outline:none;line-height:1.5;}
#reg-compose:focus{border-color:var(--accent);}
.reg-send-row{display:flex;align-items:center;gap:10px;margin-top:5px;}
#reg-status{font-size:11px;color:var(--muted);}
.reg-messages{flex:1;overflow-y:auto;padding:6px 10px 8px;display:flex;flex-direction:column;gap:6px;}
.reg-msg{background:var(--surface);border:1px solid var(--border);border-radius:4px;overflow:hidden;}
.reg-msg-hdr{display:flex;gap:10px;align-items:baseline;padding:4px 9px;font-size:11px;background:var(--surface2);border-bottom:1px solid var(--border);}
.reg-autore-tag{font-weight:bold;font-size:12px;}
.a-Carlo{color:#ffa657;}
.a-Gemini{color:var(--purple);}
.a-Sonnet{color:var(--accent);}
.a-Opus{color:var(--green);}
.a-UNKNOWN{color:var(--muted);}
.reg-msg-data{color:#444;font-size:10px;}
.reg-msg-motivo{color:var(--muted);font-style:italic;font-size:10px;margin-left:auto;}
.reg-msg-body{padding:6px 9px;font-family:'Consolas',monospace;font-size:12px;white-space:pre-wrap;word-break:break-word;line-height:1.5;color:var(--text);}
.reg-empty{color:#333;font-size:12px;padding:20px;text-align:center;}
.reg-ts{font-size:10px;color:#333;text-align:right;padding:2px 10px;}
</style>
</head>
<body>

<header>
  <h1>ETG Control Center</h1>
  <div class="pipeline">
    <b>Gemini</b> &rarr; <b>Sonnet</b> &rarr; [<b>Carlo</b>] &rarr; <b>Opus</b>
  </div>
  <div id="last-refresh"></div>
</header>

<div class="layout">

  <!-- ── SIDEBAR ── -->
  <div class="sidebar">
    <div class="sb-label">Agenti</div>
    <div class="agent-item"><div class="dot dot-idle" id="dot-gemini"></div> Gemini</div>
    <div class="agent-item"><div class="dot dot-on"   id="dot-sonnet"></div> Sonnet</div>
    <div class="agent-item"><div class="dot dot-idle" id="dot-opus"></div>   Opus</div>

    <div class="sb-label">Inbox</div>
    <div class="inbox-row" id="inbox-row"></div>

    <div class="sb-label">Per Notaio &#9203;</div>
    <div id="fn-list"></div>

    <div class="sb-label">Output Agenti</div>
    <div id="out-list"></div>

    <div class="sb-label">Scambio</div>
    <div id="scambio-list"></div>

    <div class="sb-label">Bootloader</div>
    <div id="boot-list"></div>

    <div class="sb-label">Sessioni</div>
    <div id="sess-list"></div>
  </div>

  <!-- ── MAIN ── -->
  <div class="main">

    <!-- Tab strip -->
    <div class="tab-strip">
      <button class="tab-btn active" id="tbtn-editor"    onclick="showTab('editor')">&#9998; Editor</button>
      <button class="tab-btn"        id="tbtn-registro"  onclick="showTab('registro')">&#128196; Registro DB</button>
      <button class="tab-btn"        id="tbtn-progresso" onclick="showTab('progresso')">&#128202; Progresso</button>
      <button class="tab-btn"        id="tbtn-esplora"   onclick="showTab('esplora')">&#128193; Esplora</button>
    </div>

    <!-- TAB: Editor -->
    <div class="tab-panel active" id="tab-editor">
      <div class="sym-bar">
        <div class="sym-label">Vocabolario ETG &mdash; clicca per inserire</div>
        <div class="sym-grid" id="sym-grid"></div>
      </div>
      <div class="editor">
        <div class="motivo-row">
          <span class="motivo-label">Motivo:</span>
          <input class="motivo-input" type="text" id="motivo" placeholder="tema / ragione del messaggio">
        </div>
        <textarea id="compose" placeholder="Scrivi il messaggio per gli agenti..."></textarea>
        <div class="send-row">
          <button class="btn-send" onclick="sendMsg()">Invia a Carlo.txt</button>
          <span id="status">Pronto</span>
        </div>
      </div>
      <div class="history">
        <div class="history-hdr">
          <h4>&#9733; Carlo.txt &mdash; Comunicazione Multi-Agente</h4>
          <span class="history-ts" id="h-ts">auto-refresh 5s</span>
        </div>
        <div id="history-box"></div>
      </div>
    </div>

    <!-- TAB: Registro DB -->
    <div class="tab-panel" id="tab-registro">
      <div class="reg-compose">
        <div class="reg-compose-row">
          <span class="reg-label">Da:</span>
          <select class="reg-autore" id="reg-autore">
            <option value="Carlo">Carlo</option>
            <option value="Sonnet">Sonnet</option>
            <option value="Gemini">Gemini</option>
            <option value="Opus">Opus</option>
          </select>
          <span class="reg-label">Motivo:</span>
          <input class="reg-motivo" type="text" id="reg-motivo" placeholder="tema / ragione">
        </div>
        <textarea id="reg-compose" placeholder="Scrivi messaggio per il registro ETG..."></textarea>
        <div class="reg-send-row">
          <button class="btn-send" onclick="sendRegistro()">Invia al Registro DB</button>
          <span id="reg-status">Pronto</span>
          <span class="reg-ts" id="reg-ts"></span>
        </div>
      </div>
      <div class="reg-messages" id="reg-messages">
        <div class="reg-empty">Caricamento registro...</div>
      </div>
    </div>

    <!-- TAB: Progresso -->
    <div class="tab-panel" id="tab-progresso">
      <div class="chain-row" id="chain-display"></div>
      <div class="psec" style="flex-shrink:0">
        <h4>Lab Sessions</h4>
        <div id="prog-sessions"></div>
      </div>
      <div id="prog-tasks-wrap">
        <h4>Task Aperti</h4>
        <div id="prog-tasks"></div>
      </div>
    </div>

    <!-- TAB: Esplora -->
    <div class="tab-panel" id="tab-esplora">
      <div class="explorer">
        <div class="exp-roots" id="exp-roots"></div>
        <div class="exp-content" id="exp-content">
          <div class="exp-ph">Seleziona una cartella a sinistra</div>
        </div>
      </div>
    </div>

  </div><!-- /main -->
</div><!-- /layout -->

<!-- Modal file viewer -->
<div class="overlay" id="overlay" onclick="maybeClose(event)">
  <div class="modal">
    <div class="modal-hdr">
      <span class="modal-title" id="modal-title"></span>
      <span class="modal-x" onclick="closeModal()">&#10005;</span>
    </div>
    <div id="modal-body"></div>
  </div>
</div>

<script>
// ── Simboli ETG ───────────────────────────────────────────────────────────────
const SYMS = [
  ['S','Sorgente pre-sintattica'],['U','Unit\u00e0 Umana'],['U\u2080','Parte fissa di U (neurologia)'],
  ['Um','Parte plastica di U (linguaggio)'],['C','Asse Sintattico'],['Cm','Asse Meta (struttura logica)'],
  ['Cer','Canale Inter'],['Cra','Canale Intra'],['C\u207B','Porzione intra di C'],
  ['D','Piano Disciplinare'],['\u03b5','Evento attraversamento'],['MA','Soglia minima distinguibilit\u00e0'],
  ['\u03c3','Stato Locale'],['DH','Gradiente Tenuta (bit)'],['\u0394','Scarto (portata vs attuabilit\u00e0)'],
  ['V','Operatore di Valore'],['A','Operatore di Azione'],['\u2113','Unit\u00e0 minima stabilizzazione'],
  ['L','Dominio di stabilizzazione'],['L\u207B','Sotto-stabilizzazione'],['L\u0336','L Tratteggiata (oltre MA)'],
  ['CU','Unit\u00e0 di Collocamento'],['\u03a3_CU','Linguaggio Aggregato di CU'],
  ['K\u2080','Commutatore Intra (senza costo)'],['K\u209c','Commutatore Inter (con costo)'],
  ['Q','Traiettoria (ex post)'],['H_C','Dispersione Sintattica (Shannon)'],
  ['Z_C','Impedenza Sintattica'],['F_C','Operatore Metrico (Fisher)'],
  ['\u29bf','Marcatore di Fissazione'],['\u03bc','Marcatore Intra in U\u2080'],["\u03bc'","Rielaborazione interna \u03bc"],
  ["\u2113'","Unit\u00e0 riemergente inter"],['\u16c6','Thurisaz — Lemma Umano'],
  ['NI_t','Non-incontro temporaneo'],['NI_tP','Non-incontro permanente'],
  ['R_i','Risonanza Instabile'],['V_p','Valenza Patologica'],['A_t','Attuabilit\u00e0 Triviale'],
  ['N_s','Rumore Sintattico'],['\u03a3','Saturazione Canale'],
];
const grid = document.getElementById('sym-grid');
SYMS.forEach(([sym, tip]) => {
  const btn = document.createElement('button');
  btn.className = 'sym-btn';
  btn.innerHTML = esc(sym) + '<span class="tip">' + esc(tip) + '</span>';
  btn.addEventListener('click', () => insertSym(sym));
  grid.appendChild(btn);
});
function insertSym(sym) {
  const ta = document.getElementById('compose');
  const s = ta.selectionStart, e = ta.selectionEnd;
  ta.value = ta.value.slice(0,s) + sym + ta.value.slice(e);
  ta.selectionStart = ta.selectionEnd = s + sym.length;
  ta.focus();
}

// ── Tab system ────────────────────────────────────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  document.getElementById('tbtn-' + name).classList.add('active');
  if (name === 'progresso') loadProgress();
  if (name === 'esplora') initExplorer();
  if (name === 'registro') loadRegistro(true);
}

// ── Invio messaggio ───────────────────────────────────────────────────────────
async function sendMsg() {
  const motivo = document.getElementById('motivo').value.trim();
  const testo  = document.getElementById('compose').value.trim();
  if (!testo) { setStatus('Nessun testo','err'); return; }
  setStatus('Invio\u2026','');
  try {
    const r = await fetch('/api/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({motivo,testo})});
    if (r.ok) {
      document.getElementById('compose').value='';
      document.getElementById('motivo').value='';
      setStatus('Dispaccio inviato \u2713','ok');
      await loadHistory(true);
    } else { setStatus('Errore invio','err'); }
  } catch(e) { setStatus('Errore: '+e.message,'err'); }
}

// ── Storico Carlo.txt ─────────────────────────────────────────────────────────
let lastMtime = 0;
async function loadHistory(force) {
  try {
    const r = await fetch('/api/file?f=Carlo.txt');
    if (!r.ok) return;
    const d = await r.json();
    if (force || d.mtime !== lastMtime) {
      lastMtime = d.mtime;
      const box = document.getElementById('history-box');
      const atBot = box.scrollHeight - box.scrollTop <= box.clientHeight + 60;
      box.textContent = d.content;
      if (atBot || force) box.scrollTop = box.scrollHeight;
      document.getElementById('h-ts').textContent = 'aggiornato: ' + new Date().toLocaleTimeString('it-IT');
    }
  } catch(e) {}
}

// ── Dati sidebar ──────────────────────────────────────────────────────────────
async function loadData() {
  try {
    const r = await fetch('/api/data');
    if (!r.ok) return;
    const d = await r.json();

    setDot('dot-gemini', d.agents.gemini);
    setDot('dot-sonnet', d.agents.sonnet);
    setDot('dot-opus',   d.agents.opus);

    document.getElementById('inbox-row').innerHTML =
      Object.entries(d.inbox).map(([k,v]) =>
        `<span class="ib${v>0?' has':''}">${k}:${v}</span>`
      ).join('');

    // Per Notaio
    document.getElementById('fn-list').innerHTML = d.for_notaio.length
      ? d.for_notaio.map(item =>
          `<button class="sb-btn sb-btn-notaio" title="${esc(item.dir)}" onclick="showForNotaio('${esc(item.dir)}','${esc(item.file)}')">${esc(item.dir || item.file)}</button>`
        ).join('')
      : '<div class="sb-empty">\u2014</div>';

    // Output Agenti
    document.getElementById('out-list').innerHTML = d.output_files.length
      ? d.output_files.map(f =>
          `<button class="sb-btn" onclick="showOutput('${esc(f.file)}')">${esc(f.file.replace('AGENTE_','').replace('.md',''))}</button>`
        ).join('')
      : '<div class="sb-empty">\u2014</div>';

    document.getElementById('scambio-list').innerHTML =
      d.scambio_files.map(f =>
        `<button class="sb-btn" title="${esc(f)}" onclick="showFile('${esc(f)}')">${esc(f)}</button>`
      ).join('');

    document.getElementById('boot-list').innerHTML =
      d.bootloaders.map(f => {
        const label = f.replace('BOOTLOADER_','').replace('.md','');
        return `<button class="sb-btn" onclick="showBoot('${esc(f)}')">${esc(label)}</button>`;
      }).join('');

    document.getElementById('sess-list').innerHTML =
      d.sessions.slice(0,6).map(s => {
        const id  = (s.session_id||'').slice(0,8);
        const st  = s.status||'';
        const cls = st==='certified'?'badge-ok':st.includes('fail')?'s-err':st.includes('revision')?'badge-warn':'';
        return `<div class="session-item"><span style="color:var(--accent)">${esc(id)}</span> ${esc(s.project_name||'')} <span class="${cls}">[${esc(st)}]</span></div>`;
      }).join('');

    document.getElementById('last-refresh').textContent = 'refresh: ' + new Date().toLocaleTimeString('it-IT');
  } catch(e) {}
}

function setDot(id, active) {
  const el = document.getElementById(id);
  if (el) el.className = 'dot ' + (active ? 'dot-on' : 'dot-idle');
}

// ── Progress tab ──────────────────────────────────────────────────────────────
let progressLoaded = false;
async function loadProgress() {
  try {
    const d = await fetch('/api/progress').then(r => r.json());
    // Chain
    document.getElementById('chain-display').innerHTML =
      d.chain.map((c, i) =>
        (i ? '<span class="carr">\u2192</span>' : '') +
        `<div class="cbox ${c.st}"><div class="cid ${c.st}">${esc(c.id)}</div><div class="cdesc">${esc(c.desc)}</div></div>`
      ).join('');
    // Sessions
    const sbmap = {ok:'b-ok',final:'b-ok',notaio:'b-ok',progress:'b-warn',warn:'b-warn',abandoned:'b-err',pending:'b-idle'};
    document.getElementById('prog-sessions').innerHTML =
      d.sessions.map(s =>
        `<div class="srow"><span>${esc(s.name)}</span><span class="badge ${sbmap[s.status]||'b-idle'}">${esc(s.status)}</span></div>`
      ).join('') || '<div style="color:#444;font-size:11px">Nessuna sessione trovata</div>';
    // Tasks
    document.getElementById('prog-tasks').innerHTML =
      d.tasks.map(t =>
        `<div class="trow"><span class="${t.p==='ALTA'?'palta':'pmedia'}">${esc(t.p)}</span><span>${esc(t.text)}</span><span class="twho">${esc(t.who)}</span></div>`
      ).join('');
    progressLoaded = true;
  } catch(e) {}
}

// ── Explorer tab ──────────────────────────────────────────────────────────────
const EROOTS = ['ClaudeETG','ETG_G','ETG_P','lab','bootloaders'];
let explorerInited = false;

function initExplorer() {
  if (explorerInited) return;
  explorerInited = true;
  document.getElementById('exp-roots').innerHTML =
    EROOTS.map(r =>
      `<button class="exp-root-btn" data-root="${esc(r)}" onclick="loadBrowse('${esc(r)}','')">${esc(r)}</button>`
    ).join('');
}

async function loadBrowse(root, sub) {
  document.querySelectorAll('.exp-root-btn').forEach(b =>
    b.classList.toggle('sel', b.dataset.root === root));
  try {
    const params = new URLSearchParams({d: root, sub: sub});
    const d = await fetch('/api/browse?' + params).then(r => r.json());
    if (d.error) {
      setExpContent(`<div class="exp-ph" style="color:var(--red)">${esc(d.error)}</div>`);
      return;
    }
    const crumb = sub ? root + '/' + sub : root;
    let html = `<div class="exp-breadcrumb">${esc(crumb)}/</div><div class="exp-list">`;
    if (sub) {
      const parentSub = sub.includes('/') ? sub.slice(0, sub.lastIndexOf('/')) : '';
      html += `<div class="exp-dir" data-root="${esc(root)}" data-sub="${esc(parentSub)}" data-file="">\u2b06 ..</div>`;
    }
    d.dirs.forEach(dir => {
      const ns = sub ? sub + '/' + dir : dir;
      html += `<div class="exp-dir" data-root="${esc(root)}" data-sub="${esc(ns)}" data-file="">${esc(dir)}/</div>`;
    });
    d.files.forEach(f => {
      html += `<div class="exp-file" data-root="${esc(root)}" data-sub="${esc(sub)}" data-file="${esc(f)}">${esc(f)}</div>`;
    });
    html += '</div>';
    setExpContent(html);
  } catch(e) {
    setExpContent('<div class="exp-ph" style="color:var(--red)">Errore di navigazione</div>');
  }
}

function setExpContent(html) {
  const el = document.getElementById('exp-content');
  el.innerHTML = html;
}

// Click delegation in explorer
document.addEventListener('click', async e => {
  const el = e.target.closest('[data-root]');
  if (!el || !el.closest('#exp-content')) return;
  const {root, sub, file} = el.dataset;
  if (!root && root !== '') return;
  if (file) {
    const params = new URLSearchParams({d: root, sub: sub, f: file});
    const d = await fetch('/api/browse?' + params).then(r => r.json());
    if (d.content !== undefined) openModal(file, d.content);
  } else if (root) {
    loadBrowse(root, sub);
  }
});

// ── File viewers ──────────────────────────────────────────────────────────────
async function showFile(fname) {
  const r = await fetch('/api/file?f=' + encodeURIComponent(fname));
  if (!r.ok) return;
  const d = await r.json();
  openModal(fname, d.content);
}
async function showBoot(fname) {
  const r = await fetch('/api/bootloader?f=' + encodeURIComponent(fname));
  if (!r.ok) return;
  const d = await r.json();
  openModal(fname, d.content);
}
async function showForNotaio(dir, fname) {
  const r = await fetch(`/api/fornotaio/file?d=${encodeURIComponent(dir)}&f=${encodeURIComponent(fname)}`);
  if (!r.ok) return;
  const d = await r.json();
  openModal((dir ? dir + '/' : '') + fname, d.content);
}
async function showOutput(fname) {
  const r = await fetch(`/api/output/file?f=${encodeURIComponent(fname)}`);
  if (!r.ok) return;
  const d = await r.json();
  openModal(fname, d.content);
}

// ── Modal ─────────────────────────────────────────────────────────────────────
function openModal(title, content) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').textContent = content;
  document.getElementById('overlay').classList.add('open');
}
function closeModal() {
  document.getElementById('overlay').classList.remove('open');
}
function maybeClose(e) {
  if (e.target === document.getElementById('overlay')) closeModal();
}

// ── Utilities ─────────────────────────────────────────────────────────────────
function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
                  .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
function setStatus(msg, type) {
  const el = document.getElementById('status');
  el.textContent = msg;
  el.className = type==='ok'?'s-ok':type==='err'?'s-err':'';
}

// ── Registro DB ───────────────────────────────────────────────────────────────
const AUTORE_COLORS = {Carlo:'a-Carlo', Gemini:'a-Gemini', Sonnet:'a-Sonnet', Opus:'a-Opus'};
let lastRegCount = 0;

async function loadRegistro(force) {
  try {
    const r = await fetch('/api/registro?n=60');
    if (!r.ok) return;
    const d = await r.json();
    const msgs = d.messaggi || [];
    if (!force && msgs.length === lastRegCount) return;
    lastRegCount = msgs.length;
    const box = document.getElementById('reg-messages');
    if (!msgs.length) {
      box.innerHTML = '<div class="reg-empty">Nessun messaggio nel registro.</div>';
      return;
    }
    const atBot = box.scrollHeight - box.scrollTop <= box.clientHeight + 80;
    box.innerHTML = msgs.map(m => {
      const col = AUTORE_COLORS[m.autore] || 'a-UNKNOWN';
      return `<div class="reg-msg">
        <div class="reg-msg-hdr">
          <span class="reg-autore-tag ${col}">${esc(m.autore)}</span>
          <span class="reg-msg-data">${esc(m.data_ora||'')}</span>
          ${m.motivo ? `<span class="reg-msg-motivo">${esc(m.motivo)}</span>` : ''}
        </div>
        <div class="reg-msg-body">${esc(m.contenuto||'')}</div>
      </div>`;
    }).join('');
    document.getElementById('reg-ts').textContent = 'aggiornato: ' + new Date().toLocaleTimeString('it-IT');
    if (atBot || force) box.scrollTop = box.scrollHeight;
  } catch(e) {}
}

async function sendRegistro() {
  const autore   = document.getElementById('reg-autore').value;
  const motivo   = document.getElementById('reg-motivo').value.trim();
  const contenuto = document.getElementById('reg-compose').value.trim();
  if (!contenuto) { setRegStatus('Nessun testo','err'); return; }
  setRegStatus('Invio\u2026','');
  try {
    const r = await fetch('/api/registro/send', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({autore, motivo, contenuto})
    });
    if (r.ok) {
      document.getElementById('reg-compose').value = '';
      document.getElementById('reg-motivo').value = '';
      setRegStatus('Messaggio registrato \u2713', 'ok');
      await loadRegistro(true);
    } else { setRegStatus('Errore invio','err'); }
  } catch(e) { setRegStatus('Errore: '+e.message,'err'); }
}

function setRegStatus(msg, type) {
  const el = document.getElementById('reg-status');
  el.textContent = msg;
  el.className = type==='ok'?'s-ok':type==='err'?'s-err':'';
}

// Ctrl+Enter anche nel registro
document.getElementById('reg-compose').addEventListener('keydown', e => {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); sendRegistro(); }
});

// ── Polling ───────────────────────────────────────────────────────────────────
loadHistory(true);
loadData();
setInterval(() => loadHistory(false), 5000);
setInterval(loadData, 15000);
setInterval(() => {
  if (document.getElementById('tab-registro').classList.contains('active')) loadRegistro(false);
}, 10000);

// Ctrl+Enter invia
document.getElementById('compose').addEventListener('keydown', e => {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); sendMsg(); }
});
</script>
</body>
</html>"""


# ── Apertura browser in modalità app ─────────────────────────────────────────

def open_app_browser(url: str):
    """
    Apre la dashboard in una finestra Chrome/Edge senza barra indirizzi né menu.
    --app=URL crea una finestra "app" pulita (solo la pagina + status bar).
    Fallback: browser di sistema se Chrome/Edge non trovato.
    """
    candidates = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for exe in candidates:
        if Path(exe).exists():
            subprocess.Popen([exe, f"--app={url}", "--window-size=1400,900", "--window-position=60,40"])
            logger.info(f"Browser app mode: {Path(exe).name}")
            return
    logger.info("Browser app mode non disponibile — apertura browser di sistema")
    webbrowser.open(url)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    server = HTTPServer(("127.0.0.1", PORT), ETGHandler)
    url = f"http://localhost:{PORT}"
    logger.info(f"ETG Control Center v2 → {url}")
    logger.info(f"Workspace : {WORKSPACE}")
    logger.info(f"Carlo.txt : {CARLO_TXT}")
    logger.info("Ctrl+C per fermare")
    threading.Timer(1.0, lambda: open_app_browser(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server fermato.")


if __name__ == "__main__":
    main()
