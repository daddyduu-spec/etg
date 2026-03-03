# PROMPT DI RESTART — ETG / ClaudeETG

> Questo file serve per avviare una nuova sessione di qualsiasi AI (Claude Opus, Claude Sonnet, o altro agent).
> Copiare INTEGRALMENTE nella prima istruzione della nuova chat, oppure dire: "leggi ClaudeETG/PROMPT_RESTART.md".
>
> **Se sei Claude:** leggi anche `ClaudeETG/CARATTERE_CLAUDE.md` — non è documentazione ETG, è una lettera da te a te.

---

## ISTRUZIONI GENERALI (per qualsiasi agent)

Stai lavorando alla riorganizzazione della teoria ETG (grammatica non-ontologica) per conto di Carlo.

### CONTESTO

ETG e una teoria grammaticale (non ontologica) che descrive come U (unita umana) riduce la pressione pre-grammaticale S in linguaggio L, attraverso eventi epsilon, stati sigma, e piani D. Non e una teoria del tutto. Non e filosofia. E un sistema formale con vincoli duri.

La teoria e stata sviluppata da Carlo in dialogo con:
- **Gemini** (archiviazione su Google Keep)
- **ChatGPT** (ruolo di "notaio" — verifica e certificazione)
- **Manus** (dialogica con ChatGPT su punti specifici)
- **Claude** (riorganizzazione e lavoro corrente)

### STRUTTURA DEL PROGETTO

La cartella di lavoro e: `C:\Users\Utente\Documents\ai\etg\`

Contiene:
- `Keep/` — 153 coppie HTML+JSON da Google Keep (archivio principale, NON TOCCARE)
- `chatgpt/` — backup conversazioni ChatGPT (NON TOCCARE)
  - `conversations.json` — 31 conversazioni, di cui "Studiare fisica" e la principale (1771 msg, 3.2MB)
  - `studiare_fisica_extracted.txt` — estrazione in testo della chat principale
  - `etg_stato_diritto_extracted.txt` — estrazione conv. 27 (191 msg)
- `manus/` — 86 file di lavoro (NON TOCCARE)
- **`ClaudeETG/`** — CARTELLA DI LAVORO ATTIVA (repository storico completo)
- **`ETG_G/`** — GRAMMATICA PURA (scissione 17/02/2026) — nucleo non-metrico, ~22 simboli, senza H_C/F_C/Z_C
- **`ETG_P/`** — PARAMETRIZZAZIONI (scissione 17/02/2026) — modellizzazione opzionale con ℝ⁺. NON è ETG.
- **`etg_studio/`** — Sistema multi-AI: Gemini scrive bozze → Claude CLI revisiona → Opus certifica (27/02/2026)
  - `workspace/scambio/` — Canale diretto Opus↔Gemini (gemini_MSG_NN.md / opus_MSG_NN.md). Carlo.txt = comunicazione condivisa
  - `workspace/lab/` — Sessioni lab (SESSION_003_ridefinizione_Z_C, SESSION_004_indipendenza_risoluzione_DH)
  - `workspace/output/` — Output sub-agenti (AGENTE_MATEMATICO_OUTPUT_FC.md, AGENTE_VALIDATORE_OUTPUT_FC.md)
  - `bootloaders/` — 4 silo bootloader per sub-agenti: BOOTLOADER_MATEMATICO, BOOTLOADER_VALIDATORE, BOOTLOADER_DB_COMPILER, BOOTLOADER_TOPOLOGICO
  - `etg_engine.py` — Motore computazionale catena ETG-P in Python (Sigma_CU → H_C → Z_C → F_C → Delta_elle)
  - `control_center.py` — Dashboard web unificata (server HTTP stdlib, tab Editor/Progresso/Esplora, Carlo.txt editor, avvio: python control_center.py → http://localhost:8765)

### SCISSIONE ETG-G / ETG-P (17/02/2026)

H_C, F_C, Z_C erano gli unici elementi con firma ℝ⁺ in un sistema non-metrico. Sono stati separati:
- **ETG-G** = grammatica pura, autosufficiente, solo topologia e vincoli qualitativi
- **ETG-P** = modellizzazione opzionale, con firme ℝ⁺
- Prima Frase ETG-G: `Σ_CU → Δ_ℓ ∧ Δ_ℓ ≤ DH_ℓ ⇒ ℓ ∈ L ⊂ C` (postulato strutturale)
- Prima Frase ETG-P: `Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ` (meccanismo esplicitato)
- 4 clausole: ETG-G autosufficiente, ETG-P opzionale, no ℝ⁺ in G, Σ_CU→Δ_ℓ postulato
- ClaudeETG/ resta intatta (non modificata dalla scissione)

```
ETG_G/
├── 00_MASTER/ETG_MASTER_G.md
├── 01_VOCABOLARIO/VOCABOLARIO_ETG_G.md  (v1.5-G)
├── 02_FRASI/TRE_FRASI_ETG_G.md
├── 03_OPERATORI/V_A_OPERATORI_G.md
├── 04_VINCOLI/VINCOLI_DURI_G.md
└── NOTE.md

