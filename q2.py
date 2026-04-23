import math
import numpy as np
from scipy.optimize import brentq

def f(y: float, x : float) -> float: 
    """
        Fonction pour calculer l'image de la fonction f
        Entrée: x est un réel et y est un réel
        Sortie: la fonction retourne f(x,y)
        Effet : / 
    """
    return 4 + y**2 - (y**np.pi)/x + 3*np.sin(x/y)


def racine(x : float) -> float:
    """
        Fonction pour calculer la racine de la fonction f
        Entrée: x est un réel
        Sortie: la fonction retourne la racine de f_x
        Effet : /
    """
    borne_inf = 1e-40                   
    #on prend un très petit réel proche de 0 
    #car nextafter ne fonctionne pas (erreur de domaine)
    borne_sup = 1
    while f(borne_inf,x) * f(borne_sup,x) > 0:
        borne_sup *=2
    return brentq(f,borne_inf,borne_sup,args=(x,),xtol=1e-12,rtol=1e-10)
    #on cherche la racine de f_x, comme elle est unique c'est bien g(x)

for x in [1e-3, 1, 5, 100]: 
    print(f"x={x:.3g}, g(x) ≈ {racine(x)}")