"""
ETG — Prototipo 3D: La Matita
Sistema dinamico con piani D radiali attorno all'asse C

Geometria:
- Asse orizzontale (X) = C (la costante)
- A sinistra: alfa (origine)
- Da alfa: cono (gamma/lambda)
- Piani D = rettangoli radiali attorno a C, come lame di un ventilatore
- Ogni D ha DH diverso (altezza del rettangolo)
- L = segmento alto del rettangolo (V_l — A_l), parallelo a C quando efficiente

Esportazione: file HTML interattivo (si ruota col mouse, no software extra)
"""

import numpy as np
import pyvista as pv

# ============================================================
# Configurazione ETG
# ============================================================

# Asse C: da x=0 (alfa) a x=10
C_LENGTH = 10.0

# Piani D: nome, angolo radiale, DH (altezza), colore
# I piani sono radiali attorno all'asse C (asse X)
PIANI_D = [
    {"nome": "D_fisica",      "angolo": 0,    "DH": 2.8,  "colore": [0.2, 0.4, 0.9, 0.35]},
    {"nome": "D_diritto",     "angolo": 45,   "DH": 2.2,  "colore": [0.9, 0.6, 0.1, 0.35]},
    {"nome": "D_cucina",      "angolo": 90,   "DH": 1.5,  "colore": [0.2, 0.8, 0.3, 0.35]},
    {"nome": "D_musica",      "angolo": 135,  "DH": 2.0,  "colore": [0.7, 0.2, 0.7, 0.35]},
    {"nome": "D_medicina",    "angolo": 180,  "DH": 2.5,  "colore": [0.9, 0.2, 0.2, 0.35]},
    {"nome": "D_architettura","angolo": 225,  "DH": 1.8,  "colore": [0.1, 0.7, 0.7, 0.35]},
    {"nome": "D_filosofia",   "angolo": 270,  "DH": 2.3,  "colore": [0.6, 0.5, 0.2, 0.35]},
    {"nome": "D_sport",       "angolo": 315,  "DH": 1.2,  "colore": [0.3, 0.6, 0.9, 0.35]},
]

# Cono alfa: dalla punta (x=0) al corpo della matita (x=2)
CONO_LENGTH = 2.0
CONO_RADIUS_MAX = 0.3  # dove il cono incontra il corpo

# ============================================================
# Costruzione scena
# ============================================================

plotter = pv.Plotter(off_screen=True, window_size=[1600, 900])
plotter.set_background("white")

# --- Asse C (la costante) ---
c_line = pv.Line([0, 0, 0], [C_LENGTH, 0, 0])
plotter.add_mesh(c_line, color="blue", line_width=4, label="C (costante)")

# Punto alfa
alfa_sphere = pv.Sphere(radius=0.15, center=[0, 0, 0])
plotter.add_mesh(alfa_sphere, color="red", label="alfa (origine)")

# Etichetta alfa
plotter.add_point_labels(
    np.array([[0, 0, 0.4]]),
    ["α (alfa)"],
    font_size=16, text_color="red", font_family="arial",
    shape=None, always_visible=True
)

# --- Cono gamma/lambda ---
cono = pv.Cone(
    center=[CONO_LENGTH/2, 0, 0],
    direction=[1, 0, 0],
    height=CONO_LENGTH,
    radius=CONO_RADIUS_MAX,
    resolution=60
)
plotter.add_mesh(cono, color="gold", opacity=0.25, label="cono (gamma/lambda)")

# --- Piani D come rettangoli radiali ---
for d in PIANI_D:
    ang_rad = np.radians(d["angolo"])
    dh = d["DH"]

    # Il piano D è un rettangolo:
    # - lungo l'asse X da x=CONO_LENGTH a x=C_LENGTH (sul corpo della matita)
    # - alto DH nella direzione radiale dal centro (asse C)
    # - spessore zero (è un piano)

    x_start = CONO_LENGTH
    x_end = C_LENGTH

    # Direzione radiale (Y-Z plane)
    dy = np.cos(ang_rad)
    dz = np.sin(ang_rad)

    # 4 vertici del rettangolo D
    # V_c (basso-sinistra, su C) e A_c (basso-destra, su C) = base su C
    # V_l (alto-sinistra) e A_l (alto-destra) = estremi di L
    V_c = [x_start, 0, 0]  # su C
    A_c = [x_end, 0, 0]    # su C
    V_l = [x_start, dy * dh, dz * dh]  # estremo L sinistro
    A_l = [x_end, dy * dh, dz * dh]    # estremo L destro

    # Creare il rettangolo come mesh
    points = np.array([V_c, A_c, A_l, V_l])
    faces = np.array([4, 0, 1, 2, 3])  # un quadrilatero
    rect = pv.PolyData(points, faces=faces)

    rgba = [int(c * 255) for c in d["colore"][:3]]
    plotter.add_mesh(rect, color=rgba, opacity=d["colore"][3],
                     show_edges=True, edge_color="gray", line_width=1)

    # Linea L (bordo alto = V_l — A_l) in evidenza
    l_line = pv.Line(V_l, A_l)
    plotter.add_mesh(l_line, color=rgba, line_width=3)

    # Linea S (bordo sinistro = V_l — V_c = portata)
    s_line = pv.Line(V_c, V_l)
    plotter.add_mesh(s_line, color="red", line_width=2)

    # Etichetta del piano D
    label_pos = np.array([[(x_start + x_end)/2, dy * (dh + 0.3), dz * (dh + 0.3)]])
    plotter.add_point_labels(
        label_pos,
        [d["nome"]],
        font_size=12, text_color=rgba, font_family="arial",
        shape=None, always_visible=True
    )

# --- CU: punti su C a maggiore transito ---
# Mettiamo 2 punti CU come sfere leggermente più grandi sull'asse
cu_positions = [4.0, 7.5]
for cu_x in cu_positions:
    cu_sphere = pv.Sphere(radius=0.12, center=[cu_x, 0, 0])
    plotter.add_mesh(cu_sphere, color="orange")

plotter.add_point_labels(
    np.array([[4.0, 0, -0.4], [7.5, 0, -0.4]]),
    ["CU₁", "CU₂"],
    font_size=14, text_color="orange", font_family="arial",
    shape=None, always_visible=True
)

# --- Legenda testuale ---
plotter.add_text(
    "ETG - La Matita\n"
    "Asse = C (costante) | Rosso sx = alfa | Giallo = cono gamma/lambda\n"
    "Lame colorate = piani D radiali | Altezza = DH | Bordo alto = L\n"
    "Bordo sinistro rosso = S (portata) | Punti arancioni = CU",
    position="lower_left", font_size=10, color="gray"
)

# --- Camera ---
plotter.camera_position = [
    (12, 8, 6),   # posizione camera
    (5, 0, 0),    # punto di mira (centro della matita)
    (0, 0, 1)     # vettore "su"
]

# --- Esporta come HTML interattivo ---
output_html = r"C:\Users\Utente\Documents\ai\etg\ClaudeETG\07_BRAINSTORMING\ETG_3D_Matita.html"
plotter.export_html(output_html)
print(f"Salvato: {output_html}")
print("Aprilo nel browser — puoi ruotare, zoomare, esplorare.")

# --- Esporta anche screenshot PNG ---
output_png = r"C:\Users\Utente\Documents\ai\etg\ClaudeETG\07_BRAINSTORMING\ETG_3D_Matita.png"
plotter.screenshot(output_png)
print(f"Screenshot: {output_png}")

plotter.close()
