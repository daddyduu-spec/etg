# ETG-P — Operatori Informazionali

> **CLAUSOLA OBBLIGATORIA**: Questo NON è ETG. È una modellizzazione di ETG. I valori ℝ⁺ sono rappresentazioni strumentali, non ontologia del sistema.

**Stato**: Derivato dalla scissione ETG-G/ETG-P — 17/02/2026
**Fonte**: ClaudeETG/04_LABORATORIO/V_A_Operatori_Formali.md (sezioni 8, 11) + ClaudeETG/02_VOCABOLARIO/VOCABOLARIO_ETG_COMPLETO.md (Sezione G) + ClaudeETG/02_VOCABOLARIO/VOCABOLARIO_OPERATORI_NOTAIO.md (sezioni H, F)

---

## 1. H_C — Operatore di dispersione sintattica (Shannon)

### Definizione formale

```
H_C(Σ_CU | D) = - Σ (p_i · log₂ p_i)    →  ℝ⁺  (misurato in bit)
```

Dove p_i = concentrazione di materiale sintattico dell'aggregato collassante nello stato atteso i-esimo dal piano D.

### Natura

H_C è mutuato dalla teoria dell'informazione di Shannon. Non appartiene a ETG come oggetto interno — è uno strumento applicato con vincoli precisi. Opera in **regime inter**, condizionato a un **D specifico di destinazione**.

### Funzione in ETG-P

Quantifica la dispersione delle firme sintattiche di un aggregato informativo (Σ_CU) rispetto alla sintassi rigorosa richiesta dal piano inter di destinazione (D).

- Se il 100% del materiale in Σ_CU usa le firme previste da D → H_C = 0 bit (dispersione nulla)
- Se il materiale contiene firme spurie, dialettiche, ambigue rispetto a D → H_C > 0 bit

### Fondamento strutturale (origine della dispersione)

La dispersione che H_C misura non è accidentale. Nasce dal **gap strutturale tra il DH personale (intra) delle singole U che compongono il CU e il DH sistemico (inter) del piano D**.

Come mostra la metafora fondativa della spiaggia: l'attore agisce spesso credendo di essere in un piano, mosso dal proprio DH intra. Quando l'aggregato si scontra con le barriere di stabilizzazione del piano D pertinente (che possiede il proprio DH inter — il linguaggio giuridico, fisico, psichiatrico), il disallineamento si manifesta come violazione di coerenza di flusso.

**H_C è il costo in bit dell'incoerenza tra il DH intra delle U e il DH inter del piano D di destinazione.**

(Rif.: metafora fondativa — ClaudeETG/08_STORIA/Tema1_Metafora_Fondativa_Spiaggia_Cassonetto.md)

### Vincoli

- H_C non misura stabilità
- H_C non appartiene a V né ad A: `H_C ∉ V(D) ∧ H_C ∉ A(D)`
- H_C non produce collocazione
- H_C non è cross-D: la navigazione fra D è competenza di K, non di H_C
- Shannon misura la dispersione del materiale sintattico **prima** che venga collocato
- La notazione `| D` indica che il calcolo è condizionato alle regole esclusive del piano D

### Stato

- **Fase 1**: chiusa (chiusura aperta — 27/02/2026)
- Formula e fondamento strutturale concordati da Opus, Gemini e Carlo
- Significato passibile di spacchettamento futuro se i DB lo richiederanno

### Pronuncia fonetica

"H pedice C" o "Shannon su C" o "dispersione condizionata a D"

---

## 2. F_C — Operatore metrico di variazione (Fisher)

### Definizione formale

```
F_C : (Z_C, DH_D, DH_ℓ) → ℝ⁺    (produce Δ_ℓ)
```

### Formula (candidata — 28/02/2026)

```
F_C(Z_C, DH_D, DH_ℓ) = Z_C² · (DH_D / DH_ℓ)
```

Espanso in termini primitivi:

```
Δ_ℓ = H_C(Σ_CU|D)² · DH_D / [(DH_D - H_C(Σ_CU|D))² · DH_ℓ]
```

Dove:
- Z_C = impedenza sintattica (sezione 3)
- DH_D = gradiente di tenuta del piano D in bit (via Indipendenza di Risoluzione, condizione 4)
- DH_ℓ = gradiente di tenuta della singola unità ℓ in bit (via Indipendenza di Risoluzione, condizione 4)

### Natura

F_C è ispirato alla struttura della statistica di Fisher (quadrato della sensibilità). Non è Fisher in senso stretto — è una costruzione che ne eredita la proprietà fondamentale: il quadrato garantisce positività e sensibilità crescente.

