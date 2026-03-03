"""
ETG_P - Prototipo Dinamico: Il Piano Topologico 3D
Evoluzione del modello visivo ETG_3D_Matita_v2, convertito in Plotly.

Questo script:
1. Monta il modello base (Asse C, Cono, Piani D) usando Plotly per garantire
   un HTML solido, cross-platform e visibile ovunque (anche offline).
2. Carica dinamicamente un file JSON contenente lemmi.
3. Posiziona i lemmi sui rispettivi Piani D secondo questa logica:
   - Posizione X (lungo l'asse costante C): proporzionale ad A.
   - Altezza Y (radiale, sul piano D): proporzionale a V.
4. Esporta un file HTML interattivo funzionante al 100%.
"""

import json
import numpy as np
import plotly.graph_objects as go
import os

# ============================================================
# Configurazione Geometria Base ETG
# ============================================================
C_LENGTH = 10.0
ALFA_X = -1.5
SISTEMA_START = 0.0

# Piani D (Dizionario per lookup rapido: Chiave -> Angolo, DH Max (astrazione), Vc_x (nascita), Colore)
PIANI_D = {
    "D_fisica":             {"angolo": 0,   "DH_max": 2.8, "Vc_x": 1.0, "colore": "rgba(51, 102, 229, 0.35)", "colore_bordo": "rgba(51, 102, 229, 1.0)", "nome": "Fisica"},
    "D_diritto":            {"angolo": 45,  "DH_max": 2.2, "Vc_x": 0.5, "colore": "rgba(229, 153, 25, 0.35)", "colore_bordo": "rgba(229, 153, 25, 1.0)", "nome": "Diritto"},
    "D_psicoanalisi":       {"angolo": 90,  "DH_max": 2.5, "Vc_x": 2.5, "colore": "rgba(178, 51, 178, 0.35)", "colore_bordo": "rgba(178, 51, 178, 1.0)", "nome": "Psicoanalisi"},
    "D_biologia_evolutiva": {"angolo": 135, "DH_max": 2.0, "Vc_x": 1.5, "colore": "rgba(51, 204, 76, 0.35)", "colore_bordo": "rgba(51, 204, 76, 1.0)", "nome": "Biologia"},
    "D_economia_classica":  {"angolo": 180, "DH_max": 2.3, "Vc_x": 1.2, "colore": "rgba(76, 153, 229, 0.35)", "colore_bordo": "rgba(76, 153, 229, 1.0)", "nome": "Economia"},
    "D_teologia_dogmatica": {"angolo": 225, "DH_max": 3.8, "Vc_x": 0.2, "colore": "rgba(229, 51, 51, 0.35)", "colore_bordo": "rgba(229, 51, 51, 1.0)", "nome": "Teologia"},
    "D_ingegneria":         {"angolo": 270, "DH_max": 1.8, "Vc_x": 2.0, "colore": "rgba(153, 127, 51, 0.35)", "colore_bordo": "rgba(153, 127, 51, 1.0)", "nome": "Ingegneria"},
    "D_informatica":        {"angolo": 315, "DH_max": 1.5, "Vc_x": 3.0, "colore": "rgba(25, 178, 178, 0.35)", "colore_bordo": "rgba(25, 178, 178, 1.0)", "nome": "Informatica"}
}

# ============================================================
# Funzioni Matematiche per il Posizionamento
# ============================================================
def calcola_coordinate(V, A, angolo_deg, base_x_start, base_x_end=C_LENGTH, altezza_max=3.0):
    x = base_x_start + (A * (base_x_end - base_x_start))
    r = V * altezza_max
    ang_rad = np.radians(angolo_deg)
    y = r * np.cos(ang_rad)
    z = r * np.sin(ang_rad)
    return [x, y, z]

def carica_lemmi(filepath="lemmi_etg.json"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filepath} non trovato. Genero coordinate senza lemmi.")
        return []

