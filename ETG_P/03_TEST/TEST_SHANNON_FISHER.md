# ETG-P — Test di Non-Frattalicità su Shannon/Fisher

> **CLAUSOLA OBBLIGATORIA**: Questo NON è ETG. È una modellizzazione di ETG. I valori ℝ⁺ sono rappresentazioni strumentali, non ontologia del sistema.

**Stato**: Derivato dalla scissione ETG-G/ETG-P — 17/02/2026
**Fonte**: ClaudeETG/04_LABORATORIO/Test_Non_Frattalicita.md (sezioni 6, 8)

---

## Contesto

Il test di non-frattalicità completo (5 test) è in ETG-G. I primi 3 test e il test 5 riguardano la grammatica pura e restano in ETG-G/04_VINCOLI/VINCOLI_DURI_G.md.

Questo file contiene il **Test 4** — specifico per gli operatori informazionali Shannon/Fisher che usano firme ℝ⁺ e quindi appartengono a ETG-P.

---

## Test 4 — Shannon / Fisher come operatori (test di modellizzazione)

### 4.1 Verifica Shannon

```
H_D : Σ_D → ℝ⁺
```

Condizione frattale: `H(H(Σ_D)) ~ H(Σ_D)`

**Risultato**: ❌ NON ammessa — `H ∉ Σ_D`

H_D prende uno spazio sintattico e restituisce un valore in ℝ⁺. L'output (ℝ⁺) non è dello stesso tipo dell'input (Σ_D). Quindi H non è auto-applicabile.

### 4.2 Verifica Fisher

```
F_D : Δ(Σ_D) → ℝ⁺
```

Condizione frattale: `F(Δ(Δ)) ~ Δ`

**Risultato**: ❌ NON ammessa — `F_D ⇏ Δ`

F_D prende una variazione e restituisce un valore metrico. L'output non genera nuove variazioni. Non c'è ricorsione.

---

## Esito

```
Gli operatori informazionali (H_C, F_C) NON sono chiusi.
```

Questo contribuisce all'esito complessivo: **ETG non è frattale**.

I 5 test completi sono:
1. Δ non genera L (ETG-G)
2. V e A non sono auto-applicabili (ETG-G)
3. ℓ non è isomorfo a L (ETG-G)
4. **Operatori informazionali non sono chiusi** (ETG-P — questo file)
5. ETG non è piano D (ETG-G)

---

## Nota

Anche senza questo test, ETG-G dimostra autonomamente la non-frattalicità (test 1, 2, 3, 5 sono sufficienti). Il test 4 conferma la proprietà anche per le modellizzazioni parametrizzate.

---

## Applicazione di Shannon e Fisher come ℓ in una D

### Shannon (in ETG)
- V: alto per configurabilità sintattica, nullo per contenuto/semantica
- A: alto in D micro / CU, nullo oltre soglia di traduzione
- Shannon resta in L, ma con V e A locali e vincolati

### Fisher (in ETG)
- V: alto come misura di sensibilità / curvatura
- A: alto come operatore metrico, utilizzabile trasversalmente solo come struttura, non come contenuto
- Fisher è compatibile come operatore su Δ, non come informazione
