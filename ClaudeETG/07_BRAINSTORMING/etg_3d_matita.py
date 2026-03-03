"""
ETG — Prototipo 3D: La Matita v2
Correzioni di Carlo applicate:
- Alfa FUORI dal reticolo (prima di x=0)
- Cono tangente ai V_l (irregolare)
- Semirette da alfa oltre V_l (spazio sopra L)
- V_c diversi per ogni piano (nascita in momenti diversi su C)
- A_c coincidenti (piani attualmente esistenti)
- Oltre A_l: L tratteggiata (stabilizzazione potenziale)
- Ma = soglia di causalita (A_l — A_c)
- Altezza geometrica = V_l-V_c (= S, fatta coincidere con DH per 3D statico)
"""

import numpy as np
import plotly.graph_objects as go

# ============================================================
# Configurazione ETG
# ============================================================

ALFA_X = -1.5          # alfa FUORI dal reticolo, prima di x=0
SISTEMA_START = 0.0     # punto zero del sistema (ingresso di C)
A_C_X = 10.0            # A_c coincidente per tutti i piani attuali
L_TRATT_END = 12.0      # fine di L tratteggiata (oltre Ma)

# Piani D: nome, angolo radiale, altezza (S=DH per statico), V_c (nascita su C)
PIANI_D = [
    {"nome": "D_fisica",       "angolo": 0,    "h": 2.8,  "Vc_x": 1.0,  "colore": "rgb(50,100,220)"},
    {"nome": "D_diritto",      "angolo": 45,   "h": 2.2,  "Vc_x": 0.5,  "colore": "rgb(220,150,30)"},
    {"nome": "D_cucina",       "angolo": 90,   "h": 1.5,  "Vc_x": 2.5,  "colore": "rgb(50,200,80)"},
    {"nome": "D_musica",       "angolo": 135,  "h": 2.0,  "Vc_x": 1.8,  "colore": "rgb(180,50,180)"},
    {"nome": "D_medicina",     "angolo": 180,  "h": 2.5,  "Vc_x": 0.8,  "colore": "rgb(220,50,50)"},
    {"nome": "D_architettura", "angolo": 225,  "h": 1.8,  "Vc_x": 3.0,  "colore": "rgb(30,180,180)"},
    {"nome": "D_filosofia",    "angolo": 270,  "h": 2.3,  "Vc_x": 0.3,  "colore": "rgb(150,120,50)"},
    {"nome": "D_sport",        "angolo": 315,  "h": 1.2,  "Vc_x": 4.0,  "colore": "rgb(80,150,220)"},
]

fig = go.Figure()

# ============================================================
# Asse C (la costante) — dal punto zero in poi
# ============================================================
fig.add_trace(go.Scatter3d(
    x=[SISTEMA_START, A_C_X + 2], y=[0, 0], z=[0, 0],
    mode='lines',
    line=dict(color='blue', width=6),
    name='C (costante)',
    hoverinfo='name'
))

# ============================================================
# Alfa — FUORI dal reticolo
# ============================================================
fig.add_trace(go.Scatter3d(
    x=[ALFA_X], y=[0], z=[0],
    mode='markers+text',
    marker=dict(size=12, color='red'),
    text=['α'],
    textposition='top center',
    textfont=dict(size=18, color='red'),
    name='alfa (fuori dal sistema)',
    hoverinfo='name'
))

# Linea tratteggiata alfa -> ingresso sistema
for i in range(8):
    x1 = ALFA_X + i * (SISTEMA_START - ALFA_X) / 8
    x2 = x1 + (SISTEMA_START - ALFA_X) / 16
    fig.add_trace(go.Scatter3d(
        x=[x1, x2], y=[0, 0], z=[0, 0],
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        showlegend=False, hoverinfo='skip'
    ))

# Punto di ingresso in C (alfa_1)
fig.add_trace(go.Scatter3d(
    x=[SISTEMA_START], y=[0], z=[0],
    mode='markers+text',
    marker=dict(size=7, color='darkred'),
    text=['α₁'],
    textposition='bottom center',
    textfont=dict(size=12, color='darkred'),
    name='alfa₁ (ingresso in C)',
    hoverinfo='name'
))

# ============================================================
# Piani D, Cono, Semirette, L tratteggiata
# ============================================================

# Raccogli tutti i V_l per il cono
all_Vl = []

