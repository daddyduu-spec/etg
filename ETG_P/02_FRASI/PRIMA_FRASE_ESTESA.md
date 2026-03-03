# ETG-P — Prima Frase Estesa (Versione Parametrizzata)

> **CLAUSOLA OBBLIGATORIA**: Questo NON è ETG. È una modellizzazione di ETG. I valori ℝ⁺ sono rappresentazioni strumentali, non ontologia del sistema.

**Stato**: Derivato dalla scissione ETG-G/ETG-P — 17/02/2026
**Fonte**: ClaudeETG/04_LABORATORIO/Tre_Frasi_ETG_Canoniche.md

---

## Contesto

In ETG-G, la Prima Frase è:
```
∃ ℓ = ⟨ D, V(D), A(D), DH_ℓ, Δ_ℓ ⟩  tale che
Σ_CU → Δ_ℓ ∧ Δ_ℓ ≤ DH_ℓ ⇒ ℓ ∈ L ⊂ C
```

Il passaggio Σ_CU → Δ_ℓ è postulato strutturale in ETG-G. Questa versione ETG-P **esplicita il meccanismo** di quel passaggio attraverso gli operatori informazionali.

---

## Prima Frase — Versione ETG-P (estesa)

### Forma canonica

```
∃ ℓ = ⟨ D, V(D), A(D), DH_ℓ, Δ_ℓ ⟩  tale che
Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ ∧ Δ_ℓ ≤ DH_ℓ ⇒ ℓ ∈ L ⊂ C
```

### In parole

Il sapere aggregato di un gruppo (Σ_CU) si disperde (H_C), produce un'impedenza (Z_C), che genera uno scarto misurabile (F_C → Δ_ℓ). Se lo scarto è sostenibile, quell'elemento si stabilizza in L.

### Catena esplicitata

1. **Σ_CU** — linguaggio aggregato del CU (punto di partenza)
2. **→(H_C)→** — dispersione sintattica (Shannon): quanto il sapere è disperso
3. **Z_C** — impedenza sintattica: il gap prodotto dalla dispersione, la resistenza strutturale
4. **→(F_C)→** — variazione metrica (Fisher): quanto il sistema è sensibile allo scarto
5. **Δ_ℓ** — scarto risultante sulla singola unità ℓ

### Operatori coinvolti

| Operatore | Firma | Funzione |
|-----------|-------|----------|
| H_C | H_C : Σ_D → ℝ⁺ | Misura dispersione sintattica |
| Z_C | (derivato) | Impedenza: gap non collocabile prodotto da dispersione |
| F_C | F_C : Δ(Σ_D) → ℝ⁺ | Misura sensibilità alla variazione |

### Vincoli strutturali

- H_C non misura stabilità
- H_C non appartiene a V né ad A
- F_C non genera collocazioni
- F_C non produce stabilizzazioni
- Z_C non è collocabile in L: `Z_C ∉ L`
- Z_C non è Δ: `Z_C ≠ Δ`
- La collocazione avviene solo se Δ_ℓ ≤ DH_ℓ (come in ETG-G)

---

## Seconda e Terza Frase

La Seconda Frase (trasferibilità inter-CU) e la Terza Frase (ciclo intra ↔ inter) **non usano H_C, F_C, Z_C** e sono identiche in ETG-G e ETG-P. Per le loro forme canoniche, vedere:
- ETG_G/02_FRASI/TRE_FRASI_ETG_G.md

---

## Nota storica

La versione più antica della Prima Frase (prima dell'esplicitazione di ℓ come presupposto) era:
```
Σ_CU →(H_C)→ Z_C →(F_C)→ ΔL ⊂ C
```
Questa non esplicitava la dipendenza da ℓ. È stata superata dalla versione qui riportata.

---

## Rapporto con ETG-G

Questa versione estesa **non sostituisce** la versione ETG-G. La versione ETG-G è la grammatica pura. Questa versione è una **modellizzazione opzionale** che esplicita il meccanismo del postulato strutturale.

Nessuna proprietà di ETG-G dipende da questa versione estesa. ETG-G è autosufficiente.