# ============================================================
# Core Generation
# ============================================================
def crea_scena(lemmi, output_path="ETG_P_Dinamico.html"):
    fig = go.Figure()

    # --- Asse C ---
    fig.add_trace(go.Scatter3d(
        x=[SISTEMA_START, C_LENGTH], y=[0, 0], z=[0, 0],
        mode='lines',
        line=dict(color='blue', width=6),
        name='C (costante)'
    ))
    
    # Alfa
    fig.add_trace(go.Scatter3d(
        x=[ALFA_X], y=[0], z=[0],
        mode='markers+text',
        marker=dict(size=10, color='red'),
        text=['α'],
        textposition='top center',
        textfont=dict(size=14, color='red'),
        name='alfa (origine)'
    ))

    # --- Raccogliamo i V_l per il cono ---
    all_Vl = []
    
    # --- Piani D ---
    for f_id, d in PIANI_D.items():
        ang_rad = np.radians(d["angolo"])
        dh = d["DH_max"]
        
        x_start = d["Vc_x"]
        x_end = C_LENGTH
        dy = np.cos(ang_rad)
        dz = np.sin(ang_rad)
        
        V_c = [x_start, 0, 0]
        A_c = [x_end, 0, 0]
        V_l = [x_start, dy * dh, dz * dh]
        A_l = [x_end, dy * dh, dz * dh]
        
        all_Vl.append((d, V_l))

        # Disegno del rettangolo (Piano D)
        fig.add_trace(go.Mesh3d(
            x=[V_c[0], A_c[0], A_l[0], V_l[0]],
            y=[V_c[1], A_c[1], A_l[1], V_l[1]],
            z=[V_c[2], A_c[2], A_l[2], V_l[2]],
            i=[0, 0], j=[1, 2], k=[2, 3],
            color=d["colore"].replace(', 0.35', ', 1.0'), # Plotly mesh3d with opacity uses solid color + opacity param
            opacity=0.35,
            name=d["nome"],
            showlegend=True
        ))

        # Bordi esterni del piano
        fig.add_trace(go.Scatter3d(
            x=[V_l[0], A_l[0]], y=[V_l[1], A_l[1]], z=[V_l[2], A_l[2]],
            mode='lines',
            line=dict(color=d["colore_bordo"], width=4),
            showlegend=False, hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter3d(
            x=[V_c[0], V_l[0]], y=[V_c[1], V_l[1]], z=[V_c[2], V_l[2]],
            mode='lines',
            line=dict(color='red', width=2),
            showlegend=False, hoverinfo='skip'
        ))
        
        # Etichetta del piano D
        fig.add_trace(go.Scatter3d(
            x=[(x_start + x_end) / 2], y=[dy * (dh + 0.3)], z=[dz * (dh + 0.3)],
            mode='text',
            text=[d["nome"]],
            textfont=dict(size=12, color=d["colore_bordo"]),
            showlegend=False, hoverinfo='skip'
        ))

    # --- Cono ---
    # Costruiamo il cono collegando alfa (0,0,0) ai punti V_l
    vl_sorted = sorted(all_Vl, key=lambda x: x[0]["angolo"])
    for i in range(len(vl_sorted)):
        v1 = vl_sorted[i][1]
        v2 = vl_sorted[(i + 1) % len(vl_sorted)][1]
        fig.add_trace(go.Mesh3d(
            x=[ALFA_X, v1[0], v2[0]],
            y=[0, v1[1], v2[1]],
            z=[0, v1[2], v2[2]],
            i=[0], j=[1], k=[2],
            color='gold', opacity=0.15,
            showlegend=False, hoverinfo='skip'
        ))

    # --- Lemmi (Dati json) ---
    for lemma in lemmi:
        disciplina_id = lemma.get("disciplina")
        if disciplina_id in PIANI_D:
            piano = PIANI_D[disciplina_id]
            coord = calcola_coordinate(
                V=lemma.get("V", 0), 
                A=lemma.get("A", 0), 
                angolo_deg=piano["angolo"],
                base_x_start=piano["Vc_x"],
                altezza_max=piano["DH_max"]
            )
            
            testo_hover = f"{lemma.get('id')}: {lemma.get('testo')}<br>V={lemma.get('V')} A={lemma.get('A')}"
            
            fig.add_trace(go.Scatter3d(
                x=[coord[0]], y=[coord[1]], z=[coord[2]],
                mode='markers+text',
                marker=dict(size=6, color=piano["colore_bordo"]),
                text=[lemma.get("id")],
                textposition='top center',
                textfont=dict(size=10, color='black'),
                name=lemma.get("id"),
                hovertext=testo_hover,
                hoverinfo='text'
            ))

            # Linea tratteggiata che unisce il lemma all'asse C (proiezione ortogonale su C)
            fig.add_trace(go.Scatter3d(
                x=[coord[0], coord[0]], y=[0, coord[1]], z=[0, coord[2]],
                mode='lines',
                line=dict(color='gray', width=1, dash='dot'),
                showlegend=False, hoverinfo='skip'
            ))

    # --- Layout e Rendering ---
    fig.update_layout(
        title="ETG_P - Topologia 3D Dinamica (Plotly Base)",
        scene=dict(
            xaxis_title="C: x (Astrazione/Attuabilità)",
            yaxis_title="y",
            zaxis_title="z",
            xaxis=dict(backgroundcolor="white", gridcolor="lightgray"),
            yaxis=dict(backgroundcolor="white", gridcolor="lightgray", range=[-4, 4]),
            zaxis=dict(backgroundcolor="white", gridcolor="lightgray", range=[-4, 4]),
            aspectmode='manual',
            aspectratio=dict(x=2, y=1, z=1)
        ),
        margin=dict(l=0, r=0, b=0, t=50),
        legend=dict(x=0, y=1),
        paper_bgcolor='white'
    )

    fig.write_html(output_path)
    print(f"File generato: {output_path}")

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_json = os.path.join(dir_path, "lemmi_etg.json")
    file_html = os.path.join(dir_path, "ETG_P_Dinamico.html")
    
    lemmi_data = carica_lemmi(file_json)
    crea_scena(lemmi_data, file_html)
