import numpy as np
from scipy.optimize import brentq

def f(y: float, x: float) -> float:
    """
    Entrées: une variable réelle y et un paramètre réel x
    Sortie: valeur de la fonction
    Effet:/
    """
    return 4 + y**2 - (y**np.pi / x) + 3 * np.sin(x / y)

def h(y: float, x: float) -> float:
    """
    Entrées: une variable réelle y et un paramètre réel x
    Sortie: valeur de la fonction
    Effet:/ 
    """
    return y**2 - (y**np.pi / x) + 1

def fct_g(y: float, x: float) -> float:
    """
    Entrées: une variable réelle y et un paramètre réel x
    Sortie: valeur de la fonction
    Effet:/
    """
    return y**2 - (y**np.pi / x) + 7


def g(x: float) -> float:
    """ 
    Entrée: une variable réélle x strictement positive
    Sortie: une approximation numérique de g
    Effet:/
    """
    y_max = (2 * x / np.pi) ** (1 / (np.pi - 2))
    C = 2 * y_max
    while fct_g(C,x) > 0:
        C *= 2
    z = brentq(fct_g, y_max, C, args=(x))
    t = brentq(h, y_max, z, args=(x))
    return brentq(f, t, z,args=(x))


print(round(g(1e-3), 8))
print(round(g(1), 8))
print(round(g(5), 8))
print(round(g(100), 8))
