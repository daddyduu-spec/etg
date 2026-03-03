# [LABORATORIO] ETG — FORMALISMO LOCALE PER d_intra_Neurologia di U

> Fonte: Keep — 5 gen 2026, 21:10:34 (Archiviata)
> Stato: pronto per uso di laboratorio

---

## Stato ETG locale

σᵢ ≔ ⟨D, regime, (Vᵢ, Aᵢ), DHᵢ, Kᵢ, Δᵢ⟩

dove:
- D = Piano D di collocazione
- regime = intra / inter / macro
- (Vᵢ, Aᵢ) = configurazione locale di Vincolo / Attuabilità (non quantitativa)
- DHᵢ = capacità operativa locale
- Kᵢ = insieme finito di pattern attivi
- Δᵢ = scarto informativo locale

---

## Evento ETG riuscito (attraversamento valido)

εᵢ→ᵢ₊₁ ≔ ⟨Q, σᵢ, σᵢ₊₁, Δᵢ→ᵢ₊₁ ≤ DHᵢ, Kᵢ ∩ Kᵢ₊₁ ≠ ∅⟩

Condizioni:
- lo scarto di attraversamento è assorbibile (Δ ≤ DHᵢ)
- esiste continuità di pattern (Kᵢ ∩ Kᵢ₊₁ ≠ ∅)

---

## Evento ETG fallito (non-attraversamento)

εᵢ↛ᵢ₊₁ ≔ ⟨Q, D, regime, Δᵢ→ᵢ₊₁ > DHᵢ, Kᵢ ⟂ Kᵢ₊₁⟩

Condizioni:
- scarto non assorbibile (Δ > DHᵢ)
- assenza di continuità di pattern (Kᵢ ⟂ Kᵢ₊₁)

---

## Ristrutturazione di traiettoria

Q' ≔ f(Q | εᵢ↛ᵢ₊₁, Δ_res)

dove:
- Δ_res = residuo informativo non collocato
- f = funzione di riorganizzazione non garantita, non ottimizzata, non teleologica

---

## Vincoli strutturali

- Nessuna autorità globale
- Nessuna continuità garantita
- Fallimento ammesso
- Tutte le operazioni sono locali
- La validità è ex post e situata

---

Uso ammesso: test di arbitrarietà, compatibilità neurologica, stress sintattico
Nessuna espansione ETG inclusa
