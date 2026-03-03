# TEMA 10: QUESTIONARIO CARTACEO PER INPUT U

> Estratto: 08/02/2026 (sessione Sonnet)
> Tipo: strumento operativo
> Metodo: copia blocchi con riferimento fonte e riga — NESSUNA sintesi autonoma
> Riferimento canonico: ETG_MASTER_V5.9.4_CANONICAL.md

---

## SIGNIFICATO (dall'Inventario Temi)

ChatGPT (notaio) ha proposto un questionario su carta per raccogliere input da U. Carlo lo ritiene utile. Sonnet deve cercarlo e recuperarlo.

---

## RISULTATO DELLA RICERCA

### Fonti cercate:
- conversations.json (tutte le 31 conversazioni) — keyword: "questionario", "carta", "domande", "input U", "paper", "compilare", "scheda", "modulo"
- "Studiare fisica" (studiare_fisica_extracted.txt) — stesse keyword
- Keep (153 file) — stesse keyword
- manus (86 file) — stesse keyword

### Esito:
**Il questionario cartaceo per input U NON e stato trovato letteralmente** in nessuna delle fonti cercate.

---

## MATERIALE STRUTTURALMENTE CORRELATO

I blocchi seguenti non contengono il questionario ma sono i piu vicini al concetto.

### Blocco A1: "Studiare fisica" righe 27825-27830 — Campi minimi obbligatori per epsilon

**ChatGPT notaio (riga 27825):**
> specificare quali campi minimi devono essere obbligatori per un epsilon in una nuova ricerca, altrimenti il sistema degrada.

**Carlo (riga 27830):**
> [...] lasciamo stare quali sono i campi minimi che devono essere obbligatori per un... [...] Qui c'e il ribadire la necessita di un... di applicativi di supporto. [...] c'e la necessita di un'interfaccia di immissione specializzata per gli ambiti della ricerca. E una grammatica che puo essere integrata ad altri sistemi [...] magari come semplici campi da immettere non escludibili, che mantengono conforme il processo neurologico a questa grammatica dei linguaggi.

---

### Blocco A2: "Studiare fisica" righe 29264-29271 — Campi ETG obbligatori per inserimento

**ChatGPT notaio (righe 29264-29271):**
> Contenuto inserito in tempo reale con campi ETG obbligatori:
> - D (piano)
> - regime
> - (V,A) (valenza/attuabilita)
> - Delta
> - DH
> - K
> - epsilon

---

### Blocco A3: "Studiare fisica" righe 81177-81249 — UI app ETG per neurologo

**Carlo (riga 81177):**
> mostrami un ui di un app etg per un neurologo. laddove credo che quell app debba per forza basarsi su un db topologico di D_neurologia.

**ChatGPT notaio (righe 81235-81248):**
> UI di un'app ETG per un neurologo (come la vede lui)
>
> Schermata 1 — Input disciplinare
> Titolo: "Descrivi il fenomeno osservato"
> Campi possibili:
> - Termine noto (autocomplete dal DB neurologico): es. shallow processing, deep encoding, exposure
> - oppure breve descrizione libera (facoltativa)
>
> Il neurologo non sceglie categorie ETG.

---

### Blocco A4: Conv. 21 "Analisi ETG System" msg 905 — Caso "cerco lavoro ASL"

**ChatGPT notaio — architettura applicativa:**
> Livello A — Input (LLM puro):
> - raccolta dati narrativi di U
> - linguaggio naturale
> - ambiguita ammessa
> - nessuna validazione
>
> Livello B — Collocazione (ETG = Q):
> - mappa l'input di U in: requisiti, vincoli, compatibilita procedurali
> - non valuta il valore di U
>
> Livello C — Output istituzionale:
> - restituisce a istituzione: forme compatibili, non il soggetto
> - la decisione resta umana e istituzionale

---

## FONTI KEEP — STRUTTURA CAMPI, DB PILOTA, SCHEMA DI REGISTRAZIONE

### Blocco K1: "[APPUNTI] db-etg come memoria del percorso cognitivo" (05/01/2026) — Campi per epsilon + schema tracciamento

**ChatGPT notaio — struttura sigma (stato locale):**
> sigma_i permette di: rappresentare una collocazione informativa locale, non come contenuto, ma come configurazione operativa, con: Piano D, regime, (V, A) come funzioni di collocazione, DH locale, K attivo, Delta residuo.
> Questo non e un fatto enciclopedico. E una fotografia funzionale di "come quell'informazione e maneggiabile".

**ChatGPT notaio — struttura epsilon (evento di attraversamento):**
> epsilon permette di: registrare che un passaggio e avvenuto / perche e avvenuto (Delta ≤ DH, K intersecato ≠ vuoto) / senza dire nulla sul contenuto semantico narrativo.
> Questo e cruciale: non registra cosa si e pensato, ma che tipo di attraversamento e stato possibile.

**ChatGPT notaio — limite invalicabile:**
> Questo sistema NON: elimina la soggettivita / elimina l'arbitrarieta iniziale / garantisce verita
> Questo sistema PUO: ridurre allucinazione strutturale / rendere confrontabili dottrine / permettere computazione sui percorsi

---

### Blocco K2: "[Notaio] DB in Etg di D fisica" (26/12/2025) — DB operativo pilota con 6 tabelle

**ChatGPT notaio — struttura DB modulare:**
> Il database ETG e composto da tabelle indipendenti, unibili tramite chiavi logiche non temporali.
>
> 1) TABLE: ETG_ARTIFACTS — cosa viene collocato (artifact_id, name, formal_type, domain_D, subdomain, status_L, description)
> 2) TABLE: ETG_PLACEMENT — collocazione topologica (placement_id, artifact_id, sigma_C, lambda_L, pi_DH, class_ETG, zone_ETG)
> 3) TABLE: ETG_FIELD_X — massa/saturazione campo X (field_id, artifact_id, x_value, saturation, scope)
> 4) TABLE: ETG_RELATIONS — relazioni interne al piano D (relation_id, source_id, target_id, relation_type, validity_scope)
> 5) TABLE: ETG_FRICTIONS — attriti e limiti (friction_id, artifact_id, alpha_s, alpha_l, alpha_p, note)
> 6) TABLE: ETG_METADATA — certificazione notarile (meta_id, artifact_id, certified_by, version, notes)
>
> Vincoli: Nessuna estensione oltre L comprovato / Nessun uso di L tratteggiato / Nessuna predizione / Solo collocazione, relazione, certificazione

---

### Blocco K3: "[LABORATORIO] Rendere ETG operabile senza chiuderla" (05/01/2026) — Schema minimo di registrazione

**ChatGPT notaio — 3 livelli:**
> L1 — Grammatica ETG (immutabile): simboli, relazioni ammesse, vincoli di attraversamento, condizioni di fallimento. Nessun software, solo specifica stabile.
>
> L2 — Schema di registrazione ETG (da definire): Non e un DB di contenuti, ma di tracce. Ogni evento di ricerca deve poter essere registrato come: stato sigma, evento epsilon, fallimento epsilon-non, traiettoria Q. Questo e il cuore applicativo.
>
> L3 — Strumento di supporto (posticipato): editor, API, plugin, automazioni. Vietato progettarlo ora, si progetta solo dopo L2.

**ChatGPT notaio — Schema minimo vincolato:**
> Lo schema deve: accettare il fallimento / accettare l'incompletezza / non richiedere verita / non richiedere contenuto disciplinare / essere usabile da umani e macchine

---

### Blocco K4: "[ETG] SCHEMA MINIMO — FORMALIZZAZIONE STRUTTURALE DI L" (02/01/2026) — Formalizzazione L strutturata

**ChatGPT notaio — L come insieme strutturato di affermazioni valutabili:**
> L = { l_1, l_2, ... l_n } con: ogni l_i valutabile rispetto a V, A, dh, Delta
>
> l_i puo essere: compatibile con L / tollerata da L / instabile in L / candidata a uscire da L
>
> Funzione di valutazione intra-L:
> ETG dice: questa l_i ha compatibilita bassa con la L di riferimento / questa l_i ha V coerente ma A incoerente / questa l_i ha dh insufficiente per stare in L

---

## IPOTESI SULLA COLLOCAZIONE DEL QUESTIONARIO

Il "questionario cartaceo per input U" potrebbe trovarsi:

1. In una **conversazione non ancora estratta** da conversations.json — la conv. 22 "Analisi ETG System" (1005 messaggi, indicata come non ancora estratta nel LEGGIMI)
2. In un **messaggio orale di Carlo** durante la sessione Opus 2, non trascritto
3. In un **file Keep** con nome non riconducibile direttamente al tema (cerco con termini diversi)

### Ricerche aggiuntive effettuate senza successo:
- "questionario" in tutte le fonti → 1 match irrilevante (riga 82239, contesto DB-T neurologo)
- "carta" + "domande" → nessun match ETG-rilevante
- "modulo" + "raccolta" → nessun match
- "scheda" + "input" → nessun match

---

## STATO DEL DOCUMENTO

- **Tipo**: segnalazione di assenza + raccolta materiale correlato
- **Completezza**: INCOMPLETO — il questionario non e stato trovato
- **Attende**: indicazione da Carlo sulla fonte esatta del questionario
- **Fonti cercate**: "Studiare fisica", etg_stato_diritto_extracted.txt, conversations.json (31 conv.), Keep (153 file), manus (86 file)
- **Materiale correlato trovato**: 4 blocchi da "Studiare fisica" + 4 blocchi Keep su struttura campi, DB pilota, schema registrazione, L strutturata
- **Aggiornamento 09/02/2026**: aggiunti 4 blocchi Keep (K1: campi sigma/epsilon, K2: DB pilota 6 tabelle, K3: schema minimo 3 livelli, K4: L come insieme strutturato)
