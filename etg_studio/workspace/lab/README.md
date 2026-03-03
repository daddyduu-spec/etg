# workspace/lab/

Spazio di dialogo Gemini ↔ Claude per sessioni ETG-P.

## Convenzione nomi file

```
SESSION_<id>/
  gemini_draft_01.md      ← prima bozza Gemini
  claude_review_01.md     ← review di Claude
  gemini_draft_02.md      ← revisione Gemini
  claude_review_02.md     ← secondo feedback Claude
  ...
  FINAL.md                ← versione finale approvata da Claude
```

## Regole
- Gemini scrive SOLO file `gemini_draft_*.md`
- Claude scrive SOLO file `claude_review_*.md` e `FINAL.md`
- I numeri sono progressivi (01, 02, 03...)
- `FINAL.md` = Claude ritiene il risultato coerente e pronto per il notaio
- Nessuno dei due tocca ETG_P/ — quello lo fa Claude DOPO la certificazione
