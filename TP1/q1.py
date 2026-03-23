from math import log, isclose, isnan
from typing import Tuple, List, Optional
from scipy.optimize import brentq

def f(x: float, a: float) -> float:
    """
    Entrée: x un réel strictement positif
    Sortie: la fonction f ou un NaN
    Effet:/
    """
    if x == -1 or x == -0.5:
        return float('nan')
    denom = x + 1
    if denom == 0:
        return float('nan')
    arg = 2 * x / denom
    if arg <= 0:
        return float('nan')
    return a * log(arg) - x / (2 * x + 1)



def h(x: float, a: float) -> float:
    """
    Entrées: un réel x et un réel a 
    Sortie: la fonction h qui est le changement de variable de f
    Effet:/
    """
    return f(x - 1, a)


def partie_valide(a: float, g: float, d: float, n: int = 50) -> bool:
    """
    Entrée: des réels a,g,d et un entier n
    Sortie: retourne vrai ou faux 
    Effet:/
    """
    pas = (d - g) / n
    for i in range(n + 1):
        x = g + i * pas
        y = h(x, a)
        if isnan(y):
            return False
    return True


def trouver_intervalle(a: float,
                       x_min: float,
                       x_max: float,
                       pas: float = 0.1) -> Tuple[float, float]:
    """
    Entrées:réels a,x_min,x_max,pas
    Sortie: un tuple de réel
    Effet:/
    """
    x = x_min
    y_prev = None
    x_prev = None
    while x <= x_max:
        y = h(x, a)
        if not isnan(y):
            if y_prev is not None and y_prev * y < 0:
                g, d = x_prev, x
                if partie_valide(a, g, d):
                    return g, d
            y_prev, x_prev = y, x
        x += pas

    return None


def racines_f(a: float) -> List[float]:
    """
    Entrée:un réel a 
    Sortie:liste des racines de la fonction
    Effet:/ 
    """
    seuil = 1 / (2 * log(2))
    if isclose(a, seuil, rel_tol=1e-12):
        return []

    intervalle = trouver_intervalle(a, x_min=-20.0, x_max=20.0, pas=0.05)
    if intervalle is None:
        return []

    g, d = intervalle
    racine_h = brentq(h, g, d, args=(a,))
    return [racine_h - 1]


print([round(r, 8) for r in racines_f(0.5)])
print([round(r, 8) for r in racines_f(1)])
print([round(r, 8) for r in racines_f(5)])
print([round(r, 8) for r in racines_f(0.6)])
