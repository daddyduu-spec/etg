import matplotlib.pyplot as plt
import numpy as np

# Laboratorio Gemini: Prototipo DB Topologico ETG_P
# Obiettivo: Posizionare i lemmi (l) di vari Piani D su un piano asettico V/A e visualizzarne l'isomorfismo

class Lemma:
    def __init__(self, nome, piano_d, v, a, carico_strutturale=1.0):
        """
        :param nome: Testo dell'equazione o del lemma
        :param piano_d: La disciplina d'appartenenza
        :param v: Pretesa Teorica (V in [0, 1])
        :param a: Attuabilità / Verificabilità (A in [0, 1])
        :param carico_strutturale: Dipendenze (Sigma CU)
        """
        self.nome = nome
        self.piano_d = piano_d
        self.v = v
        self.a = a
        self.carico = carico_strutturale
        # Asimmetria strutturale: delta teorico (V - A)
        # Se V >> A, estrema speculazione
        # Se A >> V, puro evento non teorizzato 
        self.asimmetria = self.v - self.a
        # L'oscillazione metrica approssimata per simulare la parametrizzazione futura
        self.storia_posizioni = [(self.asimmetria, self.carico)]

class DBTopologico:
    def __init__(self):
        self.lemmi = []

    def aggiungi_lemma(self, lemma):
        self.lemmi.append(lemma)

    def draw_mappa(self):
        plt.figure(figsize=(10, 7))
        plt.title('ETG_P: Mappatura Multi-D (Scorciatoie Cognitive)')
        plt.xlabel('Asimmetria (V - A) -> Sinistra (Tutto V), Destra (Tutto A)')
        plt.ylabel('Carico Strutturale ($\Sigma_{CU}$)')
        plt.axvline(0, color='grey', linestyle='--', linewidth=0.5, label='Soglia di Risonanza V=A')

        # Colori distinti per i piani D
        colori_piani = {
            'D_Fisica': 'blue',
            'D_Psicoanalisi': 'red',
            'D_Diritto': 'green',
            'D_Economia': 'orange'
        }

        for l in self.lemmi:
            colore = colori_piani.get(l.piano_d, 'black')
            x = l.asimmetria
            y = l.carico
            plt.scatter(x, y, color=colore, s=l.carico*50, alpha=0.7)
            plt.text(x + 0.02, y + 0.02, f"{l.nome}\n({l.piano_d})", fontsize=8)

        # Traccio zona di rottura/intuizione (L Tratteggiata/Alto Delta)
        plt.axvspan(0.7, 1.0, color='red', alpha=0.1, label="Alta Pretesa / Indimostrabile (C.S.)")
        plt.axvspan(-1.0, -0.7, color='green', alpha=0.1, label="Puro Evento A-Teorico")

        plt.xlim(-1.1, 1.1)
        plt.ylim(0, max(l.carico for l in self.lemmi) + 2)
        plt.legend(loc='upper right')
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()
        plt.savefig('mappa_etg.png')
        print("Mappa generata e salvata come 'mappa_etg.png'")

if __name__ == "__main__":
    db = DBTopologico()

    # --- INSERIMENTO LEMMI (Proof of Concept) ---
    # 1. FISICA
    # F=ma classico: Fortissima stabilità V e A
    db.aggiungi_lemma(Lemma("F=ma (Newton)", "D_Fisica", v=0.9, a=0.9, carico_strutturale=10.0))
    # Principio di Indeterminazione: Limite sull'osservabilità (Alto V, ma l'Attuabilità cala per il collasso)
    db.aggiungi_lemma(Lemma("Indeterminazione (Heisenberg)", "D_Fisica", v=0.9, a=0.3, carico_strutturale=8.0))
    # E=mc^2 paradigma limite
    db.aggiungi_lemma(Lemma("E=mc^2 (Einstein)", "D_Fisica", v=1.0, a=0.8, carico_strutturale=12.0))
    # Stringhe: pretesa cosmica (V), zero attuabilità (A)
    db.aggiungi_lemma(Lemma("Teoria delle Stringhe", "D_Fisica", v=1.0, a=0.05, carico_strutturale=3.0))

    # 2. PSICOANALISI
    # Inconscio: costrutto teorico altissimo, attuabilità empirica nulla
    db.aggiungi_lemma(Lemma("L'Inconscio", "D_Psicoanalisi", v=0.9, a=0.1, carico_strutturale=7.0))
    
    # 3. DIRITTO
    # Omicidio Colposo vs Doloso: il legislatore si sforza di calcolare l'intenzione (V) senza una metrica dell'A
    db.aggiungi_lemma(Lemma("Dolo Intenzionale", "D_Diritto", v=0.8, a=0.2, carico_strutturale=8.0))

    # 4. ECONOMIA
    # Homo Oeconomicus (attore razionale base per i mercati): pretesa modellistica altissima, falso nella realtà pratica
    db.aggiungi_lemma(Lemma("Homo Oeconomicus", "D_Economia", v=0.95, a=0.15, carico_strutturale=9.0))


    # Generazione Mappa
    db.draw_mappa()
