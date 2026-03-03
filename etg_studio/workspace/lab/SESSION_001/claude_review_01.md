# Review 01
**Sessione**: SESSION_001
**Bozza**: gemini_draft_01.md
**Data**: 2026-02-26

## Valutazione
- Coerenza col master: PROBLEMI
- Terminologia: VIOLAZIONI
- Vincoli duri: VIOLAZIONI
- Derive creative: SEGNALATE

## Problemi trovati

1. **Confusione simbolo L**: La bozza usa "L (Lontananza)" come "distanza dal centro C". Ma in ETG canonico, **L** Ã¨ il **dominio storico emergente** (insieme delle â„“ collocate). Non esiste un concetto canonizzato di "Lontananza" con simbolo L. Questo Ã¨ un neologismo non autorizzato che crea ambiguitÃ  terminologica grave.

2. **DH applicato a â„“ singola come parametro intrinseco**: La proposta parla di "assegnare un valore numerico scalare a ciascun lemma â„“" basato su DH. Ma **DH_â„“** (come da Vocabolario) Ã¨ il "gradiente che â„“ deve superare per essere collocata", non una proprietÃ  intrinseca del lemma. DH_â„“ Ã¨ un **vincolo topologico relazionale**, non un parametro assegnabile a priori.

3. **"Centro di certezza assoluta"**: Questo concetto non esiste in ETG. **C** Ã¨ il campo delle collocazioni possibili, non un "centro di certezza". Non ha struttura metrica. La nozione di "distanza da C" viola la natura topologica pura di ETG-G.

4. **Parametrizzazione [0,1] senza giustificazione**: La bozza propone "scalare puro âˆˆ [0,1]" senza specificare cosa rappresenti questo intervallo rispetto ai vincoli di ETG-P, nÃ© come si colleghi a H_C, F_C, Z_C (gli unici simboli metrici autorizzati in ETG-P).

5. **AmbiguitÃ  su "resistenza tra paradigmi"**: La bozza cita DH come "resistenza o scarto tra paradigmi", ma DH_â„“ in ETG Ã¨ definito come soglia/gradiente per la collocazione di una singola â„“ in C, non come distanza tra paradigmi.

6. **Violazione Vincolo 5**: "V, A, DH, Î” si applicano a â„“, MAI a L". La bozza sembra voler usare DH per costruire una metrica su L (tramite "lontananza"), il che violerebbe questo vincolo diretto.

7. **Manca ancoraggio ETG-P**: La proposta non specifica quale delle tre funzioni autorizzate di ETG-P (H_C, F_C, Z_C) si intende testare. Parla genericamente di "DH" senza collegarsi alla struttura formale `Î£_CU â†’(H_C)â†’ Z_C â†’(F_C)â†’ Î”_â„“`.

## Suggerimenti

1. **Eliminare il simbolo "L (Lontananza)"**: Sostituire con terminologia ETG canonizzata. Se si vuole parlare di distanza topologica, specificare rispetto a cosa (Î£_CU? Una â„“ di riferimento?) e giustificare con simboli ETG-P esistenti.

2. **Chiarire cosa si vuole parametrizzare**: Se l'obiettivo Ã¨ testare il motore 3D, specificare esattamente quale grandezza ETG-P si vuole visualizzare. Candidati canonici: H_C(â„“), Z_C(â„“), o F_C(â„“â†’â„“').

3. **Rivedere l'interpretazione di DH_â„“**: DH_â„“ non Ã¨ un "valore del lemma", ma la soglia che Î”_â„“ deve superare. La frase ETG-G corretta Ã¨: `Î”_â„“ â‰¤ DH_â„“ â‡’ â„“ âˆˆ L`. Non si puÃ² "assegnare DH_â„“ in base a distanza da C".

4. **Giustificare [0,1] con firme ETG-P**: Se si vuole normalizzare, spiegare come [0,1] si ricava da H_C, F_C, Z_C. Esempio: `H_C(â„“) / H_C_max` (ma serve definire H_C_max con vincoli formali).

5. **Riformulare il punto aperto**: Invece di chiedere se "appiattisce ETG-G", chiedere: "Questa parametrizzazione rispetta la separazione ETG-G/ETG-P? Introduce dipendenze metriche nella grammatica pura?"

6. **Ancorare a Prima Frase ETG-P**: Specificare quale passaggio della catena `Î£_CU â†’(H_C)â†’ Z_C â†’(F_C)â†’ Î”_â„“` si vuole testare numericamente.

## Esito
**RIVEDI**

La bozza introduce terminologia non canonizzata (L come Lontananza, centro di certezza), fraintende DH_â„“ come parametro intrinseco invece che vincolo relazionale, e propone una metrica senza ancorarla ai simboli autorizzati di ETG-P. Necessaria revisione completa prima di procedere con test numerici.