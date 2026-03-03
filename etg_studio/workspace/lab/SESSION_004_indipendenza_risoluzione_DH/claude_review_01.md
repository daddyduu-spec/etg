Perfetto. Ho tutti gli elementi per la review. Procedo con la scrittura della valutazione formale.

# Review 01
**Sessione**: SESSION_004
**Bozza**: gemini_draft_01.md
**Data**: 2026-02-27

## Valutazione
- Coerenza col master: PROBLEMI (un termine non canonico)
- Terminologia: PROBLEMI — "Dinamica di Orizzonte" non trovato in nessuna fonte
- Vincoli duri: OK
- Derive creative: SEGNALATE (termine inventato, notazione non standard)

## Termini non canonizzati trovati nelle fonti
Nessuno.

## Problemi trovati

1. **"Dinamica di Orizzonte" (riga 10)** — Termine NON presente in:
   - VOCABOLARIO_ETG_COMPLETO.md (dove DH è definito come "Gradiente di tenuta")
   - ETG_G/VINCOLI_DURI_G.md
   - chatgpt/studiare_fisica_extracted.txt (fonti originali)
   - Nessun altro file della documentazione
   
   Il termine canonico è **"DH (Gradiente di tenuta)"** o semplicemente **"DH"**. "Dinamica di Orizzonte" è un'espansione inventata.
   
   **Dove verificare**: VOCABOLARIO_ETG_COMPLETO.md righe 148-158, PROMPT_RESTART.md riga 179.

2. **Notazione $\Delta_{ETG-P}$ (riga 15)** — Non esiste in nessun file della documentazione. Il simbolo corretto è **$\Delta_\ell$** (delta applicato a elle), come in:
   - ETG_P/02_FRASI/PRIMA_FRASE_ESTESA.md riga 28: `Δ_ℓ`
   - Catena canonica è: `Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ`
   
   $\Delta_{ETG-P}$ suggerisce erroneamente che Delta sia "una cosa di ETG-P", quando invece Delta è un operatore applicato a elle (valido in entrambi ETG-G e ETG-P).
   
   **Dove verificare**: ETG_P/02_FRASI/PRIMA_FRASE_ESTESA.md righe 28, 41.

3. **Formulazione parentetica di DH (riga 12)** — "Gradiente di tenuta" appare tra apici come se fosse un alias o traduzione. Nel vocabolario canonico è la definizione principale, non una glossa.
   
   **Dove verificare**: VOCABOLARIO_ETG_COMPLETO.md riga 148 ("### DH — Gradiente di tenuta").

## Suggerimenti

1. **Riga 10**: Sostituire "Dinamica di Orizzonte ($DH$)" con "$DH$ (Gradiente di tenuta)" oppure semplicemente "$DH$".

2. **Riga 12**: Riformulare da:
   > "$DH$ ('Gradiente di tenuta'), come sancito in ETG-G, è un gradiente qualitativo a fasce..."
   
   a:
   > "$DH$ (Gradiente di tenuta), come sancito in ETG-G, è un gradiente qualitativo a fasce..."

3. **Riga 15**: Sostituire "$\Delta_{ETG-P}$" con "$\Delta_\ell$" per coerenza con la notazione canonica della Prima Frase ETG-P.

4. **Punto positivo**: I tre punti della clausola (righe 13-15) sono logicamente corretti e coprono gli aspetti richiesti dalla condizione 4. Il contenuto semantico è solido.

5. **Collocazione suggerita**: 
   - Inserire la clausola in `ETG_P/NOTE.md` sezione "Stato di implementazione" (aggiornare condizione 4 da ⬜ a ✅)
   - Creare `ETG_P/04_VINCOLI/CLAUSOLA_DISACCOPPIAMENTO_DH_BIT.md` come file autonomo per riferimento permanente

## Esito
**RIVEDI** — Correggere terminologia non canonica prima di sottoporre al notaio.