# VOCABOLARIO OPERATORI — ETG

> **Fonte**: "Studiare fisica" (studiare_fisica_extracted.txt), righe 119917–119988
> **Stato**: ESTRATTO dal notaio — Attende verdetto notarile per canonizzazione
> **Data estrazione**: 09/02/2026

Versione: canonica (proposta notarile)
Stato: vincolante (se approvato)

---

## Sezione B — Operatori grammaticali

> Questi agiscono, ma non producono contenuto.

---

### V — Operatore di Valore

**Definizione**:
```
V : D → ℘(Σ_D)
```

Determina quali configurazioni sono significative in un piano D.
Non determina verità. Non è semantica.

**Vincoli**:
- V(D₁) ∩ V(D₂) = ∅ salvo traduzione esplicita
- V non è auto-applicabile

---

### A — Operatore di Azione

**Definizione**:
```
A : D → ℘(𝒯_D)
```

Determina quali trasformazioni sono ammissibili in un piano D.
Limitato da Δ e DH.

**Vincoli**:
- A(D) ⊆ trasformazioni compatibili con V(D)
- A non è prescrittivo

---

### Δ — Operatore di Variazione

**Definizione**:
```
Δ : L → L'
```

Δ agisce su domini di stabilizzazione.
Non genera contenuto. Non genera nuove L.

**Vincolo**:
```
Δ(L) ≤ DH_L
```

---

### H — Operatore di Dispersione (Shannon)

**Definizione**:
```
H_D : Σ_D → ℝ⁺
```

Misura dispersione sintattica.
Non misura stabilità.
Non appartiene a V né A.

---

### F — Operatore Metrico (Fisher)

**Definizione**:
```
F_D : Δ(Σ_D) → ℝ⁺
```

Misura sensibilità alla variazione.
Strumento comparativo.
Non genera collocazioni.

---

## NOTA

Questi operatori sono stati formalizzati nella sessione che ha portato alla "prima frase ETG".
Per i vincoli d'uso nelle frasi ETG → vedere Tre_Frasi_ETG_Canoniche.md
