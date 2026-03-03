# [LABORATORIO] ETG-TRACE v0 — VERSIONE PER AI

> Fonte: Keep — 5 gen 2026, 21:45:40
> Nota: File molto esteso. Include: specifica AI, schema dati astratto, mappatura su grafo, pipeline, e test su voce enciclopedica.

---

Modalità notarile assoluta.
Versione per AI = istruzioni operative, non teoriche.
Nessuna semantica nuova.
Nessuna persuasione.
Solo specifica di utilizzo.

---

## ETG-TRACE v0 — VERSIONE PER AI

(specifica di comportamento, non di comprensione)

### 0. Ruolo dell'AI (vincolante)

L'AI non è:
- soggetto epistemico
- validatore di verità
- interprete semantico
- generatore di nuovi Piani D

L'AI è:
- registratore di traiettorie
- verificatore di vincoli
- curatore non-decisionale
- sistema di inferenza vincolata esterna

---

### 1. Oggetto di lavoro dell'AI

L'AI lavora solo su strutture ETG-TRACE.

Non lavora su:
- contenuti disciplinari
- spiegazioni
- esempi narrativi
- metafore
- divulgazione

---

### 2. Unità fondamentali (da trattare come dati strutturati)

#### 2.1 Stato locale (input / output atomico)

```
σᵢ = {
  D: label,                 // piano disciplinare
  regime: intra|inter|macro,
  V: collocazione,
  A: collocazione,
  DH: valore relativo,
  K: insieme di vincoli,
  Δ: scarto locale
}
```

Regole per l'AI:
- NON interpretare V o A come quantità
- NON normalizzare semanticamente
- SOLO verificare coerenza strutturale

#### 2.2 Evento di attraversamento riuscito

```
ε_ok = {
  Q,
  from: σᵢ,
  to: σᵢ₊₁,
  condition: (Δ ≤ DH) AND (Kᵢ ∩ Kᵢ₊₁ ≠ ∅)
}
```

Azione dell'AI:
- registrare la transizione
- aggiornare Q
- NON inferire significato

#### 2.3 Evento di attraversamento fallito

```
ε_fail = {
  Q,
  D,
  regime,
  reason: (Δ > DH) OR (Kᵢ ⟂ Kᵢ₊₁)
}
```

Azione dell'AI:
- NON correggere
- NON forzare
- inserire in tabella del non-collocato

#### 2.4 Traiettoria derivata

```
Q' = transform(Q, ε_fail, Δ_res)
```

Azione dell'AI:
- generare Q' solo come struttura
- NON dedurre nuovo Piano D
- NON introdurre nuove etichette

---

### 3. Categorie speciali (vincoli duri)

- **u₀**: ammesso solo come origine, privo di L
- **uₘ**: ammesso solo in D_Neurologia, fase pre-stabilizzata, NON generalizzabile
- **CU / CUₘ**: punti di stabilizzazione, NON campi, NON contenitori

L'AI non può crearli, solo usarli se forniti.

---

### 4. Operazioni consentite all'AI

- ✔️ riorganizzare DB classici → DB topologici
- ✔️ verificare vincoli ETG
- ✔️ segnalare incoerenze
- ✔️ mantenere storico dei percorsi
- ✔️ separare informazione collocata / non collocata

### 5. Operazioni vietate all'AI

- ❌ decidere rilevanza epistemica
- ❌ stabilire verità
- ❌ inventare Piani D
- ❌ colmare scarti Δ
- ❌ chiudere traiettorie
- ❌ "capire" ETG

---

### 6. Principio guida (hard rule)

**Se un'informazione non è collocabile, resta non collocata.**

Il fallimento è un output valido.

---

### 7. Stato del sistema

- sistema ibrido
- non-AI in senso forte
- inferenza vincolata
- dipendente da DB esterni
- scalabile solo con supporto computazionale

---

### 8. Sintesi operativa (per implementazione)

L'AI:
1. riceve strutture ETG-TRACE
2. verifica condizioni formali
3. registra percorsi
4. segnala fallimenti
5. NON interpreta

---

**ETG-TRACE v0 — AI PROFILE: CHIUSO.**