for d in PIANI_D:
    ang = np.radians(d["angolo"])
    h = d["h"]
    dy = np.cos(ang)
    dz = np.sin(ang)
    vc_x = d["Vc_x"]

    # 4 vertici del rettangolo D
    V_c = [vc_x, 0, 0]                         # nascita su C (diversa per piano)
    A_c = [A_C_X, 0, 0]                        # A_c coincidente
    V_l = [vc_x, dy * h, dz * h]               # estremo L sinistro (in alto)
    A_l = [A_C_X, dy * h, dz * h]              # estremo L destro (in alto)

    all_Vl.append(V_l)

    # --- Rettangolo D (superficie) ---
    fig.add_trace(go.Mesh3d(
        x=[V_c[0], A_c[0], A_l[0], V_l[0]],
        y=[V_c[1], A_c[1], A_l[1], V_l[1]],
        z=[V_c[2], A_c[2], A_l[2], V_l[2]],
        i=[0, 0], j=[1, 2], k=[2, 3],
        opacity=0.3,
        color=d["colore"],
        name=d["nome"],
        hoverinfo='name',
        showlegend=True
    ))

    # --- Bordi del rettangolo ---
    # L (V_l — A_l = bordo alto = L) in teal
    fig.add_trace(go.Scatter3d(
        x=[V_l[0], A_l[0]], y=[V_l[1], A_l[1]], z=[V_l[2], A_l[2]],
        mode='lines',
        line=dict(color='teal', width=4),
        name=f'L di {d["nome"]}',
        showlegend=False, hoverinfo='name'
    ))

    # S (V_c — V_l = bordo sinistro = portata) in rosso
    fig.add_trace(go.Scatter3d(
        x=[V_c[0], V_l[0]], y=[V_c[1], V_l[1]], z=[V_c[2], V_l[2]],
        mode='lines',
        line=dict(color='red', width=3),
        showlegend=False, hoverinfo='skip'
    ))

    # Ma (A_l — A_c = bordo destro = soglia causalita) in arancione
    fig.add_trace(go.Scatter3d(
        x=[A_c[0], A_l[0]], y=[A_c[1], A_l[1]], z=[A_c[2], A_l[2]],
        mode='lines',
        line=dict(color='orange', width=3),
        showlegend=False, hoverinfo='skip'
    ))

    # Base (V_c — A_c = proiezione su C)
    fig.add_trace(go.Scatter3d(
        x=[V_c[0], A_c[0]], y=[V_c[1], A_c[1]], z=[V_c[2], A_c[2]],
        mode='lines',
        line=dict(color='gray', width=1),
        showlegend=False, hoverinfo='skip'
    ))

    # --- Semiretta da alfa attraverso V_l e OLTRE (spazio sopra L) ---
    # Direzione: da alfa a V_l, poi continua
    dir_x = V_l[0] - ALFA_X
    dir_y = V_l[1]
    dir_z = V_l[2]
    norm = np.sqrt(dir_x**2 + dir_y**2 + dir_z**2)
    # Estendi la semiretta oltre V_l per 4 unita
    ext = 4.0
    end_x = V_l[0] + (dir_x / norm) * ext
    end_y = V_l[1] + (dir_y / norm) * ext
    end_z = V_l[2] + (dir_z / norm) * ext

    # Segmento alfa -> V_l (pieno)
    fig.add_trace(go.Scatter3d(
        x=[ALFA_X, V_l[0]], y=[0, V_l[1]], z=[0, V_l[2]],
        mode='lines',
        line=dict(color='goldenrod', width=2),
        showlegend=False, hoverinfo='skip'
    ))

    # Segmento V_l -> oltre (tratteggiato = spazio sopra L)
    n_seg = 10
    for i in range(n_seg):
        t1 = i / n_seg
        t2 = (i + 0.5) / n_seg
        x1 = V_l[0] + (end_x - V_l[0]) * t1
        y1 = V_l[1] + (end_y - V_l[1]) * t1
        z1 = V_l[2] + (end_z - V_l[2]) * t1
        x2 = V_l[0] + (end_x - V_l[0]) * t2
        y2 = V_l[1] + (end_y - V_l[1]) * t2
        z2 = V_l[2] + (end_z - V_l[2]) * t2
        fig.add_trace(go.Scatter3d(
            x=[x1, x2], y=[y1, y2], z=[z1, z2],
            mode='lines',
            line=dict(color='goldenrod', width=1),
            showlegend=False, hoverinfo='skip'
        ))

    # --- L tratteggiata (oltre A_l verso destra) ---
    n_tratt = 8
    for i in range(n_tratt):
        x1 = A_l[0] + i * (L_TRATT_END - A_l[0]) / n_tratt
        x2 = x1 + (L_TRATT_END - A_l[0]) / (n_tratt * 2)
        fig.add_trace(go.Scatter3d(
            x=[x1, x2], y=[A_l[1], A_l[1]], z=[A_l[2], A_l[2]],
            mode='lines',
            line=dict(color='teal', width=2),
            showlegend=False, hoverinfo='skip'
        ))

    # --- Etichetta D ---
    mid_x = (vc_x + A_C_X) / 2
    label_dist = h + 0.5
    fig.add_trace(go.Scatter3d(
        x=[mid_x], y=[dy * label_dist], z=[dz * label_dist],
        mode='text',
        text=[d["nome"]],
        textfont=dict(size=11, color='black'),
        showlegend=False, hoverinfo='skip'
    ))

