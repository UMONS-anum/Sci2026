from scipy.integrate import solve_ivp
from math import *

def ode(t:float, X:list): #Transforme notre EDO en EDO d'ordre 1.
    x, y, u, v = X
    speed = sqrt(u**2 + v**2)
    
    if x + y < 1: #Milieu A
        du = -y
        dv = x-1
    
    elif x + y > 1: #Milieu B
        du = -u * speed
        dv = -1 - v * speed
    
    return [u,v,du,dv]

def event_x_equals_2(t, X): #Servira à arrêter l'intégration lorsque x=2.
    x = X[0]
    return x-2

event_x_equals_2.terminal = True
event_x_equals_2.direction = 1 #On veut que l'event se déclenche quand x=2.

def sol(s):
    """Résoud l'EDO en fonction de s """
    X0 = [-2, -2, s, 2*s]
    solution = solve_ivp(ode, t_span=(0,100), y0=X0, events=event_x_equals_2, max_step=0.01)

    if len(solution.t_events[0]) == 0: #La trajectoire n'atteint jamais x=2.
        return None
    
    y_at_crossing = solution.y[1,-1] 
    """[1,-1] permet de prendre la 2ème coordonnée de la solution (càd y) 
    et l'évalue au dernier instant mesuré (càd celui ou x=2)"""

    return y_at_crossing - 2

def find_s():
    """Pour s<0, la vitesse initiale est dirigée vers le bas et la gauche, 
    ce qui éloigne le mobile du point cible (2,2).
    De plus, les simulations numériques montrent que la trajectoire n’atteint jamais x=2
    ou bien que la coordonnée y reste strictement inférieure à 2 lorsque x=2.
    On peut donc restreindre la recherche à s>0.
    On effectue donc une bissection pour les s positifs."""
    s_min = 0.1
    s_max = 5.0

    # On élargit l'intervalle jusqu'à trouver un changement de signe
    while sol(s_min) is None or sol(s_min) > 1e-9:
        s_min /= 2

    while sol(s_max) is None or sol(s_max) < - 1e-9:
        s_max *= 2

    # Dichotomie
    for _ in range(50):  #50 itérations
        s_mid = 0.5 * (s_min + s_max)
        val = sol(s_mid)

        if val is None:
            s_min = s_mid
        elif val > 0:
            s_max = s_mid
        else:
            s_min = s_mid

    return 0.5 * (s_min + s_max)

print(find_s())