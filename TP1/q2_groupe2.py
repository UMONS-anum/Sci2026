import math
from scipy.optimize import brentq

def f_x(y : float, x : float)->float :
    """
    Fournit les valeurs de la fonction f.

    Args:
        y : variable
        x : variable

    Returns:
        l'image de (x, y) par f
    """
    if x<= 0 :
        raise ValueError('Le paramètre x doit être strictement positif')
    return 4 + y**2 - (y**math.pi/x) + 3*math.sin(x/y)

def g(x : float)->float :
    """
    Donne une estimation numérique de g(x) = max{y > 0 | f(x, y) = 0}

    Args:
        x : variable
    
    Returns:
        l'image de x par la fonction g
    """
    borne_g : float = (2*x/math.pi)**(1/(math.pi-2)) # voir rapport
    borne_d : float = 2*borne_g
    while f_x(borne_d, x)>0 :
        borne_d *= 2
    return brentq(f_x, borne_g, borne_d,args=(x), rtol = 1e-15, xtol = 1e-15)


if __name__ == '__main__':
    valeurs_x = [1e-3, 1, 5, 100]
    for x in valeurs_x:
        print(f"x = {x} : {g(x) :.8f}")
