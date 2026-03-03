"""
ETG Studio - Mock Agents per modalita demo.
Funzionano senza API keys, generano risposte simulate
per testare la pipeline completa.
"""

import hashlib
import logging
from datetime import datetime
from pathlib import Path

from .base_agent import BaseAgent
from protocols import ETGMessage, ETGSession, MessageType, MessageStatus, AgentRole

logger = logging.getLogger("mock")


class MockGeminiAgent(BaseAgent):
    """Mock Gemini - genera specifiche simulate."""

    def __init__(self, config: dict, workspace_path: Path, **kwargs):
        super().__init__(config, workspace_path)

    def build_system_prompt(self) -> str:
        return "[DEMO] Gemini Mock"

    def process(self, msg: ETGMessage, session: ETGSession) -> tuple[str, ETGMessage]:
        brief = msg.payload.get("brief", "N/A")
        project_name = msg.project_name

        logger.info(f"[DEMO/GEMINI] Progettazione: {project_name}")

        output = f"""# SPECIFICHE TECNICHE [DEMO]
## Progetto: {project_name}
## Generato da: Gemini Mock (modalita demo)
## Data: {datetime.now().isoformat()}

---

### 1. ARCHITETTURA
- Componente A: gestione input
- Componente B: elaborazione
- Componente C: output/validazione

### 2. SPECIFICHE
- REQ-001: Il sistema deve accettare il brief: "{brief[:200]}"
- REQ-002: Produrre output strutturato
- REQ-003: Rispettare standard ETG

### 3. TEMPLATE STRUTTURA
```
progetto/
  src/
    main.py
    utils.py
  tests/
    test_main.py
  docs/
    README.md
```

### 4. PIANO PER CLAUDE
1. Implementa Componente A
2. Implementa Componente B
3. Integra A+B in Componente C
4. Scrivi test

### 5. CRITERI VALIDAZIONE PER NOTAIO
- [ ] Tutti i REQ implementati
- [ ] Test presenti e funzionanti
- [ ] Documentazione completa

---
*[DEMO MODE - specifiche simulate]*
"""

        output_path = self.write_output(output, session, "specifiche")
        session.gemini_output = str(output_path)
        session.current_agent = AgentRole.CLAUDE
        session.completed_agents.append(AgentRole.GEMINI)

        next_msg = ETGMessage(
            session_id=msg.session_id,
            project_name=project_name,
            sender=AgentRole.GEMINI,
            recipient=AgentRole.CLAUDE,
            msg_type=MessageType.HANDOFF,
            subject=f"[DEMO/SPECIFICHE] {project_name}",
            payload={
                "brief": brief,
                "gemini_specs_path": str(output_path),
                "gemini_output": output,
                "instructions": "[DEMO] Assembla la soluzione.",
            },
            attachments=[str(output_path)],
            etg_path=msg.etg_path,
            depends_on=msg.msg_id,
        )

        inbox_base = self.workspace / "inbox"
        self.send_to(AgentRole.CLAUDE, next_msg, inbox_base)
        return output, next_msg


class MockClaudeAgent(BaseAgent):
    """Mock Claude - genera assemblato simulato."""

    def __init__(self, config: dict, workspace_path: Path, **kwargs):
        super().__init__(config, workspace_path)

    def build_system_prompt(self) -> str:
        return "[DEMO] Claude Mock"

    def process(self, msg: ETGMessage, session: ETGSession) -> tuple[str, ETGMessage]:
        project_name = msg.project_name
        is_revision = (
            msg.sender == AgentRole.CHATGPT
            or msg.payload.get("retry_count", 0) > 0
        )

        if is_revision:
            retry = msg.payload.get("retry_count", 1)
            logger.info(f"[DEMO/CLAUDE] REVISIONE #{retry}: {project_name}")
            label = f"REVISIONE #{retry}"
        else:
            logger.info(f"[DEMO/CLAUDE] Assemblaggio: {project_name}")
            label = "ASSEMBLAGGIO"

        output = f"""# {label} [DEMO]
## Progetto: {project_name}
## Generato da: Claude Mock (modalita demo)
## Data: {datetime.now().isoformat()}

---

### Codice assemblato

```python
# main.py - {project_name}
def main():
    print("Progetto {project_name} assemblato con successo")
    return True

if __name__ == "__main__":
    main()
```

```python
# test_main.py
def test_main():
    from main import main
    assert main() == True
    print("[OK] test_main")
```

### Note di assemblaggio
- Componenti A, B, C integrati
- Test inclusi
- Documentazione inline

## CHECKLIST PER NOTARIZZAZIONE
- [x] Conformita alle specifiche Gemini: tutti i REQ coperti
- [x] Completezza: tutti i componenti presenti
- [x] Funzionalita: esegui `python main.py`
- [x] Standard rispettati: ETG compliant

---
*[DEMO MODE - assemblato simulato]*
"""

        suffix = f"assemblato_r{session.retry_count}" if is_revision else "assemblato"
        output_path = self.write_output(output, session, suffix)
        session.claude_output = str(output_path)
        session.current_agent = AgentRole.CHATGPT
        if AgentRole.CLAUDE not in session.completed_agents:
            session.completed_agents.append(AgentRole.CLAUDE)

        next_msg = ETGMessage(
            session_id=msg.session_id,
            project_name=project_name,
            sender=AgentRole.CLAUDE,
            recipient=AgentRole.CHATGPT,
            msg_type=MessageType.REVIEW,
            subject=f"[DEMO/REVISIONE] {project_name} - notarizzazione",
            payload={
                "brief": msg.payload.get("brief", ""),
                "gemini_specs_path": msg.payload.get("gemini_specs_path", ""),
                "gemini_output": msg.payload.get("gemini_output", ""),
                "claude_assembled_path": str(output_path),
                "claude_output": output,
                "instructions": "[DEMO] Verifica e certifica.",
            },
            attachments=[str(output_path)],
            etg_path=msg.etg_path,
            depends_on=msg.msg_id,
            priority=2,
        )

        inbox_base = self.workspace / "inbox"
        self.send_to(AgentRole.CHATGPT, next_msg, inbox_base)
        return output, next_msg


