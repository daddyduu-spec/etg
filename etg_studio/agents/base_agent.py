"""
ETG Studio - Classe base per tutti gli agenti AI.
"""

import logging
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

# Garantisce che etg_studio/ sia nel path — permette import di etg_engine
# anche quando un agente viene eseguito direttamente (non via orchestrator.py)
_studio_root = Path(__file__).parent.parent
if str(_studio_root) not in sys.path:
    sys.path.insert(0, str(_studio_root))

from protocols import ETGMessage, ETGSession, MessageStatus, MessageType, AgentRole

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Agente AI base. Ogni agente legge dalla propria inbox,
    processa il task e scrive nella inbox del prossimo agente.
    """

    def __init__(self, config: dict, workspace_path: Path):
        self.config = config
        self.workspace = workspace_path
        self.role = config["role"]
        self.model = config["model"]
        # config["inbox"] e' tipo "./workspace/inbox/gemini"
        # workspace_path e' gia "./workspace", quindi estraiamo solo "inbox/gemini"
        inbox_rel = config["inbox"].replace("./workspace/", "").lstrip("./")
        self.inbox = workspace_path / inbox_rel

        self.sessions_path = workspace_path / "sessions"
        self.shared_path = workspace_path / "shared"
        self.certified_path = workspace_path / "certified"
        self.logs_path = workspace_path / "logs"

        self.inbox.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)

        self._setup_logging()

    def _setup_logging(self):
        log_file = self.logs_path / f"{self.role}.log"
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))
        logger.addHandler(handler)

    def get_pending_messages(self) -> list[Path]:
        """Legge la inbox e restituisce messaggi pendenti ordinati per priorità."""
        if not self.inbox.exists():
            return []
        files = sorted(self.inbox.glob("*.json"))
        return files

    def load_session(self, session_id: str) -> Optional[ETGSession]:
        session_file = self.sessions_path / f"session_{session_id[:8]}.json"
        if session_file.exists():
            return ETGSession.from_json(session_file.read_text(encoding="utf-8"))
        return None

    def save_session(self, session: ETGSession):
        session.save(self.sessions_path)

    def write_output(self, content: str, session: ETGSession, suffix: str) -> Path:
        """Scrive il risultato dell'agente nella cartella shared."""
        output_dir = self.shared_path / session.session_id[:8]
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{self.role}_{suffix}.md"
        filepath = output_dir / filename
        filepath.write_text(content, encoding="utf-8")
        return filepath

    def send_to(self, recipient: str, msg: ETGMessage, inbox_base: Path):
        """Invia un messaggio nella inbox del destinatario."""
        inbox = inbox_base / recipient
        filepath = msg.save_to_inbox(inbox)
        logger.info(f"[{self.role.upper()}] -> {recipient}: {msg.subject} ({filepath.name})")
        return filepath

    def archive_message(self, msg_path: Path):
        """Sposta il messaggio processato nella cartella archive."""
        archive = msg_path.parent / "processed"
        archive.mkdir(exist_ok=True)
        msg_path.rename(archive / msg_path.name)

    @abstractmethod
    def build_system_prompt(self) -> str:
        """Prompt di sistema specifico per il ruolo dell'agente."""
        pass

    @abstractmethod
    def process(self, msg: ETGMessage, session: ETGSession) -> tuple[str, ETGMessage]:
        """
        Processa un messaggio e restituisce:
        - output: il risultato del lavoro
        - next_msg: il messaggio da inviare al prossimo agente
        """
        pass

    def run_once(self, workspace_inbox: Path) -> bool:
        """Processa il primo messaggio pendente. Ritorna True se ha lavorato."""
        pending = self.get_pending_messages()
        if not pending:
            return False

        msg_path = pending[0]
        msg = ETGMessage.from_file(msg_path)
        logger.info(f"[{self.role.upper()}] Processo: {msg.subject} (session: {msg.session_id[:8]})")

        session = self.load_session(msg.session_id)
        if not session:
            logger.error(f"Sessione non trovata: {msg.session_id}")
            return False

        try:
            msg.status = MessageStatus.IN_PROGRESS
            output, next_msg = self.process(msg, session)
            msg.mark_processed(MessageStatus.COMPLETED)
            self.archive_message(msg_path)
            self.save_session(session)
            logger.info(f"[{self.role.upper()}] Completato: {msg.subject}")
            return True
        except Exception as e:
            msg.mark_processed(MessageStatus.FAILED)
            logger.error(f"[{self.role.upper()}] Errore: {e}")
            return False
