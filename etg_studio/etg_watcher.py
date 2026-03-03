"""
ETG Studio - Watcher cartelle ETG reali.
Monitora le cartelle condivise (ClaudeETG/, Gemini/, chatgpt/, ETG_G/, ETG_P/)
e notifica l'orchestratore quando ci sono nuovi file o modifiche.
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from protocols import ETGMessage, MessageType, AgentRole

logger = logging.getLogger("etg_watcher")

# Cartelle ETG reali da monitorare (relative alla root ETG)
DEFAULT_WATCHED_FOLDERS = {
    "ClaudeETG": {
        "owner": AgentRole.CLAUDE,
        "description": "Repository canonico ETG (assemblatore)",
    },
    "Gemini": {
        "owner": AgentRole.GEMINI,
        "description": "Materiale Gemini (progettista laboratorio)",
    },
    "chatgpt": {
        "owner": AgentRole.CHATGPT,
        "description": "Output ChatGPT (notaio)",
    },
    "ETG_G": {
        "owner": AgentRole.CLAUDE,
        "description": "ETG-G grammatica pura",
    },
    "ETG_P": {
        "owner": AgentRole.GEMINI,
        "description": "ETG-P parametrizzata",
    },
    "Keep": {
        "owner": AgentRole.ORCHESTRATOR,
        "description": "Documenti Keep HTML",
    },
    "manus": {
        "owner": AgentRole.ORCHESTRATOR,
        "description": "Documenti Manus",
    },
}


class FileSnapshot:
    """Snapshot di un file: path, dimensione, data modifica."""

    def __init__(self, path: Path):
        stat = path.stat()
        self.path = str(path)
        self.size = stat.st_size
        self.mtime = stat.st_mtime
        self.name = path.name

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "name": self.name,
            "size": self.size,
            "mtime": self.mtime,
        }


class ETGWatcher:
    """
    Monitora le cartelle ETG reali per cambiamenti.
    Produce notifiche nella inbox dell'orchestratore.
    """

    def __init__(
        self,
        etg_root: Path,
        workspace_path: Path,
        watched_folders: Optional[dict] = None,
    ):
        self.etg_root = Path(etg_root).resolve()
        self.workspace = Path(workspace_path)
        self.watched = watched_folders or DEFAULT_WATCHED_FOLDERS

        # Stato precedente per confronto
        self.state_file = self.workspace / "sessions" / "watcher_state.json"
        self.previous_state = self._load_state()

        self.inbox_base = self.workspace / "inbox"
        self.inbox_base.mkdir(parents=True, exist_ok=True)

        logger.info(f"ETG Watcher inizializzato. Root: {self.etg_root}")

    def _load_state(self) -> dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        return {}

    def _save_state(self, state: dict):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(
            json.dumps(state, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def scan_folder(self, folder_name: str) -> list[FileSnapshot]:
        """Scansiona una cartella ETG e ritorna gli snapshot dei file."""
        folder_path = self.etg_root / folder_name
        if not folder_path.exists():
            return []

        snapshots = []
        for fpath in folder_path.rglob("*"):
            if fpath.is_file() and not fpath.name.startswith("."):
                try:
                    snapshots.append(FileSnapshot(fpath))
                except (OSError, PermissionError):
                    continue
        return snapshots

    def detect_changes(self) -> dict:
        """
        Confronta lo stato attuale con quello precedente.
        Ritorna dict con nuovi file, modificati e rimossi per cartella.
        """
        current_state = {}
        changes = {}

        for folder_name in self.watched:
            snapshots = self.scan_folder(folder_name)
            current_state[folder_name] = {
                s.path: s.to_dict() for s in snapshots
            }

            prev = self.previous_state.get(folder_name, {})
            curr = current_state[folder_name]

            new_files = [
                curr[p] for p in curr if p not in prev
            ]
            modified_files = [
                curr[p] for p in curr
                if p in prev and curr[p]["mtime"] != prev[p]["mtime"]
            ]
            removed_files = [
                prev[p] for p in prev if p not in curr
            ]

            if new_files or modified_files or removed_files:
                changes[folder_name] = {
                    "new": new_files,
                    "modified": modified_files,
                    "removed": removed_files,
                    "owner": self.watched[folder_name]["owner"],
                }

        # Salva lo stato attuale
        self._save_state(current_state)
        self.previous_state = current_state

        return changes

    def notify_changes(self, changes: dict):
        """Invia notifiche all'orchestratore per ogni cartella con cambiamenti."""
        for folder_name, info in changes.items():
            n_new = len(info["new"])
            n_mod = len(info["modified"])
            n_rem = len(info["removed"])

            summary = []
            if n_new:
                summary.append(f"{n_new} nuovi")
            if n_mod:
                summary.append(f"{n_mod} modificati")
            if n_rem:
                summary.append(f"{n_rem} rimossi")

            msg = ETGMessage(
                project_name=f"ETG Watcher: {folder_name}",
                sender="etg_watcher",
                recipient=AgentRole.ORCHESTRATOR,
                msg_type=MessageType.TASK,
                subject=f"[WATCHER] {folder_name}: {', '.join(summary)}",
                payload={
                    "folder": folder_name,
                    "owner": info["owner"],
                    "new_files": info["new"],
                    "modified_files": info["modified"],
                    "removed_files": info["removed"],
                    "detected_at": datetime.now().isoformat(),
                },
                etg_path=f"etg://{folder_name}",
            )
            inbox = self.inbox_base / AgentRole.ORCHESTRATOR
            msg.save_to_inbox(inbox)
            logger.info(
                f"[WATCHER] {folder_name}: {', '.join(summary)}"
            )

    def run_once(self) -> dict:
        """Esegue una scansione e notifica cambiamenti."""
        changes = self.detect_changes()
        if changes:
            self.notify_changes(changes)
        return changes

    def run_daemon(self, poll_interval: int = 10):
        """Modalita daemon: monitora continuamente."""
        logger.info(f"ETG Watcher DAEMON avviato (poll: {poll_interval}s)")
        logger.info(f"Cartelle monitorate: {list(self.watched.keys())}")

        while True:
            try:
                changes = self.run_once()
                if changes:
                    for folder, info in changes.items():
                        total = (
                            len(info.get("new", []))
                            + len(info.get("modified", []))
                        )
                        if total:
                            logger.info(f"  {folder}: {total} cambiamenti")

                time.sleep(poll_interval)
            except KeyboardInterrupt:
                logger.info("Watcher fermato.")
                break
            except Exception as e:
                logger.error(f"Errore watcher: {e}")
                time.sleep(poll_interval)

    def get_summary(self) -> dict:
        """Ritorna un sommario dello stato attuale delle cartelle ETG."""
        summary = {}
        for folder_name, meta in self.watched.items():
            folder_path = self.etg_root / folder_name
            if folder_path.exists():
                files = list(folder_path.rglob("*"))
                file_count = sum(1 for f in files if f.is_file())
                summary[folder_name] = {
                    "exists": True,
                    "file_count": file_count,
                    "owner": meta["owner"],
                    "description": meta["description"],
                }
            else:
                summary[folder_name] = {
                    "exists": False,
                    "file_count": 0,
                    "owner": meta["owner"],
                    "description": meta["description"],
                }
        return summary


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    parser = argparse.ArgumentParser(description="ETG Studio - Folder Watcher")
    parser.add_argument(
        "--etg-root",
        default=str(Path(__file__).parent.parent),
        help="Root delle cartelle ETG (default: parent di etg_studio/)",
    )
    parser.add_argument(
        "--workspace",
        default="./workspace",
        help="Workspace etg_studio",
    )
    parser.add_argument(
        "--poll", type=int, default=10,
        help="Intervallo di polling in secondi",
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Esegui una sola scansione",
    )
    parser.add_argument(
        "--summary", action="store_true",
        help="Mostra sommario cartelle ETG",
    )

    args = parser.parse_args()

    watcher = ETGWatcher(
        etg_root=args.etg_root,
        workspace_path=args.workspace,
    )

    if args.summary:
        summary = watcher.get_summary()
        print("\n" + "=" * 50)
        print("ETG FOLDERS SUMMARY")
        print("=" * 50)
        for name, info in summary.items():
            status = "OK" if info["exists"] else "MANCANTE"
            print(f"  [{status}] {name:15s} | {info['file_count']:4d} files | {info['owner']}")
            print(f"           {info['description']}")
        print("=" * 50)
    elif args.once:
        changes = watcher.run_once()
        if changes:
            print(json.dumps(changes, indent=2, ensure_ascii=False, default=str))
        else:
            print("Nessun cambiamento rilevato.")
    else:
        watcher.run_daemon(poll_interval=args.poll)


if __name__ == "__main__":
    main()
