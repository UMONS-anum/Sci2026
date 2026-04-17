import math
from scipy.optimize import brentq

def f(x: float, y: float) -> float:
# entrée : x et y des réels
# sortie : la valeur de f(x,y)   
    return 4 + y**2 - (y**math.pi)/x + 3 * math.sin(x / y)
def g(x: float) -> float:
# entrée : x un réel
# sortie : max {y>0 | f(x,y)=0}
    if x <= 0:
        raise ValueError("x must be > 0")
    y0 = 1e-64
    # borne supérieure initiale (heuristique)
    y1 = x ** (1 / (math.pi - 2)) + 7
    # on agrandit y1 pour une plus grande sécurité
    while f(x, y1) > 0:
        y1 *= 2
    root = brentq(lambda y: f(x, y), y0, y1)
    return root

if __name__ == "__main__":
    test_values = [1e-3, 1.0, 5.0, 100.0]
    for x in test_values:
        val = g(x)
        print(f"x = {x} -> g(x) = {val:.8f}")