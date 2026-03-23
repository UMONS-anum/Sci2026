import numpy as np
import math
from scipy.optimize import brentq

def f_a(x : float,a: float) -> float:
# entrée : x un réel et a un réel
#sortie : la fonction retourne f_a(x)
    return a * np.log(2 * x / (x + 1)) - x / (2 * x + 1)
def racines_f(a: float) -> list[float]:
# entrée : a un réel
# sortie : liste contenant la racine trouvée si il y en a une
    if a <= 0:
        raise ValueError("a doit être un réel strictement positif")
    a0 = (1/ (2*np.log(2)))
    if np.isclose(a, a0, rtol=1e-12, atol=1e-12):
        #on utilise isclose pour être sûr que a et a0 soient suffisament proche 
        return []
    if a > a0:
        borne_gauche = math.nextafter(0, math.inf)
        #on utilise nextafter pour etre suffisament proche de 0 
        borne_droite = 1
        while f_a(borne_gauche,a)* f_a(borne_droite,a)>0:
            borne_droite *= 2 #on ajuste dynaquement jusqu'à changement de signe
        return [brentq(f_a,borne_gauche,borne_droite,args=(a),xtol =1e-12, rtol = 1e-12 )]
    if a < a0: 
        borne_droite = math.nextafter(-1,-math.inf)
        borne_gauche = -2
        while f_a(borne_gauche,a)*f_a(borne_droite,a)>0:
            borne_gauche *= 2 # on ajuste dynamiquement jusqu'à changement de signe
        return [brentq(f_a,borne_gauche, borne_droite,args=(a), xtol = 1e-12, rtol = 1e-12)]
    
for c in [0.5,1,5]:
    print(f"a={c}, racine = {racines_f(c)}")

