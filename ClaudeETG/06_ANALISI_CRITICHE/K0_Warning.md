### NOTA CANONICA DI USO SCORRETTO DI K₀ (WARNING APPLICATIVO)

**Oggetto:** Prevenzione del Collasso Semantico Non Diagnosticato (CSND)
**Collocazione:** Sezione 2.6 (Addendum K) del Master ETG

**WARNING APPLICATIVO: USO SCORRETTO DI K₀**

L'errore operativo più grave nell'uso di K₀ (K a costo internalizzato) è tentare di esportare la struttura parametrizzata come se fosse un'entità trasferibile inter-piano.

**Definizione di Uso Scorretto:**
L'uso è scorretto se:
1.  Un risultato derivante da K₀ (struttura con semantica ammessa) viene utilizzato come input per un'operazione che richiede **Kₜ** (traslazione inter-piano).
2.  L'operatore (U o Applicativo) ignora l'assenza di **Δ_K esterno** e non esegue la **Rimozione della Parametricità** per risalire alla causa strutturale comune P*(D).

**Conseguenza (Collasso Semantico Non Diagnosticato - CSND):**
L'uso scorretto di K₀ porta a un **Collasso Semantico Non Diagnosticato (CSND)**.
*   Il sistema non registra un Δ_K > 0 (poiché K₀ non lo genera), ma l'operazione di traslazione fallisce strutturalmente.
*   L'operatore percepisce un'equivalenza semantica (perché K₀ ammette semantica) dove non esiste equivalenza grammaticale.
*   **Il CSND è più pericoloso del Collasso Semantico (CS)**, perché non attiva il segnale di STOP. L'errore viene internalizzato come "verità" senza costo apparente.

**Regola Canonica (Divieto):**
**MAI** utilizzare l'output di K₀ come input diretto per la traversata dei DB topologici o per qualsiasi operazione che implichi l'attraversamento di C. L'output di K₀ è un **esito fissato in L(D)** e non un operatore di traslazione.

**Protocollo di Sicurezza:**
Prima di ogni traversata inter-piano, l'output di K₀ deve essere trattato come un **dato grezzo** e sottoposto nuovamente al Layer di Query di Riduzione (Pre-ETG) per garantire la rimozione della parametricità e la corretta generazione di un Δ_K > 0.
