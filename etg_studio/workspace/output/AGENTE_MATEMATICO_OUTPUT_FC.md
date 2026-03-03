# Output Agente Matematico — Derivazione F_C
**Data**: 2026-02-28
**Bootloader usato**: BOOTLOADER_MATEMATICO.md (v1 + vincoli Gemini 9-10)

---

## A. Formula proposta per F_C

```
F_C(Z_C, DH_D, DH_ℓ) = Z_C² · (DH_D / DH_ℓ)
```

Espanso con Z_C candidata:

```
Δ_ℓ = [H_C(Σ_CU|D)]² · DH_D / [(DH_D - H_C(Σ_CU|D))² · DH_ℓ]
```

| Simbolo | Tipo | Definizione |
|---------|------|-------------|
| Z_C | ℝ⁺ | Impedenza sintattica = H_C / (DH_D - H_C) |
| DH_D | ℝ⁺ (bit) | Gradiente di tenuta del piano D |
| DH_ℓ | ℝ⁺ (bit) | Gradiente di tenuta dell'unità ℓ |
| H_C | ℝ⁺ (bit) | Dispersione sintattica |

Nessuna costante arbitraria. Nessuna variabile nuova.

---

## B. Derivazione

### Punto di partenza: Fisher Information classica

F(θ) = E[(d/dθ log f(x;θ))²] — misura la curvatura della log-verosimiglianza. Proprietà chiave: quadrato della derivata → F ≥ 0, F = 0 sse nessuna sensibilità, F cresce con la sensibilità.

### Passo 1: Parametro rilevante

Nel contesto ETG-P, il "parametro" è Z_C. La domanda di Fisher: quanto cambia la configurazione sintattica del piano D quando Z_C varia?

### Passo 2: Struttura di Fisher

La Fisher pura sulla distribuzione p_i rispetto a Z_C produce F ~ 1 (non discriminante). Il problema richiede non la Fisher della distribuzione interna, ma la **curvatura della risposta del piano all'impedenza**.

### Passo 3: Costruzione

```
F_C = [sensibilità]² · [fattore di scala]
```

- **Sensibilità** = Z_C (l'impedenza misura quanto il materiale devia dalla norma)
- **Fattore di scala** = DH_D / DH_ℓ (cambio di scala da piano D a unità ℓ)
- Il quadrato proviene dalla struttura di Fisher (quadrato della derivata)
- Il rapporto DH_D/DH_ℓ converte da scala D a scala ℓ

### Passo 4: Giustificazione DH_D/DH_ℓ

- DH_ℓ grande (unità robusta) → scarto ridotto → divisione per DH_ℓ
- DH_D grande (piano ampio) → scarto distribuito proporzionalmente → moltiplicazione per DH_D
- Emerge naturalmente senza costanti arbitrarie

### Passo 5: Verifica dimensionale

Z_C adimensionale (bit/bit), Z_C² adimensionale, DH_D/DH_ℓ adimensionale → F_C adimensionale → Δ_ℓ ∈ ℝ⁺ ✓

---

## C. Verifica vincoli

| # | Vincolo | Esito | Motivazione |
|---|---------|-------|-------------|
| 1 | F_C produce Δ_ℓ ∈ ℝ⁺ | ✅ | Quadrato × rapporto di positivi = positivo |
| 2 | Δ_ℓ ≤ DH_ℓ soddisfacibile | ✅ | Z_C ≤ DH_ℓ/√DH_D → regione di stabilizzazione esiste |
| 3 | F_C ≠ Z_C | ✅ | Funzione quadratica × fattore, non identità |
| 4 | F_C non genera collocazioni | ✅ | Produce numero scalare, non struttura |
| 5 | F_C ⊆ strumenti confronto Δ | ✅ | Strumento metrico puro |
| 6 | Clausola ETG-P | ✅ | Opera in ℝ⁺, nessuna asserzione ontologica |
| 7 | Bit confinato a ETG-P | ✅ | Rapporti adimensionali, bit non fuoriesce |
| 8 | Coerenza con Eq. 5 | ✅ con nota | Δ_ℓ totale compatibile, decomposizione V/A separata |
| 9 | Computabilità algoritmica | ✅ | `delta_l = z_c**2 * (dh_d / dh_l)` |
| 10 | Zero costanti arbitrarie | ✅ | Nessuna costante, solo grandezze strutturali |

---

## D. Comportamento ai limiti

| Condizione | Z_C | F_C | Δ_ℓ | Stabilizzazione |
|-----------|-----|-----|-----|-----------------|
| H_C = 0 | 0 | 0 | 0 | Sempre (ℓ ∈ L) |
| H_C → DH_D | → ∞ | → ∞ | → ∞ | Mai (blocco, Eq. 16) |
| DH_ℓ alto (rigido) | invariato | smorzato | piccolo | Facile |
| DH_ℓ basso (fragile) | invariato | amplificato | grande | Difficile |

---

## E. Coerenza con Z_C candidata

Pienamente coerente con Z_C(D) = H_C/(DH_D - H_C). Non richiede forma alternativa.

Alternative scartate:
- Z_C = (DH_D - H_C)⁻¹ → Z_C ≠ 0 quando H_C = 0 (viola comportamento atteso)
- Z_C = log(DH_D/(DH_D - H_C)) → corretta ai limiti ma non-linearità logaritmica non necessaria

---

## F. Variabili introdotte

**Nessuna.**

---

## G. Dichiarazione di ignoranza

1. **Relazione DH_D ↔ DH_ℓ**: non so se DH_ℓ ≤ DH_D, se DH_ℓ = DH_D/N, o se sono indipendenti
2. **Decomposizione Δ_ℓ in |V_l - A_l| + |V_c - A_c|**: la formula produce Δ totale, non la ripartizione
3. **Unicità della potenza quadratica**: Z_C^α con α ≠ 2 potrebbe essere ammissibile
4. **Assegnazione pratica dei valori DH_D e DH_ℓ**: non so come vengano calcolati
5. **Versione aggregata**: la formula opera su singola ℓ, non so se serve aggregazione su L
6. **Calcolo pratico di p_i**: non so come si stimano le probabilità
7. **Relazione tra Δ dell'Eq. 5 (ETG-G) e Δ_ℓ della catena ETG-P**: possibile ambiguità G/P
