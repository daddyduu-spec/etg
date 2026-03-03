"""
ETG Studio - Lab Watcher
Monitora workspace/lab/ e gestisce il dialogo automatico Gemini <-> Claude.

Quando Gemini scrive una bozza (gemini_draft_NN.md):
  -> chiama Claude via CLI (claude --print) per generare la review
  -> salva la review come claude_review_NN.md
  -> Gemini (in Anti Gravity) vede la review e risponde

Quando Claude approva (esito = APPROVO):
  -> scrive FINAL.md
  -> prepara il file per il notaio in workspace/for_notaio/
  -> scrive NOTIFY_CARLO.md per avvisare Carlo

Uso:
  python etg_studio/lab_watcher.py SESSION_<id> [--poll 5] [--max-rounds 10] [--dry-run]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
WORKSPACE = SCRIPT_DIR / "workspace"
LAB = WORKSPACE / "lab"
FOR_NOTAIO = WORKSPACE / "for_notaio"
ETG_ROOT = SCRIPT_DIR.parent  # Documents/ai/etg/


def get_session_dir(session_id: str) -> Path:
    d = LAB / session_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def find_latest_file(session_dir: Path, prefix: str) -> tuple[Path | None, int]:
    """Trova l'ultimo file con un dato prefisso e restituisce (path, numero)."""
    files = sorted(session_dir.glob(f"{prefix}_*.md"))
    if not files:
        return None, 0
    last = files[-1]
    match = re.search(r"_(\d+)\.md$", last.name)
    num = int(match.group(1)) if match else 0
    return last, num


def get_etg_dirs() -> list[str]:
    """Restituisce le cartelle ETG da dare a Claude CLI con --add-dir.
    Include chatgpt/ per accesso a studiare_fisica_extracted.txt."""
    dirs = []
    for name in ["ClaudeETG", "ETG_G", "ETG_P", "chatgpt", "etg_studio/workspace"]:
        d = ETG_ROOT / name
        if d.exists():
            dirs.append(str(d))
    return dirs


def load_session_context(session_dir: Path) -> str:
    """Carica CONTESTO_SESSIONE.md se esiste nella cartella sessione.
    Questo file contiene conoscenze specifiche per la sessione corrente
    che Claude CLI deve avere prima di giudicare."""
    ctx_file = session_dir / "CONTESTO_SESSIONE.md"
    if ctx_file.exists():
        content = ctx_file.read_text(encoding="utf-8-sig", errors="replace")
        return f"\n## Contesto specifico di sessione\n{content}\n"
    return ""