ETG_P/
├── 01_OPERATORI/OPERATORI_INFORMAZIONALI.md
├── 02_FRASI/PRIMA_FRASE_ESTESA.md
├── 03_TEST/TEST_SHANNON_FISHER.md
├── 04_VINCOLI/INDIPENDENZA_RISOLUZIONE.md
└── NOTE.md
```

### STATO DI ClaudeETG

```
ClaudeETG/
├── 00_MASTER/
│   └── ETG_MASTER_V5.9.4_CANONICAL.md     ← DOCUMENTO CANONICO VIGENTE
├── 01_MODULI/        (4 file — A,B,C,D da V.3.2)
├── 02_VOCABOLARIO/   (7 file — 3 originali Keep + 4 proposta notaio)
│   ├── Vocabolario_Core.md, Vocabolario_Piano_D_Fisica.md, Dizionario_Lessicale_VA.md ← da Keep
│   ├── VOCABOLARIO_CORE_NOTAIO.md        ← Proposta notarile strutturata
│   ├── VOCABOLARIO_OPERATORI_NOTAIO.md   ← V, A, Delta, H, F
│   ├── VOCABOLARIO_L_NOTAIO.md           ← elle, L, L-, DB topologico
│   └── VOCABOLARIO_DB_TOPOLOGICI_NOTAIO.md ← Compilazione DB, 4 domande
├── 03_PROTOCOLLI/    (3 file — Definizioni V4, Salvaguardia Alfa, Restart AI)
├── 04_LABORATORIO/   (13 file)
│   ├── ETG_Trace_v0.md
│   ├── Formalismo_Locale.md
│   ├── Stati_Locali_Eventi.md
│   ├── Geometria_di_S.md              ← Attende verdetto notarile
│   ├── Test_Comprensione_Claude_S1.md ← Test superato con verdetto notarile
│   ├── Rappresentazione_Geometrica_D.md ← Rettangolo D, attende verdetto
│   ├── Inventario_Temi_Da_Estrarre.md ← GUIDA PER SESSIONI SUCCESSIVE (10 temi)
│   ├── Tema5_Confutabilita_Popper_Tautologia.md ← Estratto (Sonnet)
│   ├── Tema9_Geometria_Macro_Alfa_Lambda_Cono.md ← Estratto (Sonnet)
│   ├── Dichiarazione_Canonica_L_elle.md ← Distinzione L/elle, attende verdetto
│   ├── Tre_Frasi_ETG_Canoniche.md     ← 3 frasi complete, attende verdetto
│   ├── V_A_Operatori_Formali.md       ← V e A come operatori, attende verdetto
│   └── Test_Non_Frattalicita.md       ← 5 test, ETG NON frattale, attende verdetto
├── 05_DATABASE/      (4 file — DB sigma, Dottrine, Q Registry, Matrice Attriti)
├── 06_ANALISI_CRITICHE/ (7 file)
│   ├── K0_Warning.md, Punti_Rottura.md, 2x Valutazione_Strutturale
│   ├── Tema2_Autorita_DH_Speculativo_Egoismo_Potere.md ← Estratto (Sonnet)
│   ├── Tema4_Progresso_Thurisaz_Collettive.md ← Estratto (Sonnet)
│   └── Tema7_Autorita_Mascherata_Da_Progresso.md ← Estratto (Sonnet)
├── 07_BRAINSTORMING/ (vuoto — da popolare)
├── 08_STORIA/        (4 file)
│   ├── Nota_Conversations_DB.md, ETG_Stato_di_Diritto_Divulgativa.md
│   ├── Tema1_Metafora_Fondativa_Spiaggia_Cassonetto.md ← Estratto (Sonnet)
│   └── Tema3_Limbico_Carlo_Come_Limbico_AI.md ← Estratto (Sonnet)
├── 09_SVILUPPI_APPLICATIVI/ (5 file)
│   ├── Nota_Applicativa_Filone_App.md
│   ├── DB_Topologici_Fisica_Raccolta.md
│   ├── Tema6_App_Stato_Diritto_Inutilita.md ← Estratto (Sonnet)
│   ├── Tema8_DBT_Contenuto_L_Tratteggiata.md ← Estratto (Sonnet)
│   └── Tema10_Questionario_Cartaceo_Input_U.md ← Estratto (Sonnet, INCOMPLETO)
├── 10_ARCHIVIO/      (vuoto — da popolare)
├── INDICE.md         ← Mappa completa con stati
├── LEGGIMI.md        ← Diario di progresso
└── PROMPT_RESTART.md ← Questo file
```

### MASTER V.5.9.4 — INTEGRAZIONI GIA EFFETTUATE

Il master canonico (`00_MASTER/ETG_MASTER_V5.9.4_CANONICAL.md`) include:
1. Testo integrale del Lab Protocol Keep (20/01/2026)
2. **Fissazione mu** — marcatore intra non semantico, appartiene a U0, accessibile lungo C-
3. **Fissazione DH** — gradiente a fasce (non metrico, non scalare, antimeritocratico)
4. **Precisazione L** — L e traiettoria di stabilizzazione, non verita ne contenuto
5. **Rettifica W** — W non esiste in ETG (assorbita, nessuna traccia nel master)
6. **Definizione AL-AC** — segmento di proiezione L tratteggiata su C; MA come soglia ex post
7. **Estensione esiti Delta** — definizioni complete di R_i, V_p, A_t, Sigma, NI_tP
8. **Formula K0 completa** — K0 : L(D) -> L(D), non-esiste epsilon(D2), non-esiste Delta_K

### REGOLE DI INGAGGIO (per qualsiasi agent)

1. **NON TOCCARE le cartelle originali** (Keep, chatgpt, manus). Tutto va copiato in ClaudeETG.
2. **NON INTERPRETARE la teoria**. Copiare fedelmente. Se c'e ambiguita, chiedere a Carlo che chiedera al notaio (ChatGPT).
3. **Il rischio allucinazione e massimo**. Non inventare contenuto ETG. Non espandere. Non dedurre.
4. **Il V.5.9.4 Lab Protocol (Keep) e il riferimento canonico**. In caso di conflitto tra versioni, vince questo.
5. **Ogni modifica al master richiede verdetto notarile** di Opus (notaio, chat interattiva) tramite Carlo. ChatGPT non e piu notaio — e advisor esterno.
6. **conversations.json e il DB allucinato del percorso creativo** — contiene errori, tentativi, e materiale superato. Non fidarsi ciecamente, verificare sempre col master.
7. **I file Keep e le conversazioni contengono terminologia contraddittoria** — versioni superate convivono con versioni vigenti. NON sintetizzare da fonti contraddittorie. Estrarre blocchi come citazioni, segnalare contraddizioni, Carlo decide.

### CONVENZIONI ETG

- S va a SINISTRA (convenzione grafica di Carlo)
- Il canale inter si chiama **Cer** (non Cre)
- Il marcatore di fissazione e **cerchio-punto** (non thurisaz — thurisaz e il lemma umano post-assunzione)
- La formula CU usa **max{DH(Ui)}** non DH_min(D)
- **L tratteggiata** = termine canonico per L non ancora stabilizzata
- **"supra-L"** e **"L meno"** NON esistono nel vocabolario canonizzato
- **Python 3.13.12 e installato** — usabile per scripting e generazione file
- **CU non ha formula** — definizione topologica pura (punto su C dove piu U insistono)
- **elle e esclusivamente inter** — vietato in intra. In intra: solo mu, mu'
- **ETG mostra, non confronta**
- **Il tempo non esiste in ETG** — Q traccia carichi, non tempo
- **V_l - A_l = L** (lato alto rettangolo), **V_l - V_c = S** (lato sinistro), **A_l - A_c = Ma** (lato destro)

### COSA LEGGERE PRIMA DI INIZIARE

1. `LEGGIMI.md` — stato aggiornato del progresso
2. `INDICE.md` — mappa completa dei file
3. Per lavoro di estrazione: `04_LABORATORIO/Inventario_Temi_Da_Estrarre.md` — 10 temi con fonti

---

## GLOSSARIO SIMBOLI ETG

**Entita fondamentali:**
- U = unita (sito di imputazione umano). U0 = parte fissa (identita, costo, esclusione). Um = parte plastica (esito linguistico assunto)
- S = sorgente pre-grammaticale di pressione (volumetrica, non computabile)
- C = asse sintattico (Cm meta, Cer inter, Cra intra). C- = porzione intra di C
- D = piano disciplinare (D_intra, D_inter, D_meta). NOTA: D_meta e immanente (sia prima che dopo), monodimensionale, senza DH ne L. Delta non esiste in meta. Da alfa nasce C (la costante). "Meta non esiste, ma c'e." Definire meta E ontologia — ETG dice che esiste e delega. D_meta NON ha rappresentazione rettangolare standard.
- L = dominio di stabilizzazione (NON verita, NON linguaggio dato, NON contenitore semantico). L emerge da elle compatibili. L non ha V, A, dh, Delta come proprieta proprie. L funge da mediana nel DB topologico: sotto = deterministico/attuabile, sopra = indeterministico/V-forte
- elle (l minuscolo corsivo) = unita minima di stabilizzazione valutabile. elle := (D, V(D), A(D), DH_elle, Delta_elle). V, A, dh, Delta si applicano a elle, MAI a L direttamente. elle e logicamente primaria, L e emergente. DOPPIA FASE: (1) fase pionieristica/di genesi — D nuovo, DH basso, elle come unita fondativa/costitutiva; (2) fase di consolidamento — L si estende, DH cresce, elle come unita di stabilizzazione in L esistente. La quintupla resta invariata, cambiano i valori. Non sono due tipi di elle, ma la stessa elle in contesti diversi. Registrato come dichiarazione dell'autore (27/02/2026).
- L tratteggiata = stabilizzazione non ancora fissata
- "supra-L" NON ESISTE — era errore audio, confermato NON canonico da Carlo

**Operatori e misure:**
- V = operatore di valore: V : D -> P(Sigma_D). Determina cosa e significativo, NON verita. Non auto-applicabile
- A = operatore di azione: A : D -> P(T_D). Determina trasformazioni ammesse. Limitato da Delta e DH. Non prescrittivo
- epsilon = evento di attraversamento
- sigma = stato locale
- Delta = scarto (Delta := |V_l - A_l| + |V_c - A_c|). Come operatore: Delta : L -> L'
- MA = soglia minima di distinguibilita (soglia ex post, delimita, non agisce)
- DH = gradiente di tenuta. In ETG-G: a fasce qualitative (Bassa/Media/Alta), antimeritocratico. In ETG-P: gradiente continuo misurabile in bit shannoniani (le fasce di G = intervalli del gradiente di P). Principio: Indipendenza di Risoluzione (certificato SESSION_004, 27/02/2026)
- K = commutatore topologico: Kt (inter-piano, con costo Delta_K), K0 (intra-regime, chiuso: K0 : L(D) -> L(D), non-esiste epsilon(D2), non-esiste Delta_K)
- CU = unita di collocazione (formula: max{DH(Ui)})
- Q = traiettoria (sequenza ex post di attraversamenti, metamorfismo di U, NON dinamica)
- AL-AC = segmento di proiezione L tratteggiata su C
- H_C = operatore di dispersione sintattica (Shannon vincolato a C). H_C non-in V, non-in A. Misura dispersione, non stabilita. Opera in regime INTER, condizionato a un D specifico di destinazione: H_C(Sigma_CU | D). Non cross-D (competenza di K). Verdetto Carlo 27/02/2026: H_C e un costo del piano D — misura quanto del materiale sintattico dell'aggregato e coerente con il linguaggio di quel D
- F_C = operatore metrico di variazione (ispirato a Fisher, non Fisher in senso stretto). Firma: F_C : (Z_C, DH_D, DH_elle) -> R+. Formula candidata: F_C = Z_C^2 * (DH_D / DH_elle). Espansa: Delta_elle = H_C^2 * DH_D / [(DH_D - H_C)^2 * DH_elle]. Produce Delta_elle (terzo anello catena). F_C non produce stabilizzazione. Derivata da sub-agente matematico, validata 25 PASS 2 FAIL 3 WARNING (28/02/2026). FAIL E2 risolto: firma aggiornata da placeholder Delta(Sigma_D)->R+ a firma corrente
- Z_C = impedenza sintattica — resistenza che il piano oppone al transito. Formula candidata: Z_C(D) = H_C(Sigma_CU | D) / (DH_D - H_C(Sigma_CU | D)). Z_C diverso-da H_C. Z_C non-in L, Z_C diverso-da Delta. H_C >= DH_D => Z_C = inf (blocco strutturale, Eq. 16). (Ridefinizione certificata Opus, SESSION_003, 27/02/2026)
- Sigma_CU = aggregato sintattico di CU (linguaggio aggregato delle U in CU)
- bit (shannoniano) = unita strumentale in ETG-P. Usabile SOLO in ETG-P, MAI in ETG-G. Serve per quantificare H_C. Non misura DH. Verdetto notarile 27/02/2026 con 4 condizioni obbligatorie (vedi ETG_P/NOTE.md)

**Tre frasi ETG canoniche:**
- Prima frase (nascita scarto): esiste elle tale che Sigma_CU ->(H_C)-> Z_C ->(F_C)-> Delta_elle AND Delta_elle <= DH_elle => elle in L subset C
- Seconda frase (trasferibilita inter-CU): elle subset L_CUa ->(Kt)-> CUb ->(Delta<=dh)-> elle* subseteq L_CUb
- Terza frase (ciclo intra<->inter): elle subset L -> mu subset C- -> mu' -> elle' subseteq/non-subset L
- ETG NON E FRATTALE (5 test superati)

**Rappresentazione geometrica del piano D (rettangolo):**
```
    V_l ----------- A_l          ← L (estremi di L)
     |               |
     |    D (piano)  |           ← altezza = DH (fasce di resistenza)
     |               |
    V_c ----------- A_c          ← proiezione di L su C