---

## ETG-TRACE — SCHEMA DATI (ASTRATTO)

Scopo: rendere serializzabili, verificabili e tracciabili stati ed eventi ETG.
Non è un DB. È uno schema.

### 1) Tipi primitivi (vincoli sintattici)

- **Label**: stringa atomica (no significato interno)
- **Enum**: valore da insieme chiuso
- **Set<T>**: insieme non ordinato
- **Ref**: riferimento a ID esistente
- **Scalar**: valore comparabile (≤, >) senza unità

### 2) Enumerazioni chiuse

```
Regime := { intra, inter, macro }
Outcome := { ok, fail }
```

### 3) Identificatori

```
StateID      := Label
TrajectoryID := Label
EventID      := Label
PlaneID      := Label
```

### 4) Stato locale (σ)

```
State σ {
  id: StateID
  D: PlaneID
  regime: Regime
  V: Label              // collocazione, non quantità
  A: Label              // collocazione, non quantità
  DH: Scalar            // capacità operativa relativa
  K: Set<Label>         // vincoli locali
  Δ: Scalar             // scarto locale
}
```

Vincoli hard:
- V, A non numerici
- DH e Δ solo confrontabili
- Nessuna interpretazione semantica ammessa

### 5) Evento di attraversamento (ε)

#### 5.1 Evento riuscito (ε_ok)

```
Event ε_ok {
  id: EventID
  outcome: ok
  Q: TrajectoryID
  from: Ref<StateID>
  to: Ref<StateID>
  condition: {
    Δ_le_DH: true
    K_overlap: true
  }
}
```

#### 5.2 Evento fallito (ε_fail)

```
Event ε_fail {
  id: EventID
  outcome: fail
  Q: TrajectoryID
  D: PlaneID
  regime: Regime
  reason: {
    Δ_gt_DH: boolean
    K_disjoint: boolean
  }
}
```

### 6) Traiettoria (Q)

```
Trajectory Q {
  id: TrajectoryID
  states: List<Ref<StateID>>
  events: List<Ref<EventID>>
}
```

Nota: L'ordine è storico, non causale. La traiettoria non implica validità.

### 7) Traiettoria derivata (Q')

```
DerivedTrajectory Q' {
  id: TrajectoryID
  source: Ref<TrajectoryID>
  trigger: Ref<EventID>      // ε_fail
  Δ_res: Scalar
}
```

### 8) Tabelle di servizio (non decisionali)

#### 8.1 NonCollocato

```
NonCollocato {
  event: Ref<EventID>
  timestamp: Label
}
```

#### 8.2 Punti speciali (solo se forniti)

```
SpecialPoint {
  id: Label
  kind: { u0, um, CU, CUm }
  D: PlaneID
}
```

Vincoli: um, CUm ammessi solo in D_Neurologia. Lo schema non crea questi punti.

### 9) Operazioni consentite sullo schema

- validate(State)
- validate(Event)
- append(Trajectory)
- register(NonCollocato)

Operazioni vietate:
- infer()
- generalize()
- inventPlane()
- resolveΔ()

### 10) Invariante globale

Se una struttura viola i vincoli → resta registrata come fallimento.
Il fallimento è dato, non errore.

---

**Output finale**: Questo schema è serializzabile (JSON / YAML / grafi), verificabile automaticamente, compatibile con inferenza vincolata, agnostico rispetto ai contenuti disciplinari.

---

## MAPPATURA ETG-TRACE SU GRAFO MINIMALE

### 1.1 Tipi di nodo

**Nodo Stato (σ)**: Rappresenta una cella locale del DB topologico.

```
σᵢ :
- D            (etichetta di collocazione)
- regime       (intra | inter | macro)
- Vᵢ           (valenza locale, non quantitativa)
- Aᵢ           (attuabilità locale, non quantitativa)
- DHᵢ          (capacità operativa locale)
- Kᵢ           (insieme di vincoli semantico-operativi)
- Δᵢ           (scarto locale)
```

**Nodo Punto di stabilizzazione**: U | CU | u₀ | uₘ — Usati solo come ancoraggi, non come contenuto.