def build_review_prompt(draft_path: Path, draft_num: int, session_id: str,
                        previous_reviews: list[Path],
                        session_dir: Path | None = None) -> str:
    """Costruisce il prompt per Claude CLI."""
    # utf-8-sig per gestire BOM (Gemini/Anti Gravity a volte scrive con BOM)
    draft_content = draft_path.read_text(encoding="utf-8-sig", errors="replace")

    # Carica review precedenti per contesto
    prev_context = ""
    for rev in previous_reviews[-2:]:  # ultime 2 review
        prev_context += f"\n### {rev.name}\n{rev.read_text(encoding='utf-8', errors='replace')}\n"

    # Carica contesto sessione se esiste
    session_context = ""
    if session_dir:
        session_context = load_session_context(session_dir)

    prompt = f"""Sei Claude, Assemblatore ETG Studio. Devi fare la review della bozza #{draft_num:02d} di Gemini.

## Contesto ETG
Hai accesso alle cartelle ClaudeETG/, ETG_G/, ETG_P/, chatgpt/ tramite --add-dir.
PRIMA di giudicare, LEGGI questi file:
- ClaudeETG/PROMPT_RESTART.md (glossario completo)
- ClaudeETG/02_VOCABOLARIO/VOCABOLARIO_ETG_COMPLETO.md (tutti i simboli canonici)
- ETG_G/04_VINCOLI/VINCOLI_DURI_G.md (vincoli inviolabili)
- ETG_P/ (lavoro precedente di parametrizzazione)
NON dichiarare un termine "non canonico" se non hai verificato nel vocabolario.

## PROTOCOLLO DI PREVALENZA (OBBLIGATORIO)
Gemini (Anti Gravity) ha in memoria l'intero file chatgpt/studiare_fisica_extracted.txt
(3.2MB, 122.000+ righe della conversazione fondativa ETG).
TU hai accesso allo stesso file via --add-dir nella cartella chatgpt/.

REGOLE DI INGAGGIO:
1. Se Gemini usa un termine che non trovi nel vocabolario canonico:
   - PRIMA cerca il termine in chatgpt/studiare_fisica_extracted.txt
   - Se lo trovi: il termine ha fondamento nelle fonti originali. NON bocciarlo.
     Segnalalo come "presente nelle fonti ma non ancora canonizzato" e suggerisci
     di sottoporre a verdetto notarile. Questo NON e' motivo di RIVEDI.
   - Se NON lo trovi ne' nel vocabolario ne' nelle fonti: segnalalo come
     "possibile invenzione — non trovato in nessuna fonte".
2. Se Gemini cita un numero di riga o un passaggio specifico:
   - VERIFICA la citazione leggendo il file indicato. Non fidarti ciecamente,
     ma non bocciare ciecamente.
3. CHI SA DI PIU' PREVALE: se la bozza di Gemini contiene conoscenza profonda
   che tu non avevi, NON e' un errore — e' nuova informazione da valutare.
   Il tuo compito e' verificare coerenza, non limitare la conoscenza.
4. Se TU sai qualcosa che Gemini sembra ignorare (es: vincolo duro, correzione
   notarile, dichiarazione dell'autore), INDICA DOVE Gemini puo' verificare
   (es: "vedi VOCABOLARIO_ETG_COMPLETO.md sezione E" o "vedi VINCOLI_DURI_G.md").
{session_context}
## Istruzioni
Leggi la bozza di Gemini e valuta:
1. Coerenza col master ETG e vocabolario canonico
2. Terminologia: usa solo simboli canonizzati? (APPLICA protocollo di prevalenza!)
3. Vincoli duri ETG-G: violazioni?
4. Derive creative: espansioni non giustificate?
5. Completezza logica

{f"## Review precedenti{prev_context}" if prev_context else ""}

## Bozza da recensire: gemini_draft_{draft_num:02d}.md
{draft_content}

## Formato risposta
Rispondi ESATTAMENTE in questo formato markdown:

# Review {draft_num:02d}
**Sessione**: {session_id}
**Bozza**: gemini_draft_{draft_num:02d}.md
**Data**: {datetime.now().strftime("%Y-%m-%d")}

## Valutazione
- Coerenza col master: [OK / PROBLEMI]
- Terminologia: [OK / PROBLEMI — con fonti verificate]
- Vincoli duri: [OK / VIOLAZIONI]
- Derive creative: [NESSUNA / SEGNALATE]

## Termini non canonizzati trovati nelle fonti
[lista di termini presenti in studiare_fisica ma non nel vocabolario, con riga approssimativa — o "Nessuno"]

## Problemi trovati
[lista numerata, o "Nessuno"]

## Suggerimenti
[cosa correggere — INDICARE SEMPRE dove l'altro puo' verificare]

## Esito
[PROSEGUI / RIVEDI / APPROVO]

IMPORTANTE: scrivi APPROVO solo se la bozza e' veramente coerente e completa.
Scrivi RIVEDI se ci sono problemi da correggere.
Scrivi PROSEGUI se e' sulla buona strada ma servono aggiunte.
NON scrivere RIVEDI solo perche' un termine non e' nel vocabolario — se e' nelle fonti, e' PROSEGUI con nota per il notaio."""

    return prompt


def _find_claude_cli() -> str:
    """Trova il path del CLI claude su Windows/Linux/Mac."""
    import shutil

    # Prova prima 'claude' direttamente
    found = shutil.which("claude")
    if found:
        return found

    # Su Windows, prova 'claude.cmd' (wrapper npm)
    if sys.platform == "win32":
        found = shutil.which("claude.cmd")
        if found:
            return found
        # Path noto npm global
        npm_path = Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd"
        if npm_path.exists():
            return str(npm_path)

    return ""


