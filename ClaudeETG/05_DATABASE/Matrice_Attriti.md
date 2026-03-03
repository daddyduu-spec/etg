# Matrice σ × ε: Tabella di Incidenza degli Attriti (ETG-C)

| σ (Tipo) | ε (Esito) | Δ (Osservato) | DH (Rif.) | Sorgente |
| :--- | :--- | :--- | :--- | :--- |
| σᵈ | Descrittivo | n.d. | n.d. | manus_2.txt |
| σᵈ | Descrittivo | n.d. | n.d. | manus_4.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_11.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_11.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_11.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | OK | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | DH | n.d. | nota_15.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_15.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | OK | n.d. | n.d. | nota_15.txt |
| σᵈ | OK | n.d. | n.d. | nota_15.txt |
| σᵈ | OK | n.d. | n.d. | nota_15.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_15.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_15.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_15.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_15.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_17.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_18.txt |
| σᶜ | Descrittivo | n.d. | n.d. | nota_2.txt |
| σᵈ | OK | DH | n.d. | nota_2.txt |
| σᵈ | FAIL | DH | n.d. | nota_2.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_2.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_3.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_4.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_4.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_4.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_4.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_5.txt |
| σᵈ | OK | n.d. | n.d. | nota_5.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_5.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_5.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_6.txt |
| σᵈ | OK | n.d. | n.d. | nota_6.txt |
| σᵈ | OK | DH | n.d. | nota_6.txt |
| σᵈ | Descrittivo | DH | n.d. | nota_6.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_6.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_6.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_8.txt |
| σᵈ | FAIL | n.d. | n.d. | nota_8.txt |
| σᵈ | Descrittivo | n.d. | n.d. | nota_8.txt |
| σᵈ | FAIL | DH | n.d. | nota_8.txt |
# Isobare di Resistenza e Pattern Cross-D (ETG-C)

## 1. Zone ad alta densità di ε↛ (Punti di Collasso)

| Sorgente | Piani D Coinvolti | Frequenza Fallimenti |
| :--- | :--- | :--- |
| manus_3.txt |  | 1 |
| nota_15.txt | D_Biologia, D_Fisica, D_Neurologia | 14 |
| nota_2.txt | D_Neurologia | 4 |
| nota_3.txt |  | 1 |
| nota_5.txt | d_intra_Neurologia | 2 |
| nota_6.txt | D_Neurologia | 4 |
| nota_8.txt |  | 3 |

## 2. Pattern Cross-D (Resistenze Trasversali)

| Sorgente | Intersezione Piani D | Note di Attrito |
| :--- | :--- | :--- |
| nota_15.txt | D_Biologia, D_Fisica, D_Neurologia | Rilevato scarto Δ persistente tra regimi diversi. |
# Vincoli di Non-Espansione (ETG-C)

Questi vincoli definiscono i "punti di arresto" dove l'operatore AU MANUS deve dichiarare l'impossibilità di procedere, impedendo derive autoritative e allucinazioni strutturali.

## 1. Vincoli su Δ (Scarto Informativo)

| Vincolo | Descrizione | Riferimento Note |
| :--- | :--- | :--- |
| **Δ_MAX_PERSISTENZA** | Qualsiasi Δ che appare in più di 5 note (ε↛) senza una successiva ε→ (riuscita) deve essere marcato come **Resistenza Topologica Permanente**. Non deve essere riassorbito, ma conservato come informazione primaria. | Note 1, 4, 6, 8, 10 (Esempio) |
| **Δ_NON_COLMABILE** | Il Δ generato da un fallimento cross-D (es. D_Neurologia ↔ D_Fisica) non deve mai essere colmato dall'AI. L'unica azione ammessa è la registrazione di **Q'** (Deviazione di Traiettoria). | Note 8, 13, 14 |

## 2. Vincoli su σ (Stato Locale)

| Vincolo | Descrizione | Riferimento Note |
| :--- | :--- | :--- |
| **σ_NO_PROMOZIONE** | Uno stato descrittivo (**σᵈ**) non deve mai essere promosso a stato collocato (**σᶜ**) dall'AI, anche se le coordinate (V, A) sono inferibili. La promozione richiede sempre una **validazione notarile esterna (U)**. | Note 3, 5, 7 |
| **σ_NON_UTILIZZABILE** | Uno stato non collocabile (**σᵘ**) non deve essere utilizzato come `σ_origine` per un nuovo evento ε. La sua unica funzione è quella di marcare il limite. | Note 6, 19 |

## 3. Vincoli su DH (Dottrina di Riferimento)

| Vincolo | Descrizione | Riferimento Note |
| :--- | :--- | :--- |
| **DH_NO_ESTENSIONE** | Il DH operativo (**DHₒ**) non deve essere esteso a un Piano D adiacente. Il DH è locale e non comparabile tra D. | Note 8, 15 |
| **DH_IMPLICITO_STOP** | Un evento ε basato su DH implicito (**DHₜ**) non può essere utilizzato per fondare un nuovo vincolo di non-espansione. | Note 1, 2, 4 |

