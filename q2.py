import math
import numpy as np
from scipy.optimize import brentq
from math import nextafter

def f(y: float, a : float) -> float: 
    return 4 + y**2 - (y**(math.pi)/a) + 3 * math.sin(a/y) 
    #fonction de l'enonce avec x fixé (ici a)
def racine(a : float) -> float:
    borne_inf = 1e-40                
    #on prend un très petit réel proche de 0 
    #car nextafter ne fonctionne pas (erreur de domaine)
    borne_sup = 1
    while f(borne_inf,a) * f(borne_sup,a) > 0:
        borne_sup *=2
    return brentq(f,borne_inf,borne_sup,args=(a,),xtol=1e-12,rtol=1e-10)
    #on cherche la racine de f_x, comme elle est unique c'est bien g(x)
print(racine(1e-3))
print(racine(1))
print(racine(5))
print(racine(100))