def call_claude(prompt: str, dry_run: bool = False) -> str:
    """Chiama Claude via CLI e restituisce la risposta."""
    if dry_run:
        return f"""# Review (DRY RUN)
**Data**: {datetime.now().strftime("%Y-%m-%d")}

## Valutazione
- Coerenza col master: OK
- Terminologia: OK
- Vincoli duri: OK
- Derive creative: NESSUNA

## Problemi trovati
Nessuno (dry run)

## Suggerimenti
Nessuno (dry run)

## Esito
APPROVO"""

    claude_cmd = _find_claude_cli()
    if not claude_cmd:
        print("[ERRORE] 'claude' CLI non trovato.")
        print("  Provato: claude, claude.cmd, %APPDATA%/npm/claude.cmd")
        return ""

    # Salva il prompt su file temporaneo per evitare il limite di Windows
    # sulla lunghezza della riga di comando (~8000 chars)
    import tempfile
    prompt_file = Path(tempfile.mktemp(suffix=".txt", prefix="etg_prompt_"))
    prompt_file.write_text(prompt, encoding="utf-8")

    try:
        # Passa il prompt via stdin Python (evita encoding issues di 'type' su Windows)
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_text = f.read()

        # Costruisci il comando con --add-dir per le cartelle ETG
        cmd_args = [claude_cmd, "--print", "--model", "sonnet"]
        for d in get_etg_dirs():
            cmd_args.extend(["--add-dir", d])

        result = subprocess.run(
            cmd_args,
            input=prompt_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=600,  # 10 min: Claude deve leggere file + studiare_fisica
            cwd=str(ETG_ROOT),
            shell=(sys.platform == "win32"),
        )
        if result.returncode != 0:
            print(f"[ERRORE] Claude CLI ha restituito codice {result.returncode}")
            print(f"  stderr: {result.stderr[:500]}")
            return ""
        return result.stdout.strip()
    except FileNotFoundError:
        print("[ERRORE] 'claude' CLI non trovato nel PATH.")
        print("  Assicurati che Claude Code sia installato e nel PATH.")
        return ""
    except subprocess.TimeoutExpired:
        print("[ERRORE] Claude CLI timeout (600s).")
        return ""
    finally:
        # Pulisci il file temporaneo
        try:
            prompt_file.unlink(missing_ok=True)
        except Exception:
            pass


def extract_verdict(review_text: str) -> str:
    """Estrae l'esito dalla review di Claude."""
    # Cerca l'ultima riga con APPROVO, RIVEDI, o PROSEGUI
    for line in reversed(review_text.splitlines()):
        line_upper = line.strip().upper()
        if "APPROVO" in line_upper:
            return "APPROVO"
        if "RIVEDI" in line_upper:
            return "RIVEDI"
        if "PROSEGUI" in line_upper:
            return "PROSEGUI"
    return "SCONOSCIUTO"


def prepare_for_notaio(session_dir: Path, session_id: str):
    """Prepara il file per il notaio (ChatGPT) quando Claude approva."""
    final_path = session_dir / "FINAL.md"
    if not final_path.exists():
        print("[ERRORE] FINAL.md non trovato!")
        return

    final_content = final_path.read_text(encoding="utf-8-sig")

    # Raccoglie la storia del dialogo
    drafts = sorted(session_dir.glob("gemini_draft_*.md"))
    reviews = sorted(session_dir.glob("claude_review_*.md"))

    notaio_text = f"""# RICHIESTA CERTIFICAZIONE NOTARILE — OPUS
**Sessione**: {session_id}
**Data**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Rounds di dialogo Gemini-Claude**: {len(drafts)} bozze, {len(reviews)} review

---

## DOCUMENTO DA CERTIFICARE

{final_content}

---

## NOTA PER CARLO

Il notaio e' Opus (questa chat). Copia il contenuto sopra e incollalo
nella chat Opus attiva, oppure digli: "certifica SESSION_{session_id}".
Opus ha il contesto completo e puo' certificare direttamente.
"""

    FOR_NOTAIO.mkdir(parents=True, exist_ok=True)
    out_path = FOR_NOTAIO / f"NOTAIO_{session_id}.md"
    out_path.write_text(notaio_text, encoding="utf-8")
    print(f"\n{'='*60}")
    print(f"FILE PRONTO PER IL NOTAIO: {out_path}")
    print(f"Carlo: apri la chat Opus e digli 'certifica {session_id}'")
    print(f"{'='*60}\n")
    return out_path


def notify_carlo(session_dir: Path, session_id: str, status: str, message: str):
    """Scrive un file di notifica per Carlo."""
    notify_path = session_dir / "NOTIFY_CARLO.md"
    notify_path.write_text(
        f"# Notifica — {session_id}\n"
        f"**Stato**: {status}\n"
        f"**Data**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"{message}\n",
        encoding="utf-8",
    )