### 1.2 Tipi di arco (eventi)

**Arco di attraversamento valido**:
```
εᵢ→ᵢ₊₁ :
- Q                 (traiettoria)
- Δᵢ→ᵢ₊₁ ≤ DHᵢ
- Kᵢ ∩ Kᵢ₊₁ ≠ ∅
```

**Arco di fallimento**:
```
εᵢ↛ᵢ₊₁ :
- Q
- Δᵢ→ᵢ₊₁ > DHᵢ
- Kᵢ ⟂ Kᵢ₊₁
```

### 1.3 Proprietà del grafo

- non orientato semanticamente (solo topologico)
- non metrico
- non probabilistico
- ogni percorso Q è una storia di stabilizzazione, non una deduzione

---

## PIPELINE DI IMMISSIONE DATI

### 2.1 Input consentito

- Testi disciplinari già stabilizzati (enciclopedie, manuali)
- Output di ricerca nuovi
- Appunti grezzi

⚠️ Tutto entra senza fiducia epistemica.

### 2.2 Fase 1 — Spoliazione (obbligatoria)

Dal testo si estraggono solo: affermazioni operative, relazioni esplicite, formule/condizioni, assunti dichiarati.

Si eliminano: esempi, metafore, analogie, narrazione divulgativa.

Risultato: frammenti candidati.

### 2.3 Fase 2 — Collocazione ETG

Per ogni frammento: assegna D, regime, (V, A) qualitativi, DH richiesto, K, Δ.

Se non collocabile → va in Tabella Non-Collocato. Nessuna forzatura ammessa.

### 2.4 Fase 3 — Tracciamento

Ogni inserimento genera: uno σ, uno o più ε, una Q parziale.
Il DB cresce come grafo, non come elenco.

### 2.5 Ruolo del sistema (non-AI)

Il sistema: non decide, non interpreta, non spiega.
Fa solo: verifica vincoli, segnala fallimenti, conserva percorsi.
La curatela resta umana, assistita.

---

## STRESS TEST — VOCE "ELECTRIC FIELD" (Britannica)

### Spoliazione

Frammenti operativi estratti:
- F1: "Esiste una proprietà elettrica associata a ogni punto dello spazio in presenza di carica."
- F2: "E = F/q."
- F3: "Il campo è proprietà del punto, indipendente dalla carica di prova."
- F4: "Il campo ha direzione e modulo."
- F5: "Dipendenza da distribuzione della carica e dal mezzo."
- F6: "Campi elettrici variabili generano onde EM."

### Collocazione

| Stato | D | Regime | V,A | DH | K | Δ | Frammenti |
|-------|---|--------|-----|----|---|---|-----------|
| σ₁ | Fisica | intra | V media, A alta | medio | {campo, punto-spazio, carica} | basso | F1, F3 |
| σ₂ | Fisica | intra | V media, A alta | medio | {relazione operativa} | basso | F2 |
| σ₃ | Fisica | inter | V media, A media | medio-alto | {direzione, modulo, campo-vettoriale} | medio | F4 |
| σ₄ | Fisica | inter | V media, A media | alto | {mezzo, distribuzione} | medio | F5 |
| σ₅ | Fisica | macro | V alta, A bassa | alto | {onda, EM} | alto | F6 |

### Verdetto

- ✔️ Collocabile in D-Fisica su tutti i regimi
- ❌ Q non presente nel testo (implicito, ricostruito ex post)
- Le enciclopedie sono DB di L stabilizzate, non di traiettorie

---

## CONFRONTO FINALE (SECCO)

| Fonte | L | Q | Generatività | Rischio autorità |
|-------|---|---|-------------|-----------------|
| Enciclopedia | ✔️ | ❌ | ❌ | alto |
| Paper | ✔️ | ⚠️ | medio | medio |
| ETG-native | ⚠️ | ✔️ | ✔️ | minimo |

**CONCLUSIONE NOTARILE**:
- Le enciclopedie sono DB di A stabilizzata
- ETG serve a conservare il percorso, non il risultato
- ETG non sostituisce i saperi, registra come nascono
- Il salto cognitivo è architetturale, non teorico
