import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================================
# Lecture des fichiers
# ============================================================

traj = np.loadtxt("exemple.trj")

params = {}
with open("robotRPR.par", "r") as f:
    for line in f:
        line = line.strip()
        if not line or "#" not in line:
            continue
        value_part, comment_part = line.split("#", 1)
        value_part = value_part.strip()
        if not value_part:
            continue
        params[comment_part.strip().split()[0]] = float(value_part)

# ============================================================
# Fonctions
# ============================================================

def forward(t1, t2, t3, p):
    x0, y0 = p['x0'], p['y0']

    # L1 : enveloppe fixe
    x1 = x0 + p['L_1'] * np.cos(t1)
    y1 = y0 + p['L_1'] * np.sin(t1)

    # Point d'entrée du coulisseau (glissement dans L1)
    xe = x0 + t2 * np.cos(t1)
    ye = y0 + t2 * np.sin(t1)

    # L2 : bras qui glisse (longueur constante)
    x2 = xe + p['L_2'] * np.cos(t1)
    y2 = ye + p['L_2'] * np.sin(t1)

    # L3 : rotation relative
    theta3 = t1 + t3
    x3 = x2 + p['L_3'] * np.cos(theta3)
    y3 = y2 + p['L_3'] * np.sin(theta3)

    return (x0, y0), (x1, y1), (xe, ye), (x2, y2), (x3, y3)

def dans_les_limites(t1, t2, t3, p):
    """Retourne True si tous les angles sont dans les limites"""
    return (
        p['t1_min'] <= t1 <= p['t1_max'] and
        p['t2_min'] <= t2 <= p['t2_max'] and
        p['t3_min'] <= t3 <= p['t3_max']
    )

def robot_brise(t1, t2, t3, p):
    """Retourne True si le robot est hors limites ou si L2 rentre dans L1"""
    if not dans_les_limites(t1, t2, t3, p):
        return True

    (_, _), (_, _), (_, _), (x2, y2), _ = forward(t1, t2, t3, p)
    d = np.hypot(x2 - p['x0'], y2 - p['y0'])

    # L2 rentre dans L1 → bris
    if d < p['L_1']:
        return True

    return False

# ============================================================
# Figure
# ============================================================

fig, ax = plt.subplots()
ax.set_title("Robot RPR : robotRPR.par\nTrajectoire : exemple.trj")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_xlim(params['xmin'], params['xmax'])
ax.set_ylim(params['ymin'], params['ymax'])
ax.set_aspect('equal')
ax.grid()

# Mur
ax.plot(
    [params['xmur[0]'], params['xmur[1]']],
    [params['ymur[0]'], params['ymur[1]']],
    'ko-', lw=3
)

# Origine
ax.plot(params['x0'], params['y0'], 'ko')

# Lignes du robot
L1_line, = ax.plot([], [], color='purple', lw=10, solid_capstyle='butt')
L2_line, = ax.plot([], [], lw=4, marker='o')
L3_line, = ax.plot([], [], lw=4, marker='o')

# Trajectoire du bout
traj_x, traj_y = [], []
traj_line, = ax.plot([], [], 'r--', lw=2)

# ============================================================
# Animation
# ============================================================

def update(i):
    t1, t2, t3 = traj[i]

    (x0, y0), (x1, y1), (xe, ye), (x2, y2), (x3, y3) = forward(t1, t2, t3, params)

    # Couleur : rouge si hors limites
    color = 'red' if robot_brise(t1, t2, t3, params) else 'blue'

    L1_line.set_data([x0, x1], [y0, y1])
    L2_line.set_data([xe, x2], [ye, y2])
    L3_line.set_data([x2, x3], [y2, y3])

    L2_line.set_color(color)
    L3_line.set_color(color)

    traj_x.append(x3)
    traj_y.append(y3)
    traj_line.set_data(traj_x, traj_y)

    return L1_line, L2_line, L3_line, traj_line

ani = FuncAnimation(
    fig,
    update,
    frames=len(traj),
    interval=params['dt'],
    blit=True
)

plt.show()