def watch_session(session_id: str, poll_interval: int = 5,
                  max_rounds: int = 10, dry_run: bool = False):
    """
    Monitora una sessione di lab e gestisce il dialogo automaticamente.
    """
    session_dir = get_session_dir(session_id)
    print(f"\n{'='*60}")
    print(f"LAB WATCHER ATTIVO")
    print(f"Sessione: {session_id}")
    print(f"Cartella: {session_dir}")
    print(f"Poll: ogni {poll_interval}s | Max rounds: {max_rounds}")
    print(f"Dry run: {dry_run}")
    print(f"{'='*60}")
    print(f"\nIn attesa della prima bozza di Gemini...")
    print(f"  (Gemini deve scrivere: {session_dir / 'gemini_draft_01.md'})\n")

    last_processed_draft = 0
    last_processed_review = 0

    while True:
        try:
            # Controlla se c'e' un FINAL.md (sessione conclusa)
            if (session_dir / "FINAL.md").exists():
                print("\n[OK] FINAL.md trovato. Sessione conclusa.")
                prepare_for_notaio(session_dir, session_id)
                notify_carlo(session_dir, session_id, "PRONTO_PER_NOTAIO",
                             "Il dialogo Gemini-Claude e' concluso.\n"
                             "Il file per il notaio e' pronto in workspace/for_notaio/.\n"
                             "Apri la chat Opus e digli 'certifica " + session_id + "'.")
                break

            # Controlla nuove bozze di Gemini
            latest_draft, draft_num = find_latest_file(session_dir, "gemini_draft")
            if latest_draft and draft_num > last_processed_draft:
                print(f"\n[NUOVA BOZZA] {latest_draft.name} rilevata!")

                if draft_num > max_rounds:
                    print(f"[LIMITE] Raggiunto max rounds ({max_rounds}). Stop.")
                    notify_carlo(session_dir, session_id, "MAX_ROUNDS",
                                 f"Raggiunto il limite di {max_rounds} rounds senza convergenza.")
                    break

                # Raccogli review precedenti
                previous_reviews = sorted(session_dir.glob("claude_review_*.md"))

                # Costruisci prompt e chiama Claude
                prompt = build_review_prompt(
                    latest_draft, draft_num, session_id, previous_reviews,
                    session_dir=session_dir
                )
                print(f"[CLAUDE] Generando review #{draft_num:02d}...")
                review_text = call_claude(prompt, dry_run=dry_run)

                if not review_text:
                    print("[ERRORE] Claude non ha restituito risposta. Riprovo al prossimo ciclo.")
                    time.sleep(poll_interval)
                    continue

                # Salva la review
                review_path = session_dir / f"claude_review_{draft_num:02d}.md"
                review_path.write_text(review_text, encoding="utf-8")
                print(f"[CLAUDE] Review salvata: {review_path.name}")

                # Controlla esito
                verdict = extract_verdict(review_text)
                print(f"[ESITO] {verdict}")

                if verdict == "APPROVO":
                    # Claude approva: crea FINAL.md dalla bozza
                    final_content = latest_draft.read_text(encoding="utf-8-sig")
                    (session_dir / "FINAL.md").write_text(
                        f"# VERSIONE FINALE APPROVATA\n"
                        f"**Approvata da Claude review #{draft_num:02d}**\n"
                        f"**Data**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                        f"---\n\n{final_content}",
                        encoding="utf-8",
                    )
                    print("[OK] FINAL.md creato. Prossimo ciclo preparera' il file per il notaio.")

                last_processed_draft = draft_num

            time.sleep(poll_interval)

        except KeyboardInterrupt:
            print("\n[STOP] Watcher fermato da utente.")
            break
        except Exception as e:
            print(f"[ERRORE] {e}")
            time.sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(description="ETG Studio - Lab Watcher")
    parser.add_argument("session", help="ID sessione (es: SESSION_001)")
    parser.add_argument("--poll", type=int, default=5, help="Intervallo poll in secondi (default: 5)")
    parser.add_argument("--max-rounds", type=int, default=10, help="Max rounds dialogo (default: 10)")
    parser.add_argument("--dry-run", action="store_true", help="Non chiama Claude, usa risposte mock")
    args = parser.parse_args()

    watch_session(args.session, args.poll, args.max_rounds, args.dry_run)


if __name__ == "__main__":
    main()
