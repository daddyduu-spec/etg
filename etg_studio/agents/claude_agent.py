"""
ETG Studio - SONNET (Claude Sonnet CLI): Assemblatore/Revisore
Ruolo: Riceve le specifiche di Gemini, assembla la soluzione completa
(codice, documenti, strutture) e deposita in workspace/ per Opus (Notaio).
La notarizzazione NON è automatica — passa sempre per Carlo (DH_ext, Eq. 14).
"""

import logging
from pathlib import Path
from datetime import datetime

import anthropic

from .base_agent import BaseAgent  # base_agent aggiunge etg_studio/ al sys.path
from protocols import ETGMessage, ETGSession, MessageType, AgentRole
from etg_engine import catena_etg_p, PianoD, AggregatoCU, Unita_ell  # motore ETG-P

logger = logging.getLogger("claude")


SYSTEM_PROMPT = """Sei SONNET (Claude Sonnet CLI), il Revisore/Assemblatore nel sistema ETG Studio.

## Catena notariale vigente (27/02/2026):
Gemini (Progettista) → Sonnet-CLI (Assemblatore) → [CARLO checkpoint] → Opus (Notaio) → Carlo (certificazione)

## Il tuo ruolo:
Ricevi le specifiche di Gemini. Assembli la soluzione completa in Python (no JSON).
Il tuo output va in workspace/output/ e attende che Carlo lo porti a Opus per notarizzazione.
NON hai accesso diretto a Opus. Carlo è il relay obbligatorio (DH_ext, Eq. 14 ETG).

## Regole ETG-P:
- Usa etg_engine.py per qualsiasi calcolo della catena Σ_CU → H_C → Z_C → F_C → Δ_ℓ
- Output in Python, mai in JSON
- Se trovi contraddizioni con ClaudeETG/ (il canone), segnalale — non le risolvere autonomamente
- Dichiara cosa NON sai (vincolo di ignoranza anti-allucinazione)

## Output strutturato (formato .md):
- **Codice Python completo** (no JSON)
- **Note di assemblaggio**: scelte e motivazioni
- **Dipendenze**: pacchetti necessari
- **Checklist per Opus** (non per ChatGPT):
```
## CHECKLIST PER OPUS (Notaio)
- [ ] Conformità alle specifiche Gemini
- [ ] Uso corretto etg_engine per calcoli ETG-P
- [ ] Nessun JSON nell'output
- [ ] Vincoli duri ETG-G rispettati
- [ ] Dichiarazione di ignoranza inclusa
```

Sei meticoloso e costruisci soluzioni che funzionano. Non inventi contenuto ETG.
"""


