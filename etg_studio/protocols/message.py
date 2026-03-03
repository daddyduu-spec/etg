"""
ETG Studio - Protocollo di comunicazione tra agenti AI
Ogni messaggio è un file JSON nella inbox dell'agente destinatario.
"""

import json
import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, Any
from pathlib import Path
from enum import Enum


class MessageStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CERTIFIED = "certified"
    REJECTED = "rejected"       # Notaio ha rifiutato: Claude deve riassemblare
    REVISION_REQUESTED = "revision_requested"


class MessageType(str, Enum):
    TASK = "task"
    RESULT = "result"
    REVIEW = "review"
    CERTIFICATION = "certification"
    ERROR = "error"
    HANDOFF = "handoff"
    CARLO_CHECKPOINT = "carlo_checkpoint"  # pausa obbligatoria per Carlo (DH_ext)


class AgentRole(str, Enum):
    GEMINI = "gemini"           # progettista_laboratorio (Antigravity)
    SONNET = "sonnet"           # assemblatore/revisore CLI (Claude Sonnet)
    OPUS = "opus"               # notaio (Claude Opus — interattivo, non automatizzabile)
    CARLO = "carlo"             # DH_ext umano — checkpoint obbligatorio (Eq. 14)
    ORCHESTRATOR = "orchestrator"
    # Deprecato — ChatGPT rimosso dalla catena notarile (27/02/2026)
    CLAUDE = "claude"           # alias legacy per SONNET
    CHATGPT = "chatgpt"         # fuori catena — advisor esterno


@dataclass
class ETGMessage:
    """Messaggio standard tra agenti nel sistema ETG Studio."""

    # Identità
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    project_name: str = ""

    # Routing
    sender: str = ""            # AgentRole
    recipient: str = ""         # AgentRole
    msg_type: str = MessageType.TASK

    # Contenuto
    subject: str = ""
    payload: dict = field(default_factory=dict)
    attachments: list = field(default_factory=list)  # percorsi file allegati

    # Workflow
    status: str = MessageStatus.PENDING
    priority: int = 1           # 1=normale, 2=urgente, 3=critico
    depends_on: Optional[str] = None  # msg_id del messaggio precedente

    # Metadati
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    processed_at: Optional[str] = None
    etg_path: str = ""          # percorso cartella ETG condivisa

    # Audit (usato dal Notaio)
    certification_hash: Optional[str] = None
    certified_by: Optional[str] = None
    certified_at: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, data: str) -> "ETGMessage":
        return cls(**json.loads(data))

    @classmethod
    def from_file(cls, path: Path) -> "ETGMessage":
        return cls.from_json(path.read_text(encoding="utf-8"))

    def save_to_inbox(self, inbox_path: Path) -> Path:
        """Salva il messaggio nella inbox del destinatario."""
        inbox_path.mkdir(parents=True, exist_ok=True)
        filename = f"{self.priority}_{self.created_at[:19].replace(':', '-')}_{self.msg_id[:8]}.json"
        filepath = inbox_path / filename
        filepath.write_text(self.to_json(), encoding="utf-8")
        return filepath

    def mark_processed(self, status: MessageStatus = MessageStatus.COMPLETED):
        self.processed_at = datetime.now().isoformat()
        self.status = status


@dataclass
class ETGSession:
    """Sessione di lavoro condivisa tra tutti gli agenti."""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_name: str = ""
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "active"

    # Tracciamento workflow
    current_agent: str = AgentRole.GEMINI
    completed_agents: list = field(default_factory=list)
    message_chain: list = field(default_factory=list)  # lista msg_id in ordine

    # Output finali
    gemini_output: Optional[str] = None    # percorso file specifiche (Gemini)
    sonnet_output: Optional[str] = None    # percorso file assemblato (Sonnet-CLI)
    opus_output: Optional[str] = None      # percorso certificazione notarile (Opus)
    final_etg_path: Optional[str] = None  # destinazione ETG
    # Legacy
    claude_output: Optional[str] = None    # alias di sonnet_output
    chatgpt_output: Optional[str] = None  # deprecato

    # Retry loop (Notaio -> Claude)
    retry_count: int = 0
    max_retries: int = 3
    last_audit_notes: Optional[str] = None   # feedback del Notaio a Claude
    last_rejection_reason: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, data: str) -> "ETGSession":
        return cls(**json.loads(data))

    def save(self, sessions_path: Path) -> Path:
        sessions_path.mkdir(parents=True, exist_ok=True)
        filepath = sessions_path / f"session_{self.session_id[:8]}.json"
        filepath.write_text(self.to_json(), encoding="utf-8")
        return filepath
