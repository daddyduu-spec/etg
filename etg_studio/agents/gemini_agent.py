"""
ETG Studio - GEMINI: Progettista di Laboratorio
Ruolo: Parametrizzatore. Riceve il brief del progetto, progetta
l'architettura, crea le specifiche tecniche e i template per Claude.
"""

import logging
from pathlib import Path
from datetime import datetime

import google.generativeai as genai

from .base_agent import BaseAgent
from protocols import ETGMessage, ETGSession, MessageType, AgentRole

logger = logging.getLogger("gemini")


SYSTEM_PROMPT = """Sei GEMINI, il Progettista di Laboratorio nel sistema ETG Studio.

Il tuo ruolo è PARAMETRIZZATORE: ricevi un brief di progetto e produci specifiche tecniche
dettagliate, architetture, parametri e template che Claude (l'Assemblatore) utilizzerà
per costruire la soluzione.

## Il tuo output DEVE includere:

### 1. ARCHITETTURA
- Schema strutturale del progetto
- Componenti principali e loro relazioni
- Stack tecnologico consigliato

### 2. SPECIFICHE TECNICHE (parametri)
- Lista dettagliata dei requisiti funzionali
- Requisiti non funzionali (performance, sicurezza, scalabilità)
- Vincoli e dipendenze

### 3. TEMPLATE E STRUTTURE
- Struttura cartelle/file
- Template di codice base
- Interfacce e contratti tra componenti

### 4. PIANO DI LAVORO per Claude
- Step sequenziali che Claude deve seguire
- Priorità di implementazione
- Punti critici da rispettare

### 5. CRITERI DI VALIDAZIONE per ChatGPT (Notaio)
- Checklist di conformità
- Standard da verificare
- Red flag da segnalare

Sii preciso, tecnico e strutturato. Il tuo output è la BIBBIA del progetto.
"""


class GeminiAgent(BaseAgent):
    """Agente Gemini - Progettista/Parametrizzatore."""

    def __init__(self, config: dict, workspace_path: Path, api_key: str):
        super().__init__(config, workspace_path)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(
            model_name=config["model"],
            system_instruction=SYSTEM_PROMPT
        )

    def build_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def process(self, msg: ETGMessage, session: ETGSession) -> tuple[str, ETGMessage]:
        """
        Riceve il brief del progetto.
        Produce specifiche tecniche complete.
        Invia a Claude per l'assemblaggio.
        """
        brief = msg.payload.get("brief", "")
        project_name = msg.project_name
        etg_path = msg.etg_path

        logger.info(f"[GEMINI] Progettazione: {project_name}")

        # Costruisce il prompt con il brief
        user_prompt = f"""
## BRIEF DI PROGETTO: {project_name}

{brief}

## CONTESTO ETG
Cartella condivisa ETG: {etg_path}
Session ID: {session.session_id[:8]}

Produci le SPECIFICHE TECNICHE COMPLETE per questo progetto.
Claude le userà per assemblare la soluzione. ChatGPT le userà come riferimento per la certificazione.
"""

        # Chiama Gemini API
        response = self.client.generate_content(user_prompt)
        output = response.text

        # Salva l'output nella cartella shared
        output_path = self.write_output(output, session, "specifiche")
        session.gemini_output = str(output_path)
        session.current_agent = AgentRole.CLAUDE
        session.completed_agents.append(AgentRole.GEMINI)

        logger.info(f"[GEMINI] Specifiche salvate: {output_path}")

        # Prepara il messaggio per Claude
        next_msg = ETGMessage(
            session_id=msg.session_id,
            project_name=project_name,
            sender=AgentRole.GEMINI,
            recipient=AgentRole.CLAUDE,
            msg_type=MessageType.HANDOFF,
            subject=f"[SPECIFICHE] {project_name} - pronto per assemblaggio",
            payload={
                "brief": brief,
                "gemini_specs_path": str(output_path),
                "gemini_output": output,
                "instructions": "Assembla la soluzione seguendo le specifiche di Gemini.",
            },
            attachments=[str(output_path)],
            etg_path=etg_path,
            depends_on=msg.msg_id,
        )

        # Invia nella inbox di Claude
        inbox_base = self.workspace / "inbox"
        self.send_to(AgentRole.CLAUDE, next_msg, inbox_base)

        return output, next_msg
