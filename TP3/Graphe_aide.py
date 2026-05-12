import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

def f(t, etat):
    x, y, vx, vy = etat
    v = np.sqrt(vx**2 + vy**2)
    # Milieu A
    if x + y <= 1:
        return [vx, vy, -y, x - 1]
    # Milieu B
    else:
        return [vx, vy, -v * vx, -v * vy - 1]

# --- Configuration du graphique ---
plt.figure(figsize=(8, 8))
x_range = np.linspace(-50, 50, 1000)
plt.plot(x_range, 1 - x_range, 'k--', lw=2, alpha=0.7)


for i in [13.58732146,[7.071610722528396, 2.200331024782522]]:
    x0, y0 = -2,-2
    if isinstance(i,float) or isinstance(i,int) :
        sol = solve_ivp(f, [0, 15], [x0, y0, i, 2*i], method='DOP853', rtol=1e-13, atol=1e-13, max_step=0.01)
    else :
        sol = solve_ivp(f, [0, 15], [x0, y0, i[0], i[1]], method='DOP853', rtol=1e-13, atol=1e-13, max_step=0.01)

    # Tracer la trajectoire
    line, = plt.plot(sol.y[0], sol.y[1], lw=1.5, alpha=0.8)
    # Marquer le point de départ
    plt.scatter(x0, y0, color=line.get_color(), s=30, edgecolors='black', zorder=5, label="Vitesse :" + str(i))

# --- Mise en forme ---
plt.scatter(2,2,marker=".",color="black")
plt.title("Trajectoires d'un mobile depuis (-2,-2)", fontsize=14)
plt.xlabel("x")
plt.ylabel("y")
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.legend(loc='upper right')
plt.grid(True, linestyle=':', alpha=0.6)
plt.axis('equal')
plt.xlim(-8,8)
plt.ylim(-8,8)
plt.show()