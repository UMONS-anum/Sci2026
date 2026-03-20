import matplotlib.pyplot as plt
from math import *
import numpy as np
from scipy import optimize


def f(x:float,y:float)->float:
    """
    Entrée: deux floatants x et y .
    Sortie: un floatant calculé à partir de x et y qui retourne 4+y**2-y**(pi)/x +3*sin(x/y), la fonction f donné dans l'énoncé.
    Effet de bord si x=0 ou y=0: lève une exception.
    """
    if x==0 or y==0:
        raise ValueError("x et y doivent être non nuls.")
    return 4+y**2-y**(pi)/x +3*sin(x/y)

def g(x:float)->float:
    """
    Entrée: un floatant x.
    Sortie: l'unique réel y tel que f(x,y)=0.
    Effet de bord si x<=0: lève une excpetion.
    """
    if x<=0:
        raise ValueError("x doit être strictement positif.")
    def h(y):# construis la fonction h à partir de la fonction f pour un x fixé
        return f(x,y)
    a1:float=1
    b1:float=1
    while h(a1)<0:
        a1/=2
    while h(b1)>0:
        b1*=2
    root=optimize.brentq(h,a1,b1,xtol=1e-8)
    return round(root,8)

if __name__ == "__main__":
    print([g(1e-3),g(1),g(5),g(100)])

