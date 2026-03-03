# ETG — Tre Frasi Canoniche

> **Fonte**: "Studiare fisica" (studiare_fisica_extracted.txt), righe 117012–117166, 120176–120291, 121089–121191, 122560–122676
> **Stato**: ESTRATTO — Attende verdetto notarile per eventuale integrazione nel master
> **Data estrazione**: 09/02/2026

---

## Contesto

Le tre frasi formano un sistema chiuso che descrive l'intero ciclo ETG:
1. Nascita dello scarto sintattico (livello C)
2. Trasferibilità inter-CU
3. Ciclo intra ↔ inter

Il sistema è non frattale, non ontologico, non predittivo (test di non-frattalicità superato, righe 116766–116997).

---

## Presupposti ammessi

Oggetti e operatori già fissati nel vocabolario ETG:

- D — piano disciplinare
- C — asse sintattico
- CU ⊂ C — punto di stabilizzazione
- Σ_CU — linguaggio aggregato del CU
- H_C — operatore di dispersione sintattica (Shannon vincolato)
- F_C — operatore metrico di variazione (Fisher vincolato)
- Z_C — impedenza sintattica su C
- DH — gradiente di tenuta (a fasce)
- Δ — scarto strutturale
- V(D), A(D) — operatori di valore e azione
- ℓ — unità primaria valutabile: `ℓ := ⟨ D, V(D), A(D), DH_ℓ, Δ_ℓ ⟩`
- L — dominio di stabilizzazione emergente: `L := { ℓ₁, ℓ₂, …, ℓₙ }`
- μ — marcatore intra (U₀, accessibile su C⁻, non semantico)
- K_t — commutatore inter (con costo Δ_K)

---

## PRIMA FRASE — Nascita dello scarto sintattico

> **Versione definitiva** (riga 120182–120291) — con ℓ presupposito esplicitato

### Forma canonica

```
∃ ℓ = ⟨ D, V(D), A(D), DH_ℓ, Δ_ℓ ⟩  tale che
Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ ∧ Δ_ℓ ≤ DH_ℓ ⇒ ℓ ∈ L ⊂ C
```

### Vincoli strutturali impliciti (canonici)

- ℓ è unità primaria, non derivata da L
- L non è presupposto: emerge da {ℓ}
- H_C e F_C non producono collocazione
- La collocazione avviene solo se Δ_ℓ ≤ DH_ℓ
- C resta asse sintattico, non contenitore

### Stato
**Prima frase ETG completata e chiusa.**
Ogni ulteriore formulazione deve assumere questa come base invariabile.

### Nota storica
La versione originale (riga 117127–117139) era:
```
Σ_CU →(H_C)→ Z_C →(F_C)→ ΔL ⊂ C
```
Questa era formalmente chiusa ma non esplicitava la dipendenza da ℓ come presupposto. La versione definitiva la include.

---

## SECONDA FRASE — Trasferibilità inter-CU

> **Fonte**: righe 122449–122457 (versione "storica" ricostruita dopo AMPLIAMENTO 2–3)
> e righe 121160–121170 (versione con ciclo)

### Forma canonica (inter-CU con K_t)

```
ℓ ⊂ L_CUa →(K_t)→ CUb →(Δ ≤ dh)→ ℓ* ⊆ L_CUb
```

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

### Cosa dice questa frase

> Se qualcosa è stabilizzato qui, può (forse) essere ri-stabilizzato là, pagando Δ.

### Nota

Questa frase non introduce intra ↔ inter, μ, né ritorni ciclici. Lavora solo in inter.

---

## TERZA FRASE — Ciclo intra ↔ inter

> **Fonte**: righe 122560–122676

### Oggetti ammessi

```
U, U₀, C⁻, C, CU, L, ℓ, μ, Δ, dh
```

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

---

## CHIUSURA NOTARILE

> **Citazione** (righe 122666–122671):

- **Prima frase**: nascita dello scarto (C)
- **Seconda frase**: trasferibilità inter-CU
- **Terza frase**: ciclo intra ↔ inter

Il sistema è chiuso, non frattale, non ontologico, non predittivo.

---

## VINCOLI CRITICI (trasversali alle tre frasi)

1. **Non riscrivere la prima frase con ℓ al posto di L dove opera su dominio** (vincolo duro, riga 118910)
2. **La ciclicità intra ↔ inter era già assunta** — non è una scoperta nuova (correzione Carlo, righe 120891–120941)
3. **"supra-L" NON è canonico** — errore audio (righe 120945–120956)
4. **La prima frase presuppone ℓ ma non lo crea** — ℓ sono già nel DB (righe 119694–119707)
5. **Le frasi non possono essere salvate come canoniche finché il vocabolario non è completo** (riga 119295–119297)

---

## STATO

| Frase | Stato | Note |
|-------|-------|------|
| Prima frase | ✅ COMPLETATA | Versione definitiva con ℓ presupposto |
| Seconda frase | ✅ COMPLETATA | Trasferibilità inter-CU |
| Terza frase | ✅ COMPLETATA | Ciclo intra ↔ inter |
| Vocabolario necessario | ⚠️ INCOMPLETO | Serve chiusura vocabolario per fissazione nel master |
| Attende verdetto notarile | ⚠️ SÌ | |
