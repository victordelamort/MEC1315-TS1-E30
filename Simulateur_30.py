import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Loader les fichiers de depart dans le programme       
traj = np.loadtxt("exemple.trj")                                                #fichier de trajectoire
x = traj[:, 0]
y = traj[:, 1]
params = {}                                                                     #fichier de configuration

with open("robotRPR.par", "r") as f:                                            #APPEL DES PARAMETRES AVEC CHATGPT
    for line in f:                                                              #appeler les variables avec params['var_name']
        line = line.strip()

        if not line or "#" not in line:
            continue

        value_part, comment_part = line.split("#", 1)

        value_part = value_part.strip()
        if not value_part:
            continue   # <-- évite float("")

        try:
            value = float(value_part)
        except ValueError:
            continue   # au cas où (sécurité)

        var_name = comment_part.strip().split()[0]
        params[var_name] = value

#Figure 
ax = plt.gca()
plt.title('Robot RPR: robotRPR.par\nTrajectoire: exemple.trj')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
ax.set_xlim([params['xmin'], params['xmax']])
ax.set_ylim([params['ymin'], params['ymax']])

#mur noir avec points aux extremites
plt.plot([params['xmur[0]'], params['xmur[1]']], [params['ymur[0]'], params['ymur[1]']], color='k', linewidth=3, marker='o')

#Origine
origine = (params['x0'], params['y0'])

#Segment L_1
x1 = params['x0'] + params['L_1'] * np.cos(params['t1_dep'])
y1 = params['y0'] + params['L_1'] * np.sin(params['t1_dep'])
L_1 = plt.plot([params['x0'], x1], [params['y0'], y1], linewidth=10, color='purple')

#Segment L_2
x2 = x1 + params['L_2'] * np.cos(params['t1_dep'])
y2 = y1 + params['L_2'] * np.sin(params['t1_dep'])
L_2 = plt.plot([x1, x2], [y1,y2], linewidth=2, color='blue', marker='o')

#Segment L_3
x3 = x2 + params['L_3'] * np.cos(params['t3_dep'])
y3 = y2 + params['L_3'] * np.sin(params['t3_dep'])
L_3 = plt.plot([x2, x3], [y2,y3], linewidth=2, color='blue', marker='o')
#Mur
plt.plot([origine], [params['y0']], color='k', marker='o')

plt.grid()
plt.gca().set_aspect('equal')
plt.show()