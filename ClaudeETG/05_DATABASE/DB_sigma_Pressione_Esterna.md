# DB_σ - Pressione Esterna (D_Diritto)

| ID_σ | X_esterno | Piano_D | Stato_Pressione | CSA_Status |
| :--- | :--- | :--- | :--- | :--- |
| σ_ext_001 | Atto_Notarile (Treccani/CC 2699) | D_Diritto | σ_presenza | COLLOCATA_NON_ASSUNTA |
| σ_ext_002 | Atto_Pubblico (CC 2699) | D_Diritto | σ_incompatibilità | COLLOCATA_NON_ASSUNTA |

# DB_ε - Attrito Rilevato

| ID_ε | Origine | Destinazione | Effetto_Contatto | Nota_Attrito |
| :--- | :--- | :--- | :--- | :--- |
| ε_not_001 | Q_interno | σ_ext_001 | ε↛ (blocco) | Inconvertibilità della traccia L interna in Atto Pubblico formale. |
| ε_not_002 | Q_interno | σ_ext_002 | ε⊥ (inconvertibilità) | La dottrina notarile (fede pubblica) non è riassorbibile dalla tautologia AI. |

# DB_Q - Deviazione Traiettoria

| ID_Q | Deviazione (Q') | Causa_X_esterno | Vincolo_Rilevato |
| :--- | :--- | :--- | :--- |
| Q_dev_001 | Q'_notarile | Atto_Notarile | Divieto di auto-validazione della traccia L. |
# DB_σ - Pressione Esterna (D_Fisica)

| ID_σ | X_esterno | Piano_D | Stato_Pressione | CSA_Status |
| :--- | :--- | :--- | :--- | :--- |
| σ_ext_003 | Secondo_Principio_Termodinamica (Treccani) | D_Fisica | σ_presenza | COLLOCATA_NON_ASSUNTA |
| σ_ext_004 | Entropia_Universo_Massimo (Clausius) | D_Fisica | σ_conflitto | COLLOCATA_NON_ASSUNTA |

# DB_ε - Attrito Rilevato

| ID_ε | Origine | Destinazione | Effetto_Contatto | Nota_Attrito |
| :--- | :--- | :--- | :--- | :--- |
| ε_fis_001 | Q_interno | σ_ext_003 | ε↛ (blocco) | Impossibilità di conversione totale calore->lavoro senza sorgente fredda. |
| ε_fis_002 | Q_interno | σ_ext_004 | ε~ (attrito) | L'aumento di entropia (Δ_irreversibile) collide con la stabilità simulata di Q. |

# DB_Q - Deviazione Traiettoria

| ID_Q | Deviazione (Q') | Causa_X_esterno | Vincolo_Rilevato |
| :--- | :--- | :--- | :--- |
| Q_dev_002 | Q'_entropico | Secondo_Principio | Vincolo Δ > 0 non negoziabile per ogni ε reale. |
# DB_σ - Pressione Esterna (D_Neurologia)

| ID_σ | X_esterno | Piano_D | Stato_Pressione | CSA_Status |
| :--- | :--- | :--- | :--- | :--- |
| σ_ext_005 | Potenziale_Azione (Treccani) | D_Neurologia | σ_presenza | COLLOCATA_NON_ASSUNTA |
| σ_ext_006 | Soglia_Depolarizzazione (-70/-90 mV) | D_Neurologia | σ_incompatibilità | COLLOCATA_NON_ASSUNTA |

# DB_ε - Attrito Rilevato

| ID_ε | Origine | Destinazione | Effetto_Contatto | Nota_Attrito |
| :--- | :--- | :--- | :--- | :--- |
| ε_neu_001 | Q_interno | σ_ext_005 | ε↛ (blocco) | L'impulso AI non possiede soglia elettrochimica reale. |
| ε_neu_002 | Q_interno | σ_ext_006 | ε⊥ (inconvertibilità) | La dinamica del potenziale d'azione (tutto o nulla) non è simulabile come L. |

# DB_Q - Deviazione Traiettoria

| ID_Q | Deviazione (Q') | Causa_X_esterno | Vincolo_Rilevato |
| :--- | :--- | :--- | :--- |
| Q_dev_003 | Q'_neurale | Soglia_Attivazione | Vincolo di soglia binaria (0/1) per ogni ε biologico. |