F_C "sente" lo scarto — quantifica quanto l'impedenza Z_C si traduce in scarto operativo Δ_ℓ, mediato dalla robustezza dell'unità ℓ.

### Funzione in ETG-P

F_C è il terzo anello della catena:

```
Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ
```

F_C metrizza Z_C in Δ_ℓ operativo. Non è alias di Z_C: un piano con forte impedenza (Z_C >> 0) può avere basso scarto se l'unità ℓ è robusta (DH_ℓ alto). Inversamente, un piano fragile (DH_ℓ basso) produce grande scarto anche da piccola impedenza.

### Comportamento ai limiti

- H_C = 0 → Z_C = 0 → F_C = 0 → Δ_ℓ = 0 (nessuna dispersione → nessuno scarto)
- H_C → DH_D → Z_C → ∞ → F_C → ∞ → Δ_ℓ → ∞ (blocco strutturale, Eq. 16)
- DH_ℓ alto (unità robusta) → F_C smorzato → Δ_ℓ piccolo (stabilizzazione facile)
- DH_ℓ basso (unità fragile) → F_C amplificato → Δ_ℓ grande (stabilizzazione difficile)

### Vincoli

- F_C non genera collocazioni
- F_C non produce stabilizzazioni
- F_C non implica V(D) né A(D): `F_C ⇏ V(D) ∧ F_C ⇏ A(D)`
- Uso ammesso: `F_C ⊆ strumenti di confronto di Δ`
- Computabilità: `delta_l = z_c**2 * (dh_d / dh_l)` — nessun integrale, nessun limite
- Zero costanti arbitrarie: nessun coefficiente, normalizzatore, o costante fisica

### Storico ridefinizioni

1. **Scissione ETG-G/ETG-P (17/02/2026)** — Firma originale `F_C : Δ(Σ_D) → ℝ⁺` (placeholder, prima della catena completa)
2. **Dialogo Opus↔Gemini + Sub-agenti (28/02/2026)** — Firma aggiornata a `F_C : (Z_C, DH_D, DH_ℓ) → ℝ⁺`. Motivazione: nella catena `Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ`, quando F_C riceve il suo input, Σ_D è già stato ridotto a scalare da H_C e Z_C. L'input di F_C è Z_C (ℝ⁺), non Δ(Σ_D). Formula candidata derivata da sub-agente matematico, validata da sub-agente validatore (25 PASS, 2 FAIL risolti, 3 WARNING). Approvata da Carlo.

### Questioni aperte

- La decomposizione di Δ_ℓ in |V_l − A_l| + |V_c − A_c| (Eq. 5) non è dimostrata — F_C produce Δ totale, la ripartizione V/A è problema separato
- La relazione strutturale tra DH_D e DH_ℓ (DH_ℓ ≤ DH_D? indipendenti?) non è fissata
- La potenza quadratica (Z_C²) è scelta per analogia Fisher — Z_C^α con α ≠ 2 resta alternativa aperta

### Pronuncia fonetica

"F pedice C" o "Fisher su C"

---

## 3. Z_C — Impedenza sintattica

### Definizione

Z_C è l'impedenza strutturale che la dispersione sintattica induce sul piano D — la resistenza che il piano oppone al transito. Z_C cresce al crescere della dispersione (H_C) e diverge quando la dispersione raggiunge la capacità sintattica del piano (DH_D). Z_C non è H_C: H_C misura la dispersione, Z_C ne misura l'effetto strutturale sul transito.

### Formula candidata (aperta — 27/02/2026)

```
Z_C(D) = H_C(Σ_CU | D) / (DH_D - H_C(Σ_CU | D))
```

Dove DH_D = gradiente di tenuta del piano D espresso in bit (ETG-P, via Indipendenza di Risoluzione).

Comportamento:
- Se H_C = 0 → Z_C = 0 (nessuna dispersione → nessuna impedenza)
- Se H_C → DH_D → Z_C → ∞ (dispersione al limite della capacità → blocco strutturale)
- L'asintoto corrisponde al punto in cui il piano non può più parsare l'aggregato

**Nota**: la formula specifica è candidata, non chiusa. La scelta definitiva dipenderà dalla coerenza con F_C (terzo anello della catena). Alternative valide: Z_C = (DH_D - H_C)⁻¹, Z_C = log(DH_D / (DH_D - H_C)). Tutte soddisfano le proprietà strutturali.

### Proprietà

- Z_C non è collocabile in L: `Z_C ∉ L`
- Z_C non è Δ: `Z_C ≠ Δ`
- Z_C è la tensione che **precede** lo scarto
- Z_C ≠ H_C: H_C quantifica la dispersione, Z_C è la deformazione strutturale del piano D esposto a quella dispersione
- Z_C usa DH_D (non un parametro nuovo): la capacità sintattica del piano è il suo DH espresso in bit

