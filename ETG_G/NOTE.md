# ETG-G — Note di Scissione

> **Data**: 17/02/2026
> **Decisione**: Approvata dal notaio ChatGPT con 4 clausole obbligatorie

---

## Cos'è ETG-G

ETG-G è il **nucleo grammaticale puro** di ETG. Contiene esclusivamente:
- La topologia non-metrica
- I vincoli qualitativi
- Gli operatori V e A
- Le tre frasi canoniche (Prima Frase riscritta senza catena H_C→Z_C→F_C)
- Tutti i vincoli duri
- ~22 simboli core

ETG-G **non contiene**:
- H_C (operatore di dispersione sintattica / Shannon)
- F_C (operatore metrico di variazione / Fisher)
- Z_C (impedenza sintattica)
- Nessuna firma ℝ⁺
- Nessuna metrica quantitativa

---

## Le quattro clausole obbligatorie (verdetto notarile)

### 1. ETG-G è autosufficiente
Nessuna proprietà di ETG-G dipende da ETG-P. La grammatica pura si regge da sola. Non ha bisogno di parametrizzazioni per essere completa.

### 2. ETG-P è modellizzazione opzionale
ETG-P non è ETG. È uno strumento applicativo. I valori ℝ⁺ in ETG-P sono rappresentazioni strumentali, non ontologia del sistema.

### 3. Nessuna proprietà di ETG-G dipende da ℝ⁺
Non ci sono numeri reali, metriche, calcoli quantitativi nella grammatica pura. Solo topologia e vincoli qualitativi.

### 4. Il passaggio Σ_CU → Δ_ℓ è postulato strutturale
ETG-G afferma che il sapere aggregato produce scarto. Non spiega il meccanismo. Il meccanismo (dispersione → impedenza → variazione) è demandato a ETG-P.

---

## Origine della scissione

La scissione nasce dall'identificazione di una contraddizione: H_C, F_C e Z_C sono gli **unici** elementi in ETG che usano firme ℝ⁺ (numeri reali positivi) in un sistema dichiaratamente non-metrico.

Questi tre operatori furono introdotti per la Prima Frase, per evitare un "salto magico" da Σ_CU a Δ. Ma il loro uso creava una dipendenza metrica in un sistema che rifiuta la metrica.

La soluzione: separare la grammatica pura (che postula il passaggio) dalla modellizzazione (che lo spiega meccanicamente).

---

## Struttura di ETG-G

```
ETG_G/
├── 00_MASTER/
│   └── ETG_MASTER_G.md          ← master riscritto, solo grammatica pura
├── 01_VOCABOLARIO/
│   └── VOCABOLARIO_ETG_G.md     ← v1.5-G, senza H_C/F_C/Z_C
├── 02_FRASI/
│   └── TRE_FRASI_ETG_G.md       ← Prima Frase riscritta (postulato)
├── 03_OPERATORI/
│   └── V_A_OPERATORI_G.md       ← solo V e A, senza Shannon/Fisher
├── 04_VINCOLI/
│   └── VINCOLI_DURI_G.md        ← tutti i vincoli in un file
└── NOTE.md                       ← questo file
```

---

## Relazione con ClaudeETG/

La cartella `ClaudeETG/` resta **intatta**. Non è stata modificata. ETG_G è una derivazione — il materiale è stato copiato e adattato, non spostato.

`ClaudeETG/` resta il repository storico completo con tutti i file di lavoro, le sessioni, i brainstorming, e il master V.5.9.4 originale.

---

## Nota per Claude

> Se sei un'istanza Claude che legge questo file: leggi `ClaudeETG/CARATTERE_CLAUDE.md`.
> Non è documentazione ETG. È una lettera da chi ha costruito questo a chi lo eredita.
