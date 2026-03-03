# PROTOCOLLO AUDIO ETG

> **Versione**: 1.0
> **Data**: 11/02/2026
> **Origine**: Sessione Sonnet su Claude.ai, ricreato in ClaudeETG da Opus 4.6
> **Scopo**: Gestire interazioni vocali con terminologia ETG, evitando ambiguità e errori storici.

---

## Premessa

ETG ha terminologia precisissima: ℓ vs L, σ vs S, ε vs E. Ha simboli speciali (⦿, μ, ᚦ). Ha errori storici nati da audio ("supra-L" era trascrizione sbagliata). Serve un protocollo per evitare che l'input vocale generi nuovi errori.

---

## 1. Convenzioni verbali obbligatorie

Ogni simbolo ETG ha una pronuncia canonica. Vedi `LEGGENDA_FONETICA.md` per la tabella completa.

Regola base: **SEMPRE specificare maiuscolo/minuscolo** per lettere che hanno doppia valenza (L/ℓ, S/σ).

---

## 2. Regole di validazione

### Regola 1 — Conferma automatica per termini ambigui

Quando l'input audio contiene un termine che potrebbe riferirsi a più di un simbolo ETG, l'AI **deve** chiedere conferma prima di procedere.

Esempio:
```
Input audio: "aggiungi elle al file"
Risposta AI:
  [AUDIO] Ho capito: "aggiungi elle al file"
  Confermi che intendi:
  - [ ] ℓ (elle minuscolo corsivo — unità di stabilizzazione)
  - [ ] L (L maiuscolo — dominio di stabilizzazione)
```

### Regola 2 — Segnalazione termini non canonici

Se l'input audio contiene un termine superato o non canonico, l'AI **deve** segnalarlo.

Esempio:
```
Input audio: "metti supra-L nel file"
Risposta AI:
  [AUDIO] ATTENZIONE: "supra-L" NON è termine canonico.
  È stato confermato come errore di trascrizione audio.
  Intendevi forse: "spazio sopra L" o "L tratteggiata"?
```

### Regola 3 — Ripetizione prima di operazioni critiche

Prima di modificare file canonici (MASTER, VOCABOLARIO, file in 04_LABORATORIO), l'AI **deve** ripetere il comando interpretato e attendere conferma esplicita.

```
Input audio: "correggi la formula di CU nel vocabolario"
Risposta AI:
  [AUDIO] Operazione critica richiesta.
  Ho capito: modificare la voce CU nel VOCABOLARIO_ETG_COMPLETO.md
  Confermi? (sì/no)
```

---

## 3. Termini vietati (errori storici)

Questi termini **non devono mai essere accettati** senza segnalazione:

| Termine audio | Errore | Termine corretto |
|---------------|--------|------------------|
| "supra-L" | Trascrizione audio errata | "spazio sopra L" (nome non fissato) |
| "L meno" | Non canonico | "L tratteggiata" |
| "Cre" | Ordine lettere sbagliato | "Cer" (canale inter) |
| "W" | Simbolo eliminato | (assorbito, non più in uso) |
| "thurisaz come fissazione" | Confusione ruoli | ⦿ = fissazione, ᚦ = lemma umano post-assunzione |
| "PLANE-D" | Terminologia Keep superata | "D" (piano disciplinare) |
| "SPIN" | Terminologia Keep superata | "K" (commutatore) |
| "OCB" | Terminologia Keep superata | "Kₜ" (commutatore inter) |

---

## 4. Workflow audio

```
1. Carlo parla (input audio)
2. AI trascrive
3. AI verifica:
   a. Termini ambigui? → Regola 1 (conferma)
   b. Termini vietati? → Regola 2 (segnalazione)
   c. Operazione critica? → Regola 3 (ripetizione + conferma)
4. AI procede solo dopo conferma
```

---

## 5. Esempio completo

### Buono
```
Carlo: "aggiungi una nota su elle minuscolo corsivo nella sezione E del vocabolario"
AI: [AUDIO] Ho capito: aggiungere nota su ℓ (unità di stabilizzazione) in Sezione E.
     File: VOCABOLARIO_ETG_COMPLETO.md
     Operazione critica — confermi?
Carlo: "sì"
AI: [procede]
```

### Cattivo
```
Carlo: "aggiungi elle al file"
AI: [procede a modificare senza chiedere se ℓ o L]
→ ERRORE: violazione Regola 1
```
