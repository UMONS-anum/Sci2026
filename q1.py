import math
import numpy as np
from scipy.optimize import brentq
from math import nextafter


def f(x : float, a : float) -> float:
    """
        Fonction pour calculer l'image de la fonction f
        Entrée: a est un réel et x est un réel
        Sortie: la fonction retourne f(x,a)
        Effet : / 
    """
    return a * np.log(2*x/(x+1)) - x/(2*x+1)


def racines_f(a: float) -> float:
    """
        Fonction pour calculer la racine de la fonction f
        Entrée: a est un réel
        Sortie: la fonction retourne la racine de f
        Effet : /
    """
    a0 = 1/ (2*np.log(2))
    # Utiliser np.isclose pour comparaison fiable des flottants
    # Tolérance: rtol=1e-09 (relative), atol=0.0 (absolue) [par défaut numpy]
    if a > a0 :
        borne_inf = nextafter(0,math.inf) # on prend le réel le plus proche à droite de 0
        borne_sup = 1
        #on cherche une borne supérieure telle que la fonction admet un changement de signe
        while f(borne_inf,a) * f(borne_sup,a) > 0:
            borne_sup *=2
        #recherche de la valeur de la racine avec brentq
        return brentq(f,borne_inf ,borne_sup,args=(a,),xtol=1e-12,rtol=1e-10)
    if np.isclose(a, a0):
        #cas où f_a n'admet pas de racine
        return None
    if a < a0:
        borne_sup = nextafter(-1,-math.inf) #on prend le réel le plus proche à gauche de -1
        borne_inf = -2
        while f(borne_inf,a) * f(borne_sup,a) > 0:
            borne_inf *=2
        return brentq(f,borne_inf,borne_sup,args=(a,),xtol=1e-12,rtol=1e-10)

#impression pour les valeurs demandées dans l'énoncé
print(racines_f(0.5))
print(racines_f(1))
print(racines_f(5))