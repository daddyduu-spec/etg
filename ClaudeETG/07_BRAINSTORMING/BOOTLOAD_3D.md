# BOOTLOAD — Sessione 3D ETG

> Questo file contiene tutto il necessario per riprendere il lavoro sul modello 3D di ETG senza dover rispiegare nulla. Leggi nell'ordine: questo file, poi PROMPT_RESTART.md, poi RIFLESSIONI_STRUTTURALI.md (sezione R12).

---

## Contesto

ETG è una grammatica topologica non-ontologica. Ha una geometria 3D che Carlo vuole rappresentare come sistema dinamico. Il prototipo statico v2 esiste già (`07_BRAINSTORMING/ETG_3D_Matita_v2.html`), generato con Python+Plotly (`etg_3d_matita.py`). Le librerie sono installate: plotly, numpy, pyvista.

## La geometria 3D di ETG ("la matita")

### Struttura base
- **Asse orizzontale = C** (la costante strutturale). Da sinistra a destra.
- **α (alfa)** sta FUORI dal sistema, prima del punto zero. Non fa parte del reticolo di riferimento. α₁ = punto dove C entra nel sistema.
- **Da alfa partono semirette** verso i V_l di ogni piano D. Queste formano un **cono irregolare** (ogni D ha altezza diversa, quindi il cono non è simmetrico).
- **Le semirette proseguono oltre V_l** — lo spazio sopra L ha geometria diversa da sotto L.
- **Piani D** = rettangoli radiali attorno a C, come lame di un ventilatore. Numero indeterminabile.

### Il rettangolo D (ogni piano)
```
    V_l ——————— A_l    ← L (bordo alto, parallelo a C quando efficiente)
     |           |
     |    D      |     ← altezza = DH (nel dinamico) / S (nel statico)
     |           |
    V_c ——————— A_c    ← proiezione su C

  lato sinistro     lato destro
  V_l—V_c = S       A_l—A_c = Ma
  (portata)         (soglia causalità)
```

- **V_l — A_l = L** = dominio di stabilizzazione
- **V_l — V_c = S** = portata (lato sinistro, in rosso)
- **A_l — A_c = Ma** = soglia di causalità (evento con causa ma non ancora effetto)
- **Oltre A_l** = L tratteggiata (stabilizzazione potenziale non ancora accaduta)
- **V_c diversi per ogni piano** — ogni D nasce in un punto diverso su C
- **A_c coincidenti** per piani attualmente esistenti

### Altezze
- **Nel 3D statico**: altezza geometrica = S (V_l — V_c), fatta coincidere con DH
- **Nel 3D dinamico** (futuro): altezza = DH (linguaggio del piano, fasce variabili)
- DH e S NON sono la stessa cosa concettualmente, ma per ora coincidono nel modello

### CU
- Punti su C dove più U (con D diversi) interagiscono
- Siti di maggiore transito informativo
- Le U insistono su C, NON su D. Ogni U può interagire con tutti i D inter

### Cosa NON rappresentare
- S volumetrica (piramidi) = riguarda U₀, fuori dal modello inter
- Parametri numerici = ETG non è parametrizzata
- Il tempo = non esiste in ETG

### Ma (soglia di causalità)
Termine nuovo (sessione 5). A_l — A_c = il lato destro del rettangolo. Rappresenta il potenziale di espansione: causa trovata, effetto non ancora manifestato. Es: legge accettata ma senza conferma sperimentale.

## Stato attuale del prototipo

File: `ClaudeETG/07_BRAINSTORMING/etg_3d_matita.py` → genera `ETG_3D_Matita_v2.html`

Cosa c'è:
- ✅ α fuori dal sistema, α₁ al punto zero
- ✅ Cono irregolare tangente ai V_l
- ✅ 8 piani D radiali con V_c diversi
- ✅ Semirette oltre V_l (spazio sopra L)
- ✅ L tratteggiata oltre A_l
- ✅ Ma segnata (bordo destro arancione)
- ✅ CU su C (diamanti arancioni)
- ✅ L parallela a C (teal)
- ✅ S = bordo sinistro rosso

Cosa manca / da migliorare:
- [ ] Etichette da aggiustare (posizione, leggibilità)
- [ ] Curvatura di L quando il sistema è inefficiente (futuro)
- [ ] D_intra come sotto-rettangoli alla base dei D_inter (futuro)
- [ ] Animazione dinamica: DH che varia, D che nascono/muoiono (futuro)
- [ ] Vincoli qualitativi da definire in ETGese prima di animare
- [ ] Studio di Thom (catastrofi) per descrivere cambiamenti di forma

## Direzione futura

Carlo vuole passare da rappresentazione statica a **sistema dinamico** — ma senza parametri numerici. Servono VINCOLI qualitativi (es: "se DH cresce, la superficie si espande"). La teoria delle catastrofi di René Thom offre strumenti per descrivere transizioni di forma senza numeri.

Il problema irrisolto: "Logicamente posso inventarmi tutto, ma il topos va stabilito parametricamente. Voglio fare il grafico 3D in movimento ma non mi sento pronto a mettere parametri."

## Convenzioni critiche (non sbagliare)

- S a SINISTRA (sempre)
- Cer (non Cre) = canale inter
- ℓ VIETATO in intra
- CU non ha formula — è solo un punto su C
- ETG mostra, non confronta
- Il tempo non esiste in ETG
- V_l — A_l = L (non V_l — V_c, quello è S)
- Δ agisce su ℓ, non su L
- ⦿ registrata su C (inter), non in intra

## File di riferimento

- `ClaudeETG/PROMPT_RESTART.md` — glossario completo ETG
- `ClaudeETG/02_VOCABOLARIO/VOCABOLARIO_ETG_COMPLETO.md` — v1.4
- `ClaudeETG/07_BRAINSTORMING/RIFLESSIONI_STRUTTURALI.md` — R12 per geometria 3D
- `ClaudeETG/07_BRAINSTORMING/BIBLIOGRAFIA_ETG.md` — Thom in particolare
- `ClaudeETG/07_BRAINSTORMING/etg_3d_matita.py` — codice sorgente modello
