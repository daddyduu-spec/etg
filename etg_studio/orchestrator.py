"""
ETG Studio - Orchestratore principale
Catena notarile vigente (27/02/2026):
    Gemini (Progettista) → Sonnet-CLI (Assemblatore) → [CARLO checkpoint] → Opus (Notaio) → Carlo (certificazione)

VINCOLO OBBLIGATORIO: Carlo è il DH_ext (Eq. 14 ETG).
Senza relay umano Carlo, AI↔AI = allucinazione garantita.
ChatGPT è fuori dalla catena — advisor esterno.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

import yaml

# Aggiunge il path del progetto
sys.path.insert(0, str(Path(__file__).parent))

import agents as agents_module  # lazy imports per GeminiAgent, ClaudeAgent, ChatGPTAgent
from agents.mock_agents import MockGeminiAgent, MockClaudeAgent, MockChatGPTAgent
from protocols import ETGMessage, ETGSession, MessageType, AgentRole

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger("orchestrator")


class ETGOrchestrator:
    """
    Orchestratore del sistema multi-AI ETG Studio.

    Gestisce il ciclo di vita di ogni progetto:
    Brief → Gemini → Claude → ChatGPT → Certificato ETG
    """

    def __init__(self, config_path: str = "config/config.yaml", demo: bool = False):
        # Risolve i path relativi rispetto alla directory dello script
        self._script_dir = Path(__file__).parent
        self.config = self._load_config(config_path)
        workspace_rel = Path(self.config["etg_studio"]["workspace"])
        self.workspace = (self._script_dir / workspace_rel).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.demo = demo

        # Inizializza gli agenti (mock in demo mode)
        if demo:
            self.agents = self._init_mock_agents()
            logger.info("MODALITA DEMO - agenti simulati attivi.")
        else:
            self.agents = self._init_agents()

        # Inbox dell'orchestratore (notifiche di completamento)
        self.inbox = self.workspace / "inbox" / "orchestrator"
        self.inbox.mkdir(parents=True, exist_ok=True)

        logger.info("ETG Studio Orchestratore avviato.")
        logger.info(f"Workspace: {self.workspace.resolve()}")

    def _load_config(self, path: str) -> dict:
        resolved = self._script_dir / path
        with open(resolved, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _init_agents(self) -> dict:
        """Inizializza gli agenti AI con le rispettive API key."""
        agents_config = self.config["agents"]

        # Legge le API key dalle variabili d'ambiente
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        openai_key = os.environ.get("OPENAI_API_KEY", "")
        google_key = os.environ.get("GOOGLE_AI_API_KEY", "")

        agents = {}

        if google_key:
            agents[AgentRole.GEMINI] = agents_module.GeminiAgent(
                config=agents_config["gemini"],
                workspace_path=self.workspace,
                api_key=google_key,
            )
            logger.info("Agente GEMINI (Progettista) inizializzato.")

        if anthropic_key:
            # Sonnet-CLI = assemblatore automatico
            agents[AgentRole.SONNET] = agents_module.ClaudeAgent(
                config=agents_config.get("sonnet", agents_config.get("claude")),
                workspace_path=self.workspace,
                api_key=anthropic_key,
            )
            logger.info("Agente SONNET-CLI (Assemblatore) inizializzato.")

        # OPUS = notaio interattivo — NON automatizzabile.
        # La notarizzazione avviene tramite Carlo (relay umano) via Carlo.txt.
        # ChatGPT = fuori dalla catena (advisor esterno). Non inizializzato.
        logger.info("NOTA: Opus (Notaio) opera in modo interattivo via Carlo. Non è un agente automatico.")

        return agents

    def _init_mock_agents(self) -> dict:
        """Inizializza agenti mock per la modalita demo."""
        agents_config = self.config["agents"]
        agents = {
            AgentRole.GEMINI: MockGeminiAgent(
                config=agents_config["gemini"],
                workspace_path=self.workspace,
            ),
            AgentRole.CLAUDE: MockClaudeAgent(
                config=agents_config["claude"],
                workspace_path=self.workspace,
            ),
            AgentRole.CHATGPT: MockChatGPTAgent(
                config=agents_config["chatgpt"],
                workspace_path=self.workspace,
            ),
        }
        logger.info("Agenti MOCK inizializzati (Gemini, Claude, ChatGPT).")
        return agents

    def start_project(
        self,
        project_name: str,
        brief: str,
        etg_path: str = "etg://shared/projects",
    ) -> str:
        """
        Avvia un nuovo progetto ETG.

        Args:
            project_name: Nome del progetto
            brief: Descrizione del progetto / brief completo
            etg_path: Percorso della cartella condivisa ETG

        Returns:
            session_id del progetto avviato
        """
        # Crea la sessione
        session = ETGSession(
            project_name=project_name,
            description=brief,
        )
        session.save(self.workspace / "sessions")

        logger.info(f"\n{'='*60}")
        logger.info(f"NUOVO PROGETTO: {project_name}")
        logger.info(f"Session ID: {session.session_id[:8]}")
        logger.info(f"ETG Path: {etg_path}")
        logger.info(f"{'='*60}")

        # Messaggio iniziale per Gemini
        initial_msg = ETGMessage(
            session_id=session.session_id,
            project_name=project_name,
            sender=AgentRole.ORCHESTRATOR,
            recipient=AgentRole.GEMINI,
            msg_type=MessageType.TASK,
            subject=f"[PROGETTO] {project_name}",
            payload={
                "brief": brief,
                "project_name": project_name,
            },
            etg_path=etg_path,
            priority=1,
        )

        # Invia a Gemini
        inbox_base = self.workspace / "inbox"
        initial_msg.save_to_inbox(inbox_base / AgentRole.GEMINI)
        logger.info(f"Progetto inviato a Gemini (Progettista).")

        return session.session_id

    def _wait_and_run_agent(self, agent, agent_role: str, timeout: int) -> bool:
        """Aspetta che l'agente abbia un messaggio e lo processa."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if agent.run_once(self.workspace / "inbox"):
                return True
            time.sleep(2)
        logger.error(f"Timeout per agente {agent_role}!")
        return False

    def run_pipeline(self, session_id: str, timeout: int = 600) -> dict:
        """
        Esegue la pipeline completa per un progetto.
        Supporta il retry loop: se ChatGPT rifiuta, Claude riassembla.
        Blocca fino al completamento o timeout.

        Returns:
            risultato con paths e stato finale
        """
        logger.info(f"\nPIPELINE AVVIATA per session: {session_id[:8]}")
        max_retries = self.config["workflow"].get("max_retries", 3)
        start_time = time.time()

        # FASE 1: Gemini (Progettista) — automatica
        if AgentRole.GEMINI in self.agents:
            logger.info(f"\n>>> GEMINI (Progettista) sta lavorando...")
            if not self._wait_and_run_agent(
                self.agents[AgentRole.GEMINI], "gemini", timeout
            ):
                return {"status": "timeout", "agent": "gemini"}
            logger.info(f"<<< GEMINI completato.")
        time.sleep(1)

        # FASE 2: Sonnet-CLI (Assemblatore) — automatica
        if AgentRole.SONNET in self.agents:
            logger.info(f"\n>>> SONNET-CLI (Assemblatore) sta lavorando...")
            if not self._wait_and_run_agent(
                self.agents[AgentRole.SONNET], "sonnet", timeout
            ):
                return {"status": "timeout", "agent": "sonnet"}
            logger.info(f"<<< SONNET-CLI completato. Output depositato in workspace/output/")
        time.sleep(1)

        # FASE 3: CHECKPOINT CARLO (DH_ext — Eq. 14 ETG)
        # Sonnet ha già scritto in Carlo.txt. La pipeline si ferma qui.
        # Carlo legge Carlo.txt, porta l'output a Opus (chat interattiva),
        # Opus certifica e scrive il verdetto in Carlo.txt.
        # La certificazione automatica NON esiste — è una violazione di Eq. 14.
        logger.info(f"\n{'='*60}")
        logger.info(f"CHECKPOINT CARLO — PIPELINE IN ATTESA")
        logger.info(f"Sonnet ha depositato l'output. Carlo deve:")
        logger.info(f"  1. Leggere Carlo.txt per vedere l'output Sonnet")
        logger.info(f"  2. Portare l'output a Opus (notaio, chat interattiva)")
        logger.info(f"  3. Opus certifica e scrive verdetto in Carlo.txt")
        logger.info(f"  4. Invocare get_final_result(session_id) per chiudere")
        logger.info(f"Session ID: {session_id[:8]}")
        logger.info(f"{'='*60}")

        return {
            "status": "awaiting_carlo_checkpoint",
            "session_id": session_id,
            "message": "Pipeline in pausa. Carlo deve portare l'output a Opus per notarizzazione.",
            "carlo_txt": str(self.workspace / "scambio" / "Carlo.txt"),
        }

    def _load_session(self, session_id: str) -> Optional[ETGSession]:
        """Carica una sessione dal disco."""
        session_file = self.workspace / "sessions" / f"session_{session_id[:8]}.json"
        if session_file.exists():
            return ETGSession.from_json(session_file.read_text(encoding="utf-8"))
        return None

    def _get_final_result(self, session_id: str) -> dict:
        """Recupera il report finale dalla sessione."""
        sessions_path = self.workspace / "sessions"
        session_file = sessions_path / f"session_{session_id[:8]}.json"

        if not session_file.exists():
            return {"status": "error", "message": "Sessione non trovata"}

        session = ETGSession.from_json(session_file.read_text(encoding="utf-8"))

        result = {
            "status": session.status,
            "session_id": session.session_id,
            "project_name": session.project_name,
            "gemini_specs": session.gemini_output,
            "claude_assembled": session.claude_output,
            "chatgpt_certified": session.chatgpt_output,
            "etg_destination": session.final_etg_path,
        }

        if session.status == "certified":
            logger.info(f"\n{'='*60}")
            logger.info(f"PROGETTO CERTIFICATO: {session.project_name}")
            logger.info(f"Certificato: {session.chatgpt_output}")
            logger.info(f"Destinazione ETG: {session.final_etg_path}")
            logger.info(f"{'='*60}\n")

        return result

    def run_daemon(self, poll_interval: int = 5):
        """
        Modalità daemon: monitora continuamente le inbox e processa messaggi.
        Utile per integrazione ETG con sync automatico.
        """
        logger.info("ETG Studio Orchestratore in modalità DAEMON.")
        logger.info("Monitoraggio inbox continuo...")

        while True:
            try:
                for role, agent in self.agents.items():
                    agent.run_once(self.workspace / "inbox")

                # Controlla inbox orchestratore per notifiche
                self._check_orchestrator_inbox()

                time.sleep(poll_interval)
            except KeyboardInterrupt:
                logger.info("Daemon fermato.")
                break
            except Exception as e:
                logger.error(f"Errore daemon: {e}")
                time.sleep(poll_interval)

    def _check_orchestrator_inbox(self):
        """Processa le notifiche di completamento."""
        for msg_path in sorted(self.inbox.glob("*.json")):
            msg = ETGMessage.from_file(msg_path)
            if msg.msg_type == MessageType.CERTIFICATION:
                esito = msg.payload.get("esito", "SCONOSCIUTO")
                logger.info(
                    f"PROGETTO COMPLETATO: {msg.project_name} | "
                    f"Esito: {esito} | "
                    f"Cert: {msg.payload.get('certified_path', 'N/A')}"
                )
                # Archivia
                archive = self.inbox / "processed"
                archive.mkdir(exist_ok=True)
                msg_path.rename(archive / msg_path.name)


