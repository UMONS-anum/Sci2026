from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import numpy as np
import matplotlib.pyplot as plt

def FunA(t:float, Z:tuple[float,float,float,float])->tuple[float]:
    """La fonction F pour l'équation différentielle dans l'ensemble A.
        Entrée : un flottant t, un 4-uple de flottants Z
            où Z contient : x, la composante en x de la vitesse, y, la composante en y de la vitesse."""
    x, vx, y, vy = Z
    return vx, -y, vy, x-1

def FunB(t:float, Z:tuple[float,float,float,float])->tuple[float]:
    """La fonction F pour l'équation différentielle dans l'ensemble B.
        Entrée : un flottant t, un 4-uple de flottants Z
            où Z contient : x, la composante en x de la vitesse, y, la composante en y de la vitesse."""
    x, vx, y, vy = Z
    return vx, -vx*np.sqrt(vx**2+vy**2), vy, -vy*np.sqrt(vx**2+vy**2)-1

def Fun(t:float, Z:tuple[float,float,float,float])->tuple[float]:
    """La fonction F générale pour l'équation différentielle.
        Entrée : un flottant t, un 4-uple de flottants Z
            où Z contient : x, la composante en x de la vitesse, y, la composante en y de la vitesse."""
    x, vx, y, vy = Z
    if x+y < 1:
        return FunA(t,Z)
    if x+y > 1:
        return FunB(t,Z)
    
def event1(t:float, Z:tuple[float,float,float,float])->float:
    """Évènement correspondant à x(t) = 2.
        Entrée : un flottant t, un 4-uple de flottants Z
            où Z contient : x, la composante en x de la vitesse, y, la composante en y de la vitesse.
        Sortie : la différence entre x(t) et 2 """
    return Z[0]-2

def event2(t:float, Z:tuple[float,float,float,float])->float:
    """Évènement correspondant à y(t) = 2.
        Entrée : un flottant t, un 4-uple de flottants Z
            où Z contient : x, la composante en x de la vitesse, y, la composante en y de la vitesse.
        Sortie : la différence entre y(t) et 2 """
    event2.terminal = 2
    return Z[2]-2

def E(s:float):
    """ Entrée : un flottant s.
        Sortie : la différence entre x(t) et 2 pour le deuxième t tel que y(t) = 2, 
                où (x,y) est la solution du problème de Cauchy avec les conditions initiales 
                données dans l'énoncé, en fonction de s."""
    SOL = solve_ivp(Fun, (0,10), (-2,s,-2,2*s), max_step=0.05, events=event2, dense_output=True)
    t = SOL.t_events[0][1]
    return event1(t,SOL.sol(t))

def trouver_s(a:float,b:float):
    """ Entrée : deux flottants a et b tels que E(a) et E(b) sont de signes opposés.
        Sortie : Une valeur du flottant s entre a et b telle que E(s) = 0."""
    return brentq(E,a,b)

if __name__ == "__main__":
    print(round(trouver_s(10,18.89795918367347),8))

#################################################

def Graph(a:float,b:float):
    """ Entrée : deux flottants a et b.
        Graphe des solutions (x,y) du problème de Cauchy avec les conditions initiales
        données dans l'énoncé, respectivement avec s = a et s = b."""
    fig, graf = plt.subplots() 
    L = np.linspace(-2,3.5,200)
    M = np.linspace(3,-2.5,200)
    graf.plot(L,M,label="Interface")
    graf.plot([2], [2], marker = 'o', label="Point (2,2)")

    a_SOL = solve_ivp(Fun, (0,10), (-2,a,-2,2*a), max_step=0.05)
    b_SOL = solve_ivp(Fun, (0,10), (-2,b,-2,2*b), max_step=0.05)

    graf.plot(a_SOL.y[0], a_SOL.y[2], label="s = "+str(a))
    graf.plot(b_SOL.y[0], b_SOL.y[2], label="s = "+str(b))

    graf.legend()
    plt.show()

if __name__ == "__main__":
    Graph(10,18.89795918367347)