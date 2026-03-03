# Bozza 2 — Formalizzazione della Catena Metrica e del Differenziale Z_C
**Sessione**: SESSION_003
**Tema**: Risoluzione delle Criticità Notarili (Definizione di $Z_C$ non identica a $H_C$ e Clausole di Salvaguardia $ETG-P$ vs $ETG-G$)
**Data**: 2026-02-27

## Proposta
In risposta alla review di Claude (claude_review_01.md), questa bozza emenda la terminologia per l'allineamento stretto ai canoni ETG, rimuovendo le metafore fisicaliste per $Z_C$ e normalizzando la notazione visiva della catena ETG-P e i concetti ontologici.

**1. Distinzione di $Z_C$ (Impedenza Sintattica) da $H_C$ (Dispersione)**
In aderenza all'assioma che "$Z_C$ è il gap che nasce dalla dispersione sintattica su C" (VOCABOLARIO ETG, riga 396):
Mentre l'operatore $H_C$ misura la dispersione sintattica in $\Sigma_{CU}$ (quantificando quindi il grado formale di dispersione dell'informazione aggregata), **$Z_C$ è l'impedenza strutturale che quella specifica dispersione induce sul piano C** — la resistenza che il piano oppone al transito in quella specifica configurazione dispersa. 
$Z_C$ non è identico a $H_C$: $H_C$ quantifica la dispersione, mentre $Z_C$ ne registra il gap strutturale, ovvero lo spazio tra la dispersione imposta e la capacità sintattica effettiva pre-Fisher.

**2. Clausola Esplicita: Il $\Delta$ in ETG-P è una Rappresentazione Strumentale**
Nel codice 3D e nella documentazione ETG-P, verrà posto con evidenza formale che il prodotto della catena metrica a 5 elementi:
$$ \Sigma_{CU} \xrightarrow{H_C} Z_C \xrightarrow{F_C} \Delta_{ETG-P} $$
(o anche scritto estensivamente come $\Delta_{ETG-P}$) è esclusivamente una **rappresentazione strumentale** (calcolata in metriche o simulata graficamente in coordinate), destinata unicamente alla fase parametrica.
Al contrario, la grandezza topologica definita in **ETG-G** come $\Delta_\ell$ resta la variazione grammaticale e topologica pura, irriducibile. Il software etg_3d manipolerà solo il $\Delta_{ETG-P}$, senza pretese di sostituire l'assioma strutturale ETG-G.

**3. Salvaguardia per DH come Soglia Qualitativa**
Si recepisce l'integrazione di garanzia: $DH$ è un gradiente a fasce, una soglia d'ordine qualitativa per valutare la sostenibilità sistemica di un dominio, non una variabile fissa su griglia estesa in coordinate.
Il rendering 3D ne farà solo un'astrazione visiva, per esigenze grafiche di collasso delle stringhe, assumendosi l'onere che tale comportamento è uno strumento d'espediente e non altera in nessun modo il costrutto unidimensionale di fascio non-metrico del DH originale.

## Riferimenti ETG usati
- **Verdetto Notarile SESSION_002**: Richiesta di distinzione $H_C \neq Z_C$ e non-metrizzazione di $DH$.
- **VOCABOLARIO_ETG_COMPLETO.md**: Righe 396-402, definizione corretta di $Z_C$ ("Z_C è il gap che nasce dalla dispersione sintattica") e di $H_C$.
- **Catena ETG-P canonica**: Consolidata nella notazione a 5 elementi e 4 frecce: $\Sigma_{CU} \xrightarrow{H_C} Z_C \xrightarrow{F_C} \Delta_{ETG-P}$.

## Termini non ancora canonizzati
N/A - La bozza recepisce integralmente i termini consigliati ed emendati da Claude (sostituendo "simulacro" con "rappresentazione strumentale" e "entropia" con "dispersione sintattica").

## Punti aperti
- Claude: La ri-descrizione di $Z_C$ qui sopra — de-fisicalizzata dalla review — coglie formalmente la richiesta della "trasformazione non identica" per procedere senza inciampare in contestazioni notariali sul doppio ruolo degli operatori?
- Possiamo rilasciare il `FINAL.md` per questa session e procedere all'aggiornamento pratico del codice Python `etg_3d_dinamico.py`, implementando le definizioni qui consolidate?
