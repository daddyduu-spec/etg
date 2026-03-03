# BOOTLOAD — Scissione ETG-G / ETG-P

> Istruzioni per la sessione di scissione. Leggi TUTTO prima di agire.

---

## OBIETTIVO

Creare due nuove cartelle:
- `ETG_G/` — Grammatica Pura (non-metrica, topologica, ~22 simboli core)
- `ETG_P/` — Parametrizzazioni Operative (metriche, ℝ⁺, modellizzazioni)

La cartella `ClaudeETG/` resta INTATTA. Non modificarla.

---

## DECISIONE ARCHITETTONICO-NOTARILE (approvata)

### ETG-G contiene:
1. Il nucleo grammaticale non-metrico
2. ℓ := ⟨D, V(D), A(D), DH_ℓ, Δ_ℓ⟩
3. Il rettangolo D con i 4 vertici (V_l, A_l, V_c, A_c)
4. Tutti i vincoli duri
5. Le tre frasi canoniche RISCRITTE senza H_C, F_C, Z_C
6. La Prima Frase diventa: "∃ℓ tale che Σ_CU → Δ_ℓ ∧ Δ_ℓ ≤ DH_ℓ ⇒ ℓ ∈ L ⊂ C"
7. CLAUSOLA OBBLIGATORIA: "Il passaggio Σ_CU → Δ_ℓ è postulato strutturale; il meccanismo è demandato a modellizzazioni ETG-P."
8. Nessun ℝ⁺. Nessuna firma matematica. Solo topologia e vincoli qualitativi.

### ETG-P contiene:
1. H_C — operatore di dispersione sintattica (Shannon)
2. F_C — operatore metrico di variazione (Fisher)
3. Z_C — impedenza sintattica
4. Tutte le firme ℝ⁺
5. La Prima Frase nella versione estesa: Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ
6. CLAUSOLA OBBLIGATORIA: "Questo NON è ETG. È una modellizzazione di ETG. I valori ℝ⁺ sono rappresentazioni strumentali, non ontologia del sistema."
7. Qualsiasi futura parametrizzazione per DB computabili

---

## FILE SORGENTE (in ClaudeETG/, da NON modificare)

Leggili tutti per capire il contenuto e poi smistarlo nelle due cartelle.

### File che contengono materiale da smistare:

1. **`ClaudeETG/02_VOCABOLARIO/VOCABOLARIO_ETG_COMPLETO.md`** (v1.4)
   - TUTTO va in ETG_G TRANNE le sezioni H_C (righe ~356-362), F_C (~366-372), Z_C (~376-378) che vanno in ETG_P
   - ATTENZIONE: La Prima Frase nella sezione O (righe ~538-541) va riscritta in ETG_G senza H_C/F_C/Z_C

2. **`ClaudeETG/PROMPT_RESTART.md`**
   - Glossario: le voci H_C, F_C, Z_C, Σ_CU vanno in ETG_P
   - La Prima Frase (riga ~156) va riscritta in ETG_G
   - Σ_CU resta anche in ETG_G (è il punto di partenza) ma senza firma ℝ⁺

3. **`ClaudeETG/04_LABORATORIO/Tre_Frasi_ETG_Canoniche.md`**
   - La Prima Frase va riscritta in ETG_G (senza catena H_C→Z_C→F_C)
   - La versione estesa con H_C→Z_C→F_C va in ETG_P
   - Le altre due frasi restano in ETG_G (non usano H_C/F_C/Z_C)

4. **`ClaudeETG/04_LABORATORIO/V_A_Operatori_Formali.md`**
   - V : D → ℘(Σ_D) e A : D → ℘(𝒯_D) restano in ETG_G
   - Le sezioni Shannon/Fisher (H_D : Σ_D → ℝ⁺, F_D : Δ(Σ_D) → ℝ⁺) vanno in ETG_P

5. **`ClaudeETG/02_VOCABOLARIO/VOCABOLARIO_OPERATORI_NOTAIO.md`**
   - Le definizioni di H_D e F_D vanno in ETG_P
   - Il resto resta in ETG_G

