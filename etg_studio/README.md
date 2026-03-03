# ETG Studio - Multi-AI Collaboration

Sistema di collaborazione tra tre AI (Gemini, Claude, ChatGPT) su cartelle condivise ETG.
Ogni AI svolge un ruolo specifico nella pipeline di produzione.

---

## Ruoli

| AI | Ruolo | Funzione |
|----|-------|----------|
| **Gemini** | Progettista Laboratorio | Riceve il brief, progetta l'architettura, crea specifiche tecniche e parametri |
| **Claude** | Assemblatore | Legge le specifiche Gemini, costruisce la soluzione completa (codice, doc) |
| **ChatGPT** | Notaio | Audita l'output di Claude contro le specifiche Gemini, emette certificato |

## Flusso di lavoro

```
Brief del progetto
      |
      v
[GEMINI - Progettista]
  - Architettura
  - Specifiche tecniche
  - Template
  - Criteri di validazione
      |
      v (inbox/claude/)
[CLAUDE - Assemblatore]
  - Legge specifiche Gemini
  - Assembla la soluzione
  - Genera codice e documentazione
  - Prepara checklist per Notaio
      |
      v (inbox/chatgpt/)
[CHATGPT - Notaio]
  - Audit punto per punto
  - Verifica conformità
  - Emette CERTIFICATO ETG
      |
      v (certified/)
PROGETTO CERTIFICATO
```

## Struttura cartelle

```
etg_studio/
├── workspace/
│   ├── inbox/
│   │   ├── gemini/      <- task per Gemini
│   │   ├── claude/      <- task per Claude
│   │   ├── chatgpt/     <- task per ChatGPT (Notaio)
│   │   └── orchestrator/ <- notifiche completamento
│   ├── shared/          <- output condivisi tra agenti
│   ├── sessions/        <- stato sessioni
│   ├── certified/       <- certificati finali
│   └── logs/            <- log per agente
├── agents/
│   ├── gemini_agent.py
│   ├── claude_agent.py
│   └── chatgpt_agent.py
├── protocols/
│   └── message.py       <- protocollo messaggi JSON
├── config/
│   └── config.yaml
├── orchestrator.py      <- coordinatore principale
├── launch.py            <- launcher interattivo
└── requirements.txt
```

## Setup

### 1. Installa dipendenze

```bash
pip install -r requirements.txt
```

### 2. Configura API keys

```bash
cp .env.example .env
# Modifica .env con le tue chiavi
```

Oppure esporta direttamente:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_AI_API_KEY="AIza..."
```

### 3. Avvia

**Modalità interattiva:**
```bash
python launch.py
```

**Da linea di comando:**
```bash
python orchestrator.py run \
  --name "Nome Progetto" \
  --brief "Descrizione del progetto..." \
  --etg-path "etg://shared/mio-progetto"
```

**Da file brief:**
```bash
python orchestrator.py run \
  --name "API REST" \
  --brief brief.txt \
  --etg-path "etg://shared/api-rest"
```

**Modalita daemon (ETG sync continuo):**
```bash
python orchestrator.py daemon --poll 5
```

## Protocollo messaggi

Ogni messaggio tra agenti e' un file JSON nella inbox del destinatario:

```json
{
  "msg_id": "uuid",
  "session_id": "uuid",
  "project_name": "Nome Progetto",
  "sender": "gemini",
  "recipient": "claude",
  "msg_type": "handoff",
  "subject": "[SPECIFICHE] Nome Progetto",
  "payload": {
    "brief": "...",
    "gemini_output": "...",
    "gemini_specs_path": "./workspace/shared/..."
  },
  "status": "pending",
  "etg_path": "etg://shared/..."
}
```

## Certificato di notarizzazione

Il Notaio (ChatGPT) emette un certificato in `workspace/certified/`:

```
CERTIFICATO ETG STUDIO - [DATA]
Notaio: ChatGPT (gpt-4o)

PROGETTO: ...
SESSION ID: ...
HASH DOCUMENTO: sha256:...

ESITO: CERTIFICATO / NON CERTIFICATO / CERTIFICATO CON RISERVE

AUDIT TRAIL: [punto per punto]
CONFORMITA' GEMINI: [checklist]
RILIEVI: [eventuali problemi]
FIRMA: [hash SHA256 del certificato]
```

## Integrazione ETG

Il campo `etg_path` in ogni messaggio indica la cartella condivisa ETG di destinazione.
Dopo la certificazione, il progetto viene salvato in `workspace/certified/` pronto
per il push nella cartella ETG specificata.

Per sincronizzazione automatica con ETG, configura `ETG_HOST` e `ETG_API_KEY` nel `.env`.