# ─── Entry point CLI ────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="ETG Studio - Multi-AI Orchestrator")
    subparsers = parser.add_subparsers(dest="command")

    # Comando: avvia un progetto
    run_parser = subparsers.add_parser("run", help="Avvia un progetto ETG")
    run_parser.add_argument("--name", required=True, help="Nome del progetto")
    run_parser.add_argument("--brief", required=True, help="Brief del progetto (o path a file .txt)")
    run_parser.add_argument("--etg-path", default="etg://shared/projects", help="Cartella ETG")
    run_parser.add_argument("--timeout", type=int, default=600, help="Timeout in secondi")

    # Comando: modalità daemon
    daemon_parser = subparsers.add_parser("daemon", help="Avvia in modalità daemon")
    daemon_parser.add_argument("--poll", type=int, default=5, help="Intervallo poll (sec)")

    # Comando: demo
    demo_parser = subparsers.add_parser("demo", help="Avvia in modalita demo (senza API keys)")
    demo_parser.add_argument("--name", default="Demo ETG", help="Nome progetto demo")
    demo_parser.add_argument("--brief", default="Progetto dimostrativo ETG Studio", help="Brief demo")

    # Comando: status progetto
    status_parser = subparsers.add_parser("status", help="Stato di un progetto")
    status_parser.add_argument("--session", required=True, help="Session ID")

    # Comando: watch (watcher cartelle ETG)
    watch_parser = subparsers.add_parser("watch", help="Monitora cartelle ETG reali")
    watch_parser.add_argument("--etg-root", default=str(Path(__file__).parent.parent), help="Root ETG")
    watch_parser.add_argument("--poll", type=int, default=10, help="Intervallo poll (sec)")
    watch_parser.add_argument("--summary", action="store_true", help="Mostra sommario cartelle")

    args = parser.parse_args()

    is_demo = args.command == "demo"
    orchestrator = ETGOrchestrator(demo=is_demo)

    if args.command == "demo":
        brief = args.brief
        session_id = orchestrator.start_project(
            project_name=args.name,
            brief=brief,
            etg_path="etg://demo",
        )
        result = orchestrator.run_pipeline(session_id, timeout=60)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "watch":
        from etg_watcher import ETGWatcher
        watcher = ETGWatcher(
            etg_root=args.etg_root,
            workspace_path=orchestrator.workspace,
        )
        if args.summary:
            summary = watcher.get_summary()
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            watcher.run_daemon(poll_interval=args.poll)

    elif args.command == "run":
        # Legge il brief da file se è un path
        brief = args.brief
        if brief.endswith(".txt") and Path(brief).exists():
            brief = Path(brief).read_text(encoding="utf-8")

        session_id = orchestrator.start_project(
            project_name=args.name,
            brief=brief,
            etg_path=args.etg_path,
        )

        result = orchestrator.run_pipeline(session_id, timeout=args.timeout)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "daemon":
        orchestrator.run_daemon(poll_interval=args.poll)

    elif args.command == "status":
        result = orchestrator._get_final_result(args.session)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