class MockChatGPTAgent(BaseAgent):
    """Mock ChatGPT - genera certificato simulato (sempre CERTIFICATO in demo)."""

    def __init__(self, config: dict, workspace_path: Path, **kwargs):
        super().__init__(config, workspace_path)

    def build_system_prompt(self) -> str:
        return "[DEMO] ChatGPT Mock"

    def _compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def process(self, msg: ETGMessage, session: ETGSession) -> tuple[str, ETGMessage]:
        project_name = msg.project_name
        claude_output = msg.payload.get("claude_output", "")
        doc_hash = self._compute_hash(claude_output)
        now = datetime.now()

        logger.info(f"[DEMO/CHATGPT] Notarizzazione: {project_name}")

        output = f"""
============================================================
         CERTIFICATO ETG STUDIO [DEMO] - {now.strftime('%Y-%m-%d')}
         Notaio: ChatGPT Mock (modalita demo)
============================================================

PROGETTO: {project_name}
SESSION ID: {session.session_id}
HASH DOCUMENTO: {doc_hash}

## ESITO: CERTIFICATO

## AUDIT TRAIL
1. Specifiche Gemini ricevute: OK
2. Assemblato Claude ricevuto: OK
3. Conformita verificata: OK (demo)
4. Qualita codice: OK (demo)

## CONFORMITA SPECIFICHE GEMINI
- [x] REQ-001: Implementato
- [x] REQ-002: Implementato
- [x] REQ-003: Implementato

## RILIEVI
Nessun rilievo (modalita demo).

## RACCOMANDAZIONI
Eseguire con API keys reali per audit effettivo.

## FIRMA DIGITALE
Notaio: ChatGPT Mock
Data: {now.isoformat()}
Hash certificato: {self._compute_hash(doc_hash + now.isoformat())}

---
*[DEMO MODE - certificato simulato]*
"""
        cert_hash = self._compute_hash(output)

        self.certified_path.mkdir(parents=True, exist_ok=True)
        cert_filename = (
            f"CERTIFICATO_{session.session_id[:8]}"
            f"_{now.strftime('%Y%m%d_%H%M%S')}.md"
        )
        cert_path = self.certified_path / cert_filename
        cert_path.write_text(output, encoding="utf-8")

        session.chatgpt_output = str(cert_path)
        session.final_etg_path = msg.etg_path
        session.status = "certified"
        session.completed_agents.append(AgentRole.CHATGPT)

        completion_msg = ETGMessage(
            session_id=msg.session_id,
            project_name=project_name,
            sender=AgentRole.CHATGPT,
            recipient=AgentRole.ORCHESTRATOR,
            msg_type=MessageType.CERTIFICATION,
            subject=f"[DEMO/CERTIFICATO] {project_name}",
            status=MessageStatus.CERTIFIED,
            payload={
                "certified_path": str(cert_path),
                "certification_hash": cert_hash,
                "etg_path": msg.etg_path,
                "esito": "CERTIFICATO",
                "retry_count": session.retry_count,
            },
            attachments=[str(cert_path)],
            certification_hash=cert_hash,
            certified_by=AgentRole.CHATGPT,
            certified_at=now.isoformat(),
            etg_path=msg.etg_path,
        )

        inbox_base = self.workspace / "inbox"
        self.send_to(AgentRole.ORCHESTRATOR, completion_msg, inbox_base)
        return output, completion_msg