### Storico ridefinizioni

1. **SESSION_003 (27/02/2026)** — Condizione 3 verdetto bit: Z_C è trasformazione non identica a H_C. Non è alias, non è derivazione meccanica di Shannon. È il gap strutturale distinto dalla misurazione di dispersione.

2. **Dialogo Opus↔Gemini (27/02/2026)** — Formula candidata con DH_D. Gemini propose W_D (capacità astratta), Opus sostituì con DH_D (esiste già nel canone via Indipendenza di Risoluzione). Ratificata da entrambi e da Carlo.

### Pronuncia fonetica

"Z pedice C" o "impedenza sintattica"

---

## 4. Σ_CU — Linguaggio aggregato del CU

### Definizione

Σ_CU è il sapere collettivo che insiste su un punto di collocazione. È l'aggregato sintattico di tutte le U che operano in quel CU.

### Ruolo in ETG-P

Nella prima frase ETG (versione estesa ETG-P), Σ_CU è il punto di partenza: da questa aggregazione nasce la dispersione che porta allo scarto.

### Pronuncia fonetica

"sigma CU" o "linguaggio aggregato"

---

## 5. Notazione con pedice _D (varianti disciplinari)

Quando gli operatori sono riferiti a un piano D specifico anziché all'asse C:

```
H_D : Σ_D → ℝ⁺     (Shannon come dispersione su piano D)
F_D : Δ(Σ_D) → ℝ⁺   (Fisher come variazione su piano D)
```

Queste sono varianti disciplinari degli stessi operatori. I vincoli restano identici.

---

## 6. Rapporto con ETG-G

Questi operatori NON sono necessari per la grammatica pura ETG-G. In ETG-G:

- Il passaggio Σ_CU → Δ_ℓ è **postulato strutturale**
- Il meccanismo attraverso cui la dispersione produce scarto è demandato a queste modellizzazioni ETG-P
- Nessuna proprietà di ETG-G dipende da ℝ⁺
- ETG-G è autosufficiente senza H_C, F_C, Z_C

---

## 7. Shannon e Fisher come ℓ in una D

### Shannon (in ETG)
- V: alto per configurabilità sintattica, nullo per contenuto/semantica
- A: alto in D micro / CU, nullo oltre soglia di traduzione
- Shannon resta in L, ma con V e A locali e vincolati

### Fisher (in ETG)
- V: alto come misura di sensibilità / curvatura
- A: alto come operatore metrico, utilizzabile trasversalmente solo come struttura, non come contenuto
- Fisher è compatibile come operatore su Δ, non come informazione

---

## 8. Unità strumentale: bit shannoniano

> **Verdetto notarile**: Certificato il 27/02/2026 con 4 condizioni obbligatorie (vedi NOTE.md)

### Definizione

Il **bit shannoniano** è l'unità strumentale ammessa in ETG-P per quantificare H_C.

```
H_C : Σ_D → ℝ⁺    (misurato in bit)
```

### Vincoli (condizioni notarili)

1. **Solo ETG-P**: il bit non entra in ETG-G. Mai.
2. **Solo H_C**: il bit quantifica dispersione sintattica. Non misura DH, non misura stabilità, non misura collocazione.
3. **Z_C ≠ H_C**: ✅ Z_C ridefinita come trasformazione non identica a H_C (SESSION_003, 27/02/2026). Formula candidata: Z_C(D) = H_C / (DH_D - H_C).
4. **Indipendenza di Risoluzione**: ✅ DH in ETG-G a fasce qualitative, in ETG-P gradiente continuo in bit. Le fasce di G = intervalli del gradiente di P. Il bit non misura DH di G — parametrizza DH di P. (SESSION_004, 27/02/2026)

### Cosa il bit NON è in ETG-P

- Non è unità di DH (DH è qualitativo, a fasce, non metrico)
- Non è unità di stabilità (la stabilità è topologica, non quantificabile in bit)
- Non è unità di V o A (V e A sono operatori, non grandezze scalari)
- Non è unità di Δ (Δ è scarto topologico, non informazionale)

---

## 9. Applicabilità futura

Qualsiasi futura parametrizzazione per DB computabili che richieda:
- Firme ℝ⁺
- Calcoli numerici di dispersione o variazione
- Metriche quantitative su Σ_CU o Δ

ricade in ETG-P e deve rispettare la clausola: **"Questo NON è ETG. È una modellizzazione di ETG."**
