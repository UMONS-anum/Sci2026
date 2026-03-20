import math
import scipy.optimize

from math import nextafter

from scipy.optimize import brentq 

from typing import List

import numpy as np  # importe une bibliothèque de calcul

class Enonce (Exception) :
    """
    Exception lancée lorsqu'on ne respecte pas l'énoncé.
    """

    def __init__(self, msg="Veuillez respecter l'énoncé."):
        super().__init__(msg)

    pass

def f(x:float, a:float) -> float :
    """
    Fournit les valeurs de la fonction f_a.

    Args:
        a (float) : le paramètre strictement positif de la fonction
        x (float) : la variable

    Raises:
        Enonce : se déclanche lorsque les données ne correspondent pas à l'énoncé

    Returns:
        (float) : l'image de x par f_a
    """

    if a<=0 :
        raise Enonce("Alpha doit être un réel strictement positif.")

    return a*np.log((2*x)/(x+1)) -(x)/(2*x+1)

def trouver_borne_adaptative(a: float, x_depart: float, chercher_positif: bool) -> float:
    """
    Fonction outil pour trouver une borne valide.
    Elle éloigne x_depart vers l'infini (en le multipliant par 2) jusqu'à ce que 
    la fonction f_a atteigne le signe attendu (celui de son asymptote).
    
    Args:
        a (float): le paramètre de la fonction f_a
        x_depart (float): le point de départ de la recherche (-2.0 ou 1.0)
        chercher_positif (bool): True si on cherche f(x) > 0, False si on cherche f(x) < 0
    """
    borne = x_depart
    if chercher_positif:
        # L'asymptote est > 0, on avance vers +inf tant que la fonction est négative
        while f(borne, a) <= 0:
            borne *= 2.0
    else:
        # L'asymptote est < 0, on recule vers -inf tant que la fonction est positive
        while f(borne, a) >= 0:
            borne *= 2.0
            
    return borne


def racines_f(a: float) -> List[float]:
    """
    Prend 'a' comme seul argument et retourne la liste des racines de f_a.
    """
    point_critique = 1 / (2 * math.log(2))

    # Cas 1 : Aucune racine
    # ATTENTION à l'erreur numérique avec les virgules flottantes donc éviter a == point_critique et utiliser fonction isclose
    if math.isclose(a, point_critique, rel_tol=1e-8) : # rel_tol = r_tol de brentq mais pour math.isclose
        return [math.nan] # ou []

    # Cas 2 : Une racine sur la branche gauche ]-inf, -1[
    elif a < point_critique:
        # On remplace nextafter par une borne manuelle très proche si nextafter cause un Overflow
        borne_droite = nextafter(-1, -math.inf) 
        
        # Appel de notre nouvelle fonction pour trouver la borne gauche
        # On part de -2.0 et on cherche une valeur où f(x) < 0
        borne_gauche = trouver_borne_adaptative(a, x_depart=-2.0, chercher_positif=False) 

        # args=(a,) permet de passer la constante 'a' à la fonction f(x, a).
        return [brentq(f, borne_gauche, borne_droite ,args=(a,), rtol=1e-8)] # rtol dans brentq = "Cherche la racine, et arrête-toi uniquement quand tu es sûr à $10^{-8}$ près que c'est la bonne réponse"

    # Cas 3 : Une racine sur la branche droite ]0, +inf[
    else:
        borne_gauche = nextafter(0, math.inf)
        borne_droite = trouver_borne_adaptative(a, x_depart=1.0, chercher_positif=True)
        return [brentq(f, borne_gauche, borne_droite, args=(a,), rtol=1e-8)] # rtol dans brentq = "Cherche la racine, et arrête-toi uniquement quand tu es sûr à $10^{-8}$ près que c'est la bonne réponse"


if __name__ == "__main__":
    valeurs_a = [1 / (2 * math.log(2)),0.5,1,5]
    for a in valeurs_a:
        print([float(f"{racines_f(a)[0]:.8f}")]) 