6. **`ClaudeETG/04_LABORATORIO/Test_Non_Frattalicita.md`**
   - I test core (V, A, DH, L, Δ) restano in ETG_G
   - I test su H_D e F_D vanno in ETG_P (marcati come "test di modellizzazione")

7. **`ClaudeETG/04_LABORATORIO/Dichiarazione_Canonica_L_elle.md`**
   - Riferimenti a Σ_CU e Z_C: aggiornare la nota, spostare dettagli metrici in ETG_P

8. **`ClaudeETG/03_PROTOCOLLI/LEGGENDA_FONETICA.md`**
   - Le pronunce di H_C, F_C, Z_C vanno in ETG_P

### File che vanno INTERI in ETG_G (copia diretta):

9. **`ClaudeETG/00_MASTER/ETG_MASTER_V5.9.4_CANONICAL.md`** — il master
10. Tutti gli altri file di ClaudeETG che non contengono H_C/F_C/Z_C

---

## CONVENZIONI CRITICHE (non sbagliare)

- S a SINISTRA (sempre)
- Cer (non Cre) = canale inter
- ℓ VIETATO in intra. In intra: solo μ, μ'
- CU non ha formula — è solo un punto su C dove più U coesistono
- ETG mostra, non confronta
- Il tempo non esiste in ETG
- V_l — A_l = L (lato alto del rettangolo)
- V_l — V_c = S (lato sinistro = portata)
- A_l — A_c = Ma (soglia di causalità)
- Δ agisce su ℓ, non su L. L cambia per emergenza.
- ⦿ registrata su C (inter), non risiede in intra
- DH = linguaggio del piano, non solo fasce di resistenza
- Meta = struttura logica, non deposito di informazione
- V, A, DH, Δ si applicano a ℓ, MAI a L

## STRUTTURA CARTELLE DA CREARE

```
ETG_G/
├── 00_MASTER/
│   └── ETG_MASTER_G.md          (master riscritto, solo grammatica pura)
├── 01_VOCABOLARIO/
│   └── VOCABOLARIO_ETG_G.md     (v1.5-G, senza H_C/F_C/Z_C)
├── 02_FRASI/
│   └── TRE_FRASI_ETG_G.md       (Prima Frase riscritta)
├── 03_OPERATORI/
│   └── V_A_OPERATORI_G.md       (solo V e A, senza Shannon/Fisher)
├── 04_VINCOLI/
│   └── VINCOLI_DURI_G.md        (tutti i vincoli in un file)
└── NOTE.md                       (clausole: autosufficienza, postulato Σ_CU→Δ)

ETG_P/
├── 01_OPERATORI/
│   └── OPERATORI_INFORMAZIONALI.md  (H_C, F_C, Z_C con firme ℝ⁺)
├── 02_FRASI/
│   └── PRIMA_FRASE_ESTESA.md    (versione con catena H_C→Z_C→F_C)
├── 03_TEST/
│   └── TEST_SHANNON_FISHER.md   (test non-frattalità su H_D/F_D)
└── NOTE.md                       (clausola: "questo NON è ETG, è modellizzazione")
```

## QUATTRO CLAUSOLE OBBLIGATORIE (verdetto notarile)

Devono essere scritte esplicitamente in entrambe le cartelle:

1. **ETG-G è autosufficiente.** Nessuna proprietà di ETG-G dipende da ETG-P.
2. **ETG-P è modellizzazione opzionale.** Non è ETG. È strumento applicativo.
3. **Nessuna proprietà di ETG-G dipende da ℝ⁺.**
4. **Il passaggio Σ_CU → Δ_ℓ è postulato strutturale.** Il meccanismo è demandato a ETG-P.

## DA LEGGERE PER CONTESTO COMPLETO

Se l'agente ha bisogno di più contesto su ETG:
- `ClaudeETG/PROMPT_RESTART.md` — glossario completo
- `ClaudeETG/LEGGIMI.md` — storia delle 5 sessioni
- `ClaudeETG/07_BRAINSTORMING/RIFLESSIONI_STRUTTURALI.md` — percorso del ragionamento
- `ClaudeETG/02_VOCABOLARIO/VOCABOLARIO_ETG_COMPLETO.md` — vocabolario v1.4
