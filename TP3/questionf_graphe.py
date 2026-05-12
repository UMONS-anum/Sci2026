import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

def f(t, etat):
    x,y,vx,vy = etat
    return[-vx,-vy,-y,x-1]

def frontiere(t, y):
    return y[0] + y[1] - 1.001
def abs2(t, y):
    return y[0] + 2

frontiere.terminal = True


# --- Configuration du graphique ---
plt.figure(figsize=(8, 8))
x_range = np.linspace(-50, 50, 1000)
plt.plot(x_range, 1 - x_range, 'k--', lw=2, alpha=0.7)


for i in [2,3,2.8307886339423742]:
    x0, y0 = -2,-2
    sol = solve_ivp(f, [0, -10], [i,1-i,-1/np.sqrt(2),1/np.sqrt(2)], events=[frontiere,abs2], method='DOP853', rtol=1e-13, atol=1e-13, max_step=0.01)
    print(sol.t_events)
    # Tracer la trajectoire
    line, = plt.plot(sol.y[0], sol.y[1], lw=1.5, alpha=0.8)
    # Marquer le point de départ
    plt.scatter(x0, y0, color=line.get_color(), s=30, edgecolors='black', zorder=5, label="Départ : (" + str(i)+"," + str(1-i) +")")

# --- Mise en forme ---
plt.scatter(2,2,marker=".",color="black")
plt.title("Trajectoire de mobile arrivant tangentiellement à la frontière", fontsize=14)
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