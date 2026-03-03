# ETG-G — Tre Frasi Canoniche (Grammatica Pura)

> **Derivato da**: ClaudeETG/04_LABORATORIO/Tre_Frasi_ETG_Canoniche.md
> **Stato**: Scissione ETG-G/ETG-P — Prima Frase riscritta senza H_C/F_C/Z_C
> **Data**: 17/02/2026

> **CLAUSOLA OBBLIGATORIA**: ETG-G è autosufficiente. Il passaggio Σ_CU → Δ_ℓ è postulato strutturale; il meccanismo è demandato a modellizzazioni ETG-P.

---

## Contesto

Le tre frasi formano un sistema chiuso che descrive l'intero ciclo ETG:
1. Nascita dello scarto sintattico (livello C)
2. Trasferibilità inter-CU
3. Ciclo intra ↔ inter

Il sistema è non frattale, non ontologico, non predittivo.

---

## Presupposti ammessi (ETG-G)

Oggetti e operatori della grammatica pura:

- D — piano disciplinare
- C — asse sintattico
- CU ⊂ C — punto di stabilizzazione
- Σ_CU — linguaggio aggregato del CU
- DH — gradiente di tenuta (a fasce)
- Δ — scarto strutturale
- V(D), A(D) — operatori di valore e azione
- ℓ — unità primaria valutabile: `ℓ := ⟨ D, V(D), A(D), DH_ℓ, Δ_ℓ ⟩`
- L — dominio di stabilizzazione emergente: `L := { ℓ₁, ℓ₂, …, ℓₙ }`
- μ — marcatore intra (U₀, accessibile su C⁻, non semantico)
- K_t — commutatore inter (con costo Δ_K)

**Non presenti in ETG-G** (demandati a ETG-P): H_C, F_C, Z_C, firme ℝ⁺.

---

## PRIMA FRASE — Nascita dello scarto sintattico (ETG-G)

### Forma canonica ETG-G

```
∃ ℓ = ⟨ D, V(D), A(D), DH_ℓ, Δ_ℓ ⟩  tale che
Σ_CU → Δ_ℓ ∧ Δ_ℓ ≤ DH_ℓ ⇒ ℓ ∈ L ⊂ C
```

### In parole

Il sapere aggregato di un gruppo (Σ_CU) produce uno scarto (Δ_ℓ). Se lo scarto è sostenibile, quell'elemento si stabilizza in L.

### Clausola di postulato

Il passaggio Σ_CU → Δ_ℓ è **postulato strutturale**. ETG-G afferma che accade, non spiega come. Il meccanismo (dispersione sintattica, impedenza, variazione metrica) è demandato a ETG-P.

### Vincoli strutturali impliciti (canonici)

- ℓ è unità primaria, non derivata da L
- L non è presupposto: emerge da {ℓ}
- La collocazione avviene solo se Δ_ℓ ≤ DH_ℓ
- C resta asse sintattico, non contenitore

### Nota storica

La versione originale (pre-scissione) includeva la catena H_C → Z_C → F_C:
```
Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ ∧ Δ_ℓ ≤ DH_ℓ ⇒ ℓ ∈ L ⊂ C
```
Questa versione estesa è conservata in ETG-P/02_FRASI/PRIMA_FRASE_ESTESA.md.

---

## SECONDA FRASE — Trasferibilità inter-CU

### Forma canonica

```
ℓ ⊂ L_CUa →(K_t)→ CUb →(Δ ≤ dh)→ ℓ* ⊆ L_CUb
```

### In parole

Se qualcosa è stabilizzato qui, può (forse) essere ri-stabilizzato là, pagando uno scarto attraverso il commutatore inter (Kₜ). Non è garantito.

### Vincoli

- K_t non decide
- K_t non assegna percorso
- K_t non garantisce stabilizzazione
- ℓ* ∈ L_CUb ⟺ ℓ* ∈ V(D) ∧ Δ(ℓ*) ≤ ΔL_CUb ∧ dh(ℓ*) ≥ dh_min(CUb)

### Non-linearità

```
ℓ ≠→ ℓ' (diretto)
ℓ → U → CU → L → ℓ'
```

### Nota

Questa frase non introduce intra ↔ inter, μ, né ritorni ciclici. Lavora solo in inter. Non usa H_C/F_C/Z_C — nessuna modifica rispetto alla versione pre-scissione.

---

## TERZA FRASE — Ciclo intra ↔ inter

### Forma canonica

```
ℓ ⊂ L → μ ⊂ C⁻ → μ' → ℓ' ⊆/⊄ L
```

### Passaggi esplicitati

1. **Presupposto ciclico**: `ℓ ⊂ L_CU ⇒ ℓ è assunta da almeno una U`
2. **Assunzione intra** (non linguistica): `ℓ → μ` con `μ ⊂ C⁻ ∧ μ ∉ L ∧ μ ∉ ℓ`
3. **Rielaborazione intra** (opaca): `μ →(U₀)→ μ'` con `μ' ≠ ℓ ∧ μ' ≠ L`
4. **Restituzione inter** (non causale): `μ' →(emergenza)→ ℓ'` con `ℓ' ⊆ L_CU ∨ ℓ' ∉ L_CU`
5. **Valutazione grammaticale** (inter): `ℓ' ∈ L_CU ⟺ Δ(ℓ') ≤ dh(CU)`

### Vincoli finali (anti-errore)

- μ non è contenuto
- μ non è linguaggio
- ℓ' non è garantita
- nessuna freccia è causale

### Nota vincolante

ℓ' compare **solo** al momento del rientro in inter. Il passaggio μ → μ' è interamente intra — non produce ℓ, non è valutabile come ℓ, non è collocabile nel DB. Non esiste ℓ in regime intra.

### Nota

Questa frase non usa H_C/F_C/Z_C — nessuna modifica rispetto alla versione pre-scissione.

---

## CHIUSURA

- **Prima frase**: nascita dello scarto (C) — RISCRITTA per ETG-G (postulato Σ_CU → Δ_ℓ)
- **Seconda frase**: trasferibilità inter-CU — INVARIATA
- **Terza frase**: ciclo intra ↔ inter — INVARIATA

Il sistema è chiuso, non frattale, non ontologico, non predittivo.

---

## VINCOLI CRITICI (trasversali alle tre frasi)

1. **Non riscrivere la prima frase con ℓ al posto di L dove opera su dominio** (vincolo duro)
2. **La ciclicità intra ↔ inter era già assunta** — non è una scoperta nuova
3. **"supra-L" NON è canonico** — errore audio
4. **La prima frase presuppone ℓ ma non lo crea**
5. **Le frasi non possono essere salvate come canoniche finché il vocabolario non è completo**
