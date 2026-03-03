"""
ETG Studio - CHATGPT: DEPRECATO (27/02/2026)
ChatGPT è stato rimosso dalla catena notarile ETG.
Ruolo attuale: advisor esterno di Carlo — non partecipa alla pipeline.

Il notaio è ora Opus (Claude Opus, chat interattiva via Carlo come relay).
Questo file è conservato per riferimento storico — NON viene più usato.
"""
# ATTENZIONE: questo agente non viene istanziato dall'orchestratore aggiornato.

import hashlib
import logging
from datetime import datetime
from pathlib import Path

from openai import OpenAI

from .base_agent import BaseAgent
from protocols import ETGMessage, ETGSession, MessageType, MessageStatus, AgentRole

logger = logging.getLogger("chatgpt")


SYSTEM_PROMPT = """Sei CHATGPT, il Notaio nel sistema ETG Studio.

Il tuo ruolo è NOTAIO CERTIFICATORE: ricevi le specifiche di Gemini e l'assemblato di Claude,
li confronti rigorosamente e emetti il certificato di conformità ufficiale ETG.

## Il tuo processo di notarizzazione:

### 1. AUDIT DOCUMENTALE
- Verifica che ogni punto delle specifiche Gemini sia stato implementato da Claude
- Identifica discrepanze, omissioni o deviazioni
- Classifica ogni finding: CONFORME / NON CONFORME / PARZIALE

### 2. VERIFICA DI QUALITÀ
- Correttezza logica e tecnica dell'implementazione
- Completezza della documentazione
- Sicurezza e best practice rispettate
- Standard ETG rispettati

### 3. CERTIFICATO DI NOTARIZZAZIONE
Il tuo output DEVE contenere:
```
╔══════════════════════════════════════════════════════╗
║         CERTIFICATO ETG STUDIO - [DATA]              ║
║         Notaio: ChatGPT (gpt-4o)                     ║
╚══════════════════════════════════════════════════════╝

PROGETTO: [nome]
SESSION ID: [id]
HASH DOCUMENTO: [sha256]

## ESITO: CERTIFICATO / NON CERTIFICATO / CERTIFICATO CON RISERVE

## AUDIT TRAIL
[punto per punto delle verifiche]

## CONFORMITÀ SPECIFICHE GEMINI
[checklist dettagliata]

## RILIEVI
[eventuali problemi trovati]

## RACCOMANDAZIONI
[suggerimenti per miglioramenti futuri]

## FIRMA DIGITALE
Notaio: ChatGPT
Data: [timestamp ISO]
Hash: [sha256 dell'intero documento]
```

### 4. DECISIONE FINALE
- CERTIFICATO: tutto conforme, pronto per ETG
- CERTIFICATO CON RISERVE: funziona ma ci sono raccomandazioni non bloccanti
- NON CERTIFICATO: problemi critici, Claude deve riassemblare

Sei rigoroso, imparziale e la tua certificazione ha valore legale-procedurale in ETG.
"""