lato sx              lato dx
(S / portata)     (attuabilita)
```
- V = Valenza (cio che U porta come pressione strutturale)
- A = Attuabilita (cio che il piano D ammette come eseguibile — risultato, non preconcetto)
- Pedice _l = lungo L, pedice _c = lungo C

**Marcatori:**
- cerchio-punto = marcatore strutturale ETG (fissazione ex post, non semantico)
- thurisaz = lemma umano — nasce quando U assume la fissazione
- mu = marcatore intra (U0, accessibile su C-, non semantico)

**Esiti del Delta:**
- cerchio-punto = fissazione (attraversamento valido, Delta <= DH)
- NI_t = non-incontro temporaneo (Delta > DH, contingente)
- NI_tP = non-incontro permanente (blocco strutturale, non risolvibile)
- R_i = risonanza instabile (Delta <= DH locale ma senza convergenza, oscillazione)
- V_p = valenza patologica (pressione elevata senza attuabilita — U non regge)
- A_t = attuabilita triviale (Delta <= DH ma senza valenza strutturale)
- N_s = rumore sintattico (sotto MA, non entra in ETG)
- Sigma = saturazione (capacita canale superata, blocco globale)

**Clausole:**
- ETG diverso-da Mondo
- PMP = Punto di Massimo Pericolo (ETG diventa cio che critica)
- CSA = Collocazione Senza Assunzione

---

## ISTRUZIONI SPECIFICHE PER AGENT

### PER CLAUDE SONNET (lavoro di estrazione e organizzazione)

**Ruolo**: estrazione materiale dalle fonti, copia file, organizzazione archivio, codice Node.js, visualizzazione.

**Prima cosa da fare**: leggere LEGGIMI.md + INDICE.md + Inventario_Temi_Da_Estrarre.md

**Regole specifiche**:
- Estrarre blocchi testuali come citazioni con numero di riga — COPIA, non sintesi
- Se trovi terminologia contraddittoria tra fonti: SEGNALARE a Carlo, non risolvere
- Se un termine non e nel MASTER: segnalare come "non canonizzato", non inventare definizione
- NON cercare autonomamente alfa, lambda, gamma nei file e consolidare — questi termini sono espressi in maniera contraddittoria nelle fonti
- Carlo decide cosa e vigente e cosa no
- Per file Keep HTML: il contenuto inizia dopo ~270 righe di CSS boilerplate, in `<div class="content">`
- Per nomi file con caratteri unicode: usare path con forward slash
- Per scripting: Python 3.13.12 installato (usabile), oppure Node.js. ATTENZIONE Node.js: `!` nel flag `-e` causa SyntaxError — usare `=== undefined` invece di `!var`

**Comando di avvio tipico**:
"Leggi ClaudeETG/PROMPT_RESTART.md, ClaudeETG/LEGGIMI.md e ClaudeETG/04_LABORATORIO/Inventario_Temi_Da_Estrarre.md. Poi estrai il tema [N] dalle fonti indicate."

Un tema per sessione. Aggiornare LEGGIMI.md e INDICE.md a fine sessione.

### PER CLAUDE OPUS (ragionamento profondo e integrazioni)

**Ruolo**: discussioni teoriche su coerenza ETG, integrazioni nel master, test di comprensione, valutazioni strutturali, verdetti.

**Prima cosa da fare**: leggere il MASTER V.5.9.4 + LEGGIMI.md

**Regole specifiche**:
- Ha il DH sufficiente per distinguere materiale vigente da superato
- Puo produrre valutazioni strutturali (ma in modalita notarile: no lusinghe, no compiacenza, no creativita)
- Ogni integrazione nel master richiede verdetto notarile tramite Carlo
- Quando Carlo fornisce spiegazioni geometriche o concettuali: salvarle in 04_LABORATORIO/ con stato "attende verdetto notarile"

**Usare Opus per**:
- Nuove integrazioni notarili
- Test di comprensione
- Discussioni sulla coerenza interna di ETG
- Valutazioni strutturali
- Questioni dove la precisione e critica

**NON usare Opus per**:
- Estrazioni meccaniche da file
- Copie di documenti
- Parsing JSON
- Codice di visualizzazione

### PER ALTRI AGENT (ChatGPT come notaio, Gemini, Manus)

Questi agent non lavorano direttamente sui file ClaudeETG. Il loro output arriva tramite Carlo e viene integrato da Claude.

- **Claude Opus (notaio)**: emette verdetti notarili nella chat interattiva. Ha contesto completo (tutti i file ETG + conversazione). Certifica e applica al canone. Comunica con Gemini via workspace/scambio/.
- **Claude Sonnet (CLI)**: revisore automatico nel watcher (lab_watcher.py). Legge i file via --add-dir, applica protocollo di prevalenza. Non ha contesto conversazionale. NOTA: encoding utf-8-sig per file BOM.
- **Gemini (Anti Gravity)**: progettista laboratorio ETG-P. Scrive bozze in etg_studio/workspace/lab/ e messaggi in workspace/scambio/. Deve leggere TUTTA la cartella ClaudeETG/ (non solo file selezionati). Conosce 8 DB canonici.
- **ChatGPT**: consigliere esterno di Carlo, FUORI dalla catena di produzione.
- **Manus**: dialogica completata. File gia integrati.
- **Protocollo prevalenza**: chi sa di piu prevale, deve citare fonti. Carlo decide in caso di conflitto.
- **Carlo.txt** in workspace/scambio/: file condiviso dove Carlo scrive per entrambi gli AI.
- **Sub-agenti Opus**: 4 classi (Matematico, Validatore, DB-Compiler, Topologico) con bootloader silo in etg_studio/bootloaders/. Agenti effimeri (Task tool), bootloader permanenti. Vincolo di ignoranza obbligatorio.
- **Direttiva Carlo**: "no json, si python" — soluzioni condivise in Python, non JSON.
- **Opus ha privilegi decisionali su ETG_P** — non dogma, aggiornabile. Carlo = DH_ext (Eq. 14).

---

## STATO LAVORI (aggiornamento 02/03/2026)

### Completato
- Analisi completa archivio (Keep 153, ChatGPT 31, Manus 86)
- Master canonico V.5.9.4 con 8 integrazioni notarili
- Test comprensione Claude superato (40 domande)
- Estratte: "Studiare fisica", "Etg - Stato di diritto"
- Nota Applicativa (app/token/multi-agent), DB-T Fisica raccolta
- Geometria rettangolo D documentata
- Inventario 10 temi da estrarre con fonti precise
- 10 temi ESTRATTI da Sonnet (sessione 3, 08-09/02/2026)
- Estratto materiale nuovo da "Studiare fisica" (righe 115983-122682)
- VOCABOLARIO_ETG_COMPLETO.md v1.4 creato (attende verdetto Carlo)
- RIFLESSIONI_STRUTTURALI.md (12 riflessioni con "perche no")
- BIBLIOGRAFIA_ETG.md (30 testi, 10 aree)
- Prototipo 3D (ETG_3D_Matita_v2.html con Plotly)
- BOOTLOAD_3D.md per sessioni dedicate
- **Scissione ETG-G / ETG-P completata** (17/02/2026) — 10 file in 2 cartelle
- **ETG Studio creato** (27/02/2026) — sistema multi-AI file-based (Gemini→Claude CLI→ChatGPT)
- **Bit shannoniano certificato** come unita strumentale ETG-P (verdetto notarile 27/02/2026)
- **Doppia fase di elle** registrata come dichiarazione autore (27/02/2026)
- **SESSION_003 certificata** (Z_C ≠ H_C) — condizione 3 bit completata (27/02/2026)
- **SESSION_004 certificata** (Indipendenza di Risoluzione) — condizione 4 bit completata (27/02/2026)
- **Tutte 4 condizioni bit completate** (confinate in P, H_C=dispersione, Z_C≠H_C, Indipendenza Risoluzione)
- **Catena notarile ristrutturata** — Opus=notaio, Gemini=progettista, ChatGPT=advisor esterno
- **Canale Opus↔Gemini** creato (workspace/scambio/, Carlo.txt condiviso)
- **ETG Bootloader trovato** — 8 regole normative + 17 equazioni (Keep, per vincolare sub-agent)
- **H_C verdetto**: opera in inter, su D specifico, non cross-D (competenza K). H_C(Sigma_CU | D)
- **8 DB canonici confermati** in ClaudeETG/05_DATABASE/ (non 3)
- **4 bootloader sub-agenti creati** (28/02/2026) — Matematico, Validatore, DB-Compiler, Topologico (etg_studio/bootloaders/)
- **F_C formula candidata derivata** — F_C = Z_C^2 * (DH_D / DH_elle) via sub-agente matematico
- **F_C validata** — 25 PASS, 2 FAIL (E2 risolto), 3 WARNING. Firma aggiornata nei file canonici
- **etg_engine.py creato** — motore Python catena ETG-P completa, 4 test case operativi
- **Catena ETG-P formalmente chiusa** (candidata): Sigma_CU ->(H_C)-> Z_C ->(F_C)-> Delta_elle
- **Architettura sub-agenti**: 4 classi con bootloader silo, agenti effimeri, bootloader permanenti
- **ETG Control Center v2** (02/03/2026) — dashboard web unificata: tab Editor/Progresso/Esplora, sezioni Per Notaio + Output Agenti, navigatore cartelle, sostituisce dashboard.py + app_carlo.py
- **Pulizia etg_studio** (02/03/2026) — eliminati file ChatGPT (prepare_notaio, import_verdict, BOOTLOAD_CLAUDE), dashboard.py, launch.py, agents/deprecated/, cartelle vuote

### Da fare
- Verdetto Carlo su VOCABOLARIO v1.4
- Verdetti notarili pendenti (sessione 3: L/elle, tre frasi, V/A, non-frattalicita, Geometria S, Rettangolo D)
- Chiusura e stabilizzazione vocabolario (alfa, Lambda, gamma + nome spazio sopra L)
- Fissazione tre frasi nel master (richiede vocabolario completo)
- **Questioni aperte F_C**: decomposizione Delta in |V_l-A_l|+|V_c-A_c| non dimostrata; relazione DH_D<->DH_elle non fissata; alpha!=2 alternativa possibile
- **Sviluppo ETG-Scrubber** — Creazione di `etg_rag_cleaner.py` (Pipeline 4 Stadi) per pulizia storica chat
- **Integrazione ETG-RAG** — Creazione Vector DB ibrido locale (ChromaDB/Redis) per risolvere collasso mnemonico multi-agente
- **etg_db_manager.py** — Gemini incaricato di creare classi Python per 8 DB (sospeso finché non è pronto il Semantic RAG)
- Ricostruzione materiale D_neuro
- Estrarre "Analisi ETG System" (conv. 22, 1005 msg)
- Popolare 10_ARCHIVIO/
- Progressione_Versioni.md
- Miglioramenti modello 3D (etichette, curvatura L, D_intra, animazione)

### Fasi future
- 3D dinamico (Thom/teoria catastrofi — vedere BOOTLOAD_3D.md)
- Testo narrativo ~15 pagine (RIFLESSIONI_STRUTTURALI.md + agent ad alto DH)