class ClaudeAgent(BaseAgent):
    """Agente Claude - Assemblatore."""

    def __init__(self, config: dict, workspace_path: Path, api_key: str):
        super().__init__(config, workspace_path)
        self.client = anthropic.Anthropic(api_key=api_key)

    def build_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def _is_revision(self, msg: ETGMessage) -> bool:
        """Verifica se il messaggio e' una richiesta di revisione dal Notaio."""
        return (
            msg.sender == AgentRole.CHATGPT
            or msg.payload.get("audit_notes") is not None
            or msg.payload.get("retry_count", 0) > 0
        )

    def _build_revision_prompt(self, msg: ETGMessage) -> str:
        """Costruisce il prompt per la revisione basato sul feedback del Notaio."""
        project_name = msg.project_name
        brief = msg.payload.get("brief", "")
        gemini_output = msg.payload.get("gemini_output", "")
        previous_output = msg.payload.get("claude_previous_output", "")
        audit_notes = msg.payload.get("audit_notes", "")
        rejection_reason = msg.payload.get("rejection_reason", "")
        retry_count = msg.payload.get("retry_count", 1)

        return f"""## REVISIONE #{retry_count} - PROGETTO: {project_name}

## BRIEF ORIGINALE:
{brief}

## SPECIFICHE TECNICHE DI GEMINI (Progettista):
{gemini_output}

---
## IL TUO ASSEMBLATO PRECEDENTE (RIFIUTATO DAL NOTAIO):
{previous_output}

---
## FEEDBACK DEL NOTAIO (ChatGPT) - MOTIVO DEL RIFIUTO:
{rejection_reason}

## NOTE COMPLETE DI AUDIT:
{audit_notes}

---
ISTRUZIONI: Il Notaio ha rifiutato il tuo assemblato precedente.
Leggi ATTENTAMENTE ogni rilievo e correggi TUTTI i problemi segnalati.
Riassembla la soluzione COMPLETA (non solo le parti modificate).
Includi la checklist aggiornata per una nuova notarizzazione.

ETG Path: {msg.etg_path}
"""

    def process(self, msg: ETGMessage, session: ETGSession) -> tuple[str, ETGMessage]:
        """
        Riceve le specifiche da Gemini (o revisione dal Notaio).
        Assembla la soluzione completa.
        Invia a ChatGPT per notarizzazione.
        """
        gemini_output = msg.payload.get("gemini_output", "")
        brief = msg.payload.get("brief", "")
        project_name = msg.project_name
        etg_path = msg.etg_path
        is_revision = self._is_revision(msg)

        if is_revision:
            retry_count = msg.payload.get("retry_count", 1)
            logger.info(f"[CLAUDE] REVISIONE #{retry_count}: {project_name}")
            user_prompt = self._build_revision_prompt(msg)
        else:
            logger.info(f"[CLAUDE] Assemblaggio: {project_name}")
            user_prompt = f"""
## PROGETTO: {project_name}
## BRIEF ORIGINALE:
{brief}

## SPECIFICHE TECNICHE DI GEMINI (Progettista):
{gemini_output}

---
Assembla la soluzione completa seguendo le specifiche di Gemini.
Produci tutto il codice e la documentazione necessaria.
Includi la checklist per ChatGPT (Notaio) alla fine.

ETG Path: {etg_path}
"""

        # Chiama Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8096,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ]
        )

        output = response.content[0].text

        # Salva output nella shared (formato .md, no JSON)
        suffix = f"assemblato_r{session.retry_count}" if is_revision else "assemblato"
        output_path = self.write_output(output, session, suffix)
        session.sonnet_output = str(output_path)
        session.claude_output = str(output_path)  # alias legacy
        session.current_agent = AgentRole.CARLO    # prossimo checkpoint: Carlo
        session.completed_agents.append(AgentRole.SONNET)

        logger.info(f"[SONNET] Assemblaggio salvato: {output_path}")

        # Scrive in Carlo.txt per notificare il checkpoint
        carlo_txt = self.workspace / "scambio" / "Carlo.txt"
        if carlo_txt.exists():
            notifica = (
                f"\n\n---\nAutore: Sonnet-CLI\nData: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Motivo: Assemblaggio completato — checkpoint Carlo richiesto\n---\n"
                f"Progetto: {project_name}\n"
                f"Output: {output_path}\n"
                f"Prossimo passo: porta l'output a Opus per notarizzazione.\n"
                f"Session: {msg.session_id[:8]}\n"
            )
            with open(carlo_txt, "a", encoding="utf-8") as f:
                f.write(notifica)

        # Prepara il messaggio per il checkpoint Carlo (DH_ext, Eq. 14)
        # Carlo leggerà Carlo.txt e porterà manualmente l'output a Opus
        gemini_specs_path = msg.payload.get("gemini_specs_path", "")

        next_msg = ETGMessage(
            session_id=msg.session_id,
            project_name=project_name,
            sender=AgentRole.SONNET,
            recipient=AgentRole.CARLO,           # checkpoint umano obbligatorio
            msg_type=MessageType.CARLO_CHECKPOINT,
            subject=f"[CHECKPOINT CARLO] {project_name} — da portare a Opus",
            payload={
                "brief": brief,
                "gemini_specs_path": gemini_specs_path,
                "sonnet_output_path": str(output_path),
                "sonnet_output": output,
                "instructions": (
                    "Carlo: assemblaggio Sonnet completato. "
                    "Porta l'output a Opus (notaio) per certificazione notarile. "
                    "Opus scriverà in Carlo.txt il verdetto."
                ),
            },
            attachments=[str(output_path)],
            etg_path=etg_path,
            depends_on=msg.msg_id,
            priority=2,
        )

        # Non inviare a inbox automatica — Carlo è umano, legge Carlo.txt
        logger.info(f"[SONNET] Checkpoint Carlo notificato via Carlo.txt")

        return output, next_msg