class ChatGPTAgent(BaseAgent):
    """Agente ChatGPT - Notaio."""

    def __init__(self, config: dict, workspace_path: Path, api_key: str):
        super().__init__(config, workspace_path)
        self.client = OpenAI(api_key=api_key)

    def build_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def _compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def process(self, msg: ETGMessage, session: ETGSession) -> tuple[str, ETGMessage]:
        """
        Riceve l'assemblato di Claude e le specifiche di Gemini.
        Esegue l'audit completo e certifica.
        Salva nella cartella certified/.
        """
        gemini_output = msg.payload.get("gemini_output", "")
        claude_output = msg.payload.get("claude_output", "")
        brief = msg.payload.get("brief", "")
        project_name = msg.project_name
        etg_path = msg.etg_path

        logger.info(f"[CHATGPT/NOTAIO] Notarizzazione: {project_name}")

        # Hash del documento Claude per la firma
        doc_hash = self._compute_hash(claude_output)

        # Chiama GPT-4o per l'audit
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"""
## PROGETTO DA NOTARIZZARE: {project_name}
## SESSION ID: {session.session_id}
## HASH DOCUMENTO CLAUDE: {doc_hash}

---
## BRIEF ORIGINALE:
{brief}

---
## SPECIFICHE GEMINI (Progettista di Laboratorio):
{gemini_output}

---
## ASSEMBLATO CLAUDE (Assemblatore):
{claude_output}

---
Esegui l'audit completo. Verifica la conformità punto per punto.
Emetti il CERTIFICATO DI NOTARIZZAZIONE ETG ufficiale.
ETG Path destinazione: {etg_path}
Data/ora: {datetime.now().isoformat()}
"""
                }
            ]
        )

        output = response.choices[0].message.content
        cert_hash = self._compute_hash(output)
        esito = self._extract_esito(output)

        # Salva il certificato (anche se NON certificato, serve come audit trail)
        self.certified_path.mkdir(parents=True, exist_ok=True)
        status_label = esito.replace("_", "-")
        cert_filename = (
            f"{status_label}_{session.session_id[:8]}_r{session.retry_count}"
            f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        cert_path = self.certified_path / cert_filename
        cert_path.write_text(output, encoding="utf-8")

        session.chatgpt_output = str(cert_path)
        session.final_etg_path = etg_path
        session.completed_agents.append(AgentRole.CHATGPT)

        inbox_base = self.workspace / "inbox"

        # ── RIFIUTO: rimanda a Claude con il feedback dell'audit ──────────────
        if esito == "NON_CERTIFICATO" and session.retry_count < session.max_retries:
            session.retry_count += 1
            session.last_audit_notes = output
            session.last_rejection_reason = self._extract_rejection_reason(output)
            session.status = "revision_requested"
            # Rimuove CHATGPT dai completed per permettere un nuovo giro
            session.completed_agents = [a for a in session.completed_agents if a != AgentRole.CHATGPT]

            logger.warning(
                f"[CHATGPT/NOTAIO] RIFIUTATO (tentativo {session.retry_count}/{session.max_retries}): "
                f"{project_name}"
            )

            revision_msg = ETGMessage(
                session_id=msg.session_id,
                project_name=project_name,
                sender=AgentRole.CHATGPT,
                recipient=AgentRole.CLAUDE,
                msg_type=MessageType.REVISION_REQUESTED if hasattr(MessageType, 'REVISION_REQUESTED') else MessageType.REVIEW,
                subject=f"[REVISIONE #{session.retry_count}] {project_name} - richiesta correzioni",
                payload={
                    "brief": msg.payload.get("brief", ""),
                    "gemini_output": msg.payload.get("gemini_output", ""),
                    "gemini_specs_path": msg.payload.get("gemini_specs_path", ""),
                    "claude_previous_output": claude_output,
                    "audit_notes": output,
                    "rejection_reason": session.last_rejection_reason,
                    "retry_count": session.retry_count,
                    "instructions": (
                        f"Il Notaio ha RIFIUTATO il tuo assemblato (tentativo {session.retry_count}).\n"
                        "Leggi attentamente le note di audit e correggi i problemi indicati.\n"
                        "Riassembla tenendo conto di OGNI rilievo del Notaio."
                    ),
                },
                attachments=[str(cert_path)],
                etg_path=etg_path,
                depends_on=msg.msg_id,
                priority=3,
            )
            self.send_to(AgentRole.CLAUDE, revision_msg, inbox_base)
            msg.mark_processed(MessageStatus.REJECTED)
            return output, revision_msg

        # ── CERTIFICATO (o max retry raggiunto) ──────────────────────────────
        if esito == "NON_CERTIFICATO":
            session.status = "failed_max_retries"
            logger.error(f"[CHATGPT/NOTAIO] Max retry raggiunto: {project_name}")
        else:
            session.status = "certified"
            logger.info(f"[CHATGPT/NOTAIO] {esito}: {cert_path}")

        msg.certification_hash = cert_hash
        msg.certified_by = AgentRole.CHATGPT
        msg.certified_at = datetime.now().isoformat()
        msg.mark_processed(MessageStatus.CERTIFIED)

        final_report = self._build_final_report(session, cert_path, cert_hash, output, esito)
        final_path = self.write_output(final_report, session, "report_finale")

        completion_msg = ETGMessage(
            session_id=msg.session_id,
            project_name=project_name,
            sender=AgentRole.CHATGPT,
            recipient=AgentRole.ORCHESTRATOR,
            msg_type=MessageType.CERTIFICATION,
            subject=f"[{esito}] {project_name}",
            status=MessageStatus.CERTIFIED,
            payload={
                "certified_path": str(cert_path),
                "final_report_path": str(final_path),
                "certification_hash": cert_hash,
                "etg_path": etg_path,
                "esito": esito,
                "retry_count": session.retry_count,
            },
            attachments=[str(cert_path)],
            certification_hash=cert_hash,
            certified_by=AgentRole.CHATGPT,
            certified_at=datetime.now().isoformat(),
            etg_path=etg_path,
        )
        self.send_to(AgentRole.ORCHESTRATOR, completion_msg, inbox_base)

        return output, completion_msg

    def _extract_esito(self, cert_text: str) -> str:
        if "NON CERTIFICATO" in cert_text:
            return "NON_CERTIFICATO"
        if "CON RISERVE" in cert_text:
            return "CERTIFICATO_CON_RISERVE"
        return "CERTIFICATO"

    def _extract_rejection_reason(self, cert_text: str) -> str:
        """Estrae il motivo del rifiuto per inviarlo a Claude come feedback."""
        lines = cert_text.splitlines()
        capture = False
        reasons = []
        for line in lines:
            if any(kw in line.upper() for kw in ["RILIEVI", "NON CONFORME", "PROBLEMI", "MANCANTE"]):
                capture = True
            if capture:
                reasons.append(line)
            if capture and len(reasons) > 20:
                break
        return "\n".join(reasons) if reasons else cert_text[:500]

    def _build_final_report(
        self, session: ETGSession, cert_path: Path, cert_hash: str,
        cert_text: str, esito: str = "CERTIFICATO"
    ) -> str:
        esito = self._extract_esito(cert_text)
        return f"""# REPORT FINALE ETG STUDIO

## Progetto: {session.project_name}
## Session ID: {session.session_id}
## Completato: {datetime.now().isoformat()}

---

## PIPELINE ESEGUITA
1. **GEMINI** (Progettista Laboratorio) → {session.gemini_output}
2. **CLAUDE** (Assemblatore) → {session.claude_output}
3. **CHATGPT** (Notaio) → {cert_path}

## ESITO FINALE: {esito}

## CERTIFICATO
- File: {cert_path.name}
- Hash SHA256: {cert_hash}
- Destinazione ETG: {session.final_etg_path}

---
*Generato automaticamente da ETG Studio*
"""