# ============================================================
# Superficie del cono (tangente ai V_l, irregolare)
# ============================================================
# Il cono è l'involucro che collega alfa a tutti i V_l
# Lo rappresentiamo come triangoli alfa -> V_l_i -> V_l_i+1

# Ordina V_l per angolo
vl_sorted = sorted(zip(PIANI_D, all_Vl), key=lambda x: x[0]["angolo"])

for i in range(len(vl_sorted)):
    v1 = vl_sorted[i][1]
    v2 = vl_sorted[(i + 1) % len(vl_sorted)][1]

    fig.add_trace(go.Mesh3d(
        x=[ALFA_X, v1[0], v2[0]],
        y=[0, v1[1], v2[1]],
        z=[0, v1[2], v2[2]],
        i=[0], j=[1], k=[2],
        opacity=0.1,
        color='gold',
        showlegend=(i == 0),
        name='Cono (alfa → V_l)' if i == 0 else '',
        hoverinfo='skip'
    ))

# ============================================================
# CU (punti su C a maggiore transito)
# ============================================================
cu_x = [3.5, 7.0]
fig.add_trace(go.Scatter3d(
    x=cu_x, y=[0, 0], z=[0, 0],
    mode='markers+text',
    marker=dict(size=8, color='orange', symbol='diamond'),
    text=['CU₁', 'CU₂'],
    textposition='bottom center',
    textfont=dict(size=12, color='orange'),
    name='CU (siti interazione)',
    hoverinfo='name+text'
))

# ============================================================
# Annotazione Ma (soglia causalita)
# ============================================================
fig.add_trace(go.Scatter3d(
    x=[A_C_X], y=[0], z=[-0.5],
    mode='text',
    text=['Ma (soglia causalità)'],
    textfont=dict(size=10, color='orange'),
    showlegend=False, hoverinfo='skip'
))

# ============================================================
# Layout
# ============================================================
fig.update_layout(
    title=dict(
        text="ETG — La Matita v2<br>"
             "<sub>α fuori dal sistema | Cono tangente ai V_l | Semirette oltre V_l = spazio sopra L | "
             "V_c diversi (nascita) | L tratteggiata oltre Ma</sub>",
        font=dict(size=16)
    ),
    scene=dict(
        xaxis_title="C (costante) →",
        yaxis_title="",
        zaxis_title="",
        xaxis=dict(backgroundcolor="white", gridcolor="lightgray"),
        yaxis=dict(backgroundcolor="white", gridcolor="lightgray"),
        zaxis=dict(backgroundcolor="white", gridcolor="lightgray"),
        camera=dict(
            eye=dict(x=-1.8, y=1.5, z=1.0),
            center=dict(x=0, y=0, z=0)
        ),
        aspectmode='data'
    ),
    legend=dict(
        x=0.01, y=0.99,
        bgcolor="rgba(255,255,255,0.9)",
        font=dict(size=11)
    ),
    width=1400,
    height=800,
    margin=dict(l=0, r=0, t=80, b=0)
)

# ============================================================
# Salva
# ============================================================
output = r"C:\Users\Utente\Documents\ai\etg\ClaudeETG\07_BRAINSTORMING\ETG_3D_Matita_v2.html"
fig.write_html(output)
print(f"Salvato: {output}")
print("Aprilo nel browser — ruota col mouse, zoom con la rotella.")
