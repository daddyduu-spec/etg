# [LABORATORIO] ETG — STATI LOCALI E EVENTI DI ATTRAVERSAMENTO

> Fonte: Keep — 5 gen 2026, 20:55:34
> Stato: STABILIZZATO — Uso: laboratorio ETG / DB topologico / stress test

---

Versione laboratorio — copiabile

---

## A) Stato ETG locale (cella del rettangolo)

### Definizione minimale

σᵢ ≔ ⟨D, regime, (Vᵢ, Aᵢ), DHᵢ, Kᵢ, Δᵢ⟩

### Vincoli

- D è etichetta di collocazione (non contenitore)
- regime ∈ {intra, inter, macro}
- Vᵢ, Aᵢ sono posizioni topologiche (non quantità)
- DHᵢ è capacità operativa locale
- Kᵢ è insieme delle interazioni ammesse nel piano
- Δᵢ è scarto locale non ancora risolto

---

## B) Evento ETG di attraversamento riuscito (celle adiacenti)

### Formalizzazione

εᵢ→ᵢ₊₁ ≔ ⟨Q, σᵢ, σᵢ₊₁, Δᵢ→ᵢ₊₁ ≤ DHᵢ, Kᵢ ∩ Kᵢ₊₁ ≠ ∅⟩

### Effetti

- Q avanza
- σᵢ₊₁ diventa stato attivo
- Δ viene assorbito o trasformato
- nessuna generazione ontologica

---

## C) Evento ETG di fallimento di attraversamento

### Formalizzazione

εᵢ↛ᵢ₊₁ ≔ ⟨Q, D, regime, Δᵢ→ᵢ₊₁ > DHᵢ, Kᵢ ⟂ Kᵢ₊₁⟩

### Effetti

- Q non avanza
- σᵢ resta attivo
- Δ locale persiste
- nessuna semantica nuova prodotta

---

## D) Nascita di una traiettoria secondaria

### Formalizzazione

Q' ≔ f(Q | εᵢ↛ᵢ₊₁, Δ_res)

### Vincoli

- Q' non è nuova entità
- Q' resta nella stessa topologia
- Q' è deviazione / riflessione operativa

---

## E) Vincoli globali (laboratorio)

- Nessun operatore genera contenuti
- Nessun evento attraversa MA
- Nessuna Q implica nuovo Piano D
- Ogni nascita storica di Piano D è solo ex post
- La non-linearità emerge da: riflessione, deviazione, soglia DH — non da calcolo numerico

---

Nota: testo conforme a modalità notarile, senza espansione ontologica.
