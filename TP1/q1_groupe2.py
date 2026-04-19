import scipy.optimize as opt
from math import log
from math import isclose 

def f(x : float, a : float)->float :
    """
    Entrée : paramètre a et inconnue x
    Sortie : valeur de f_a évaluée en x
    Effet : /
    """
    return a*log((2*x)/(x+1))-x/(2*x+1)

def g(y : float, a : float)->float :
    """
    Entrée : paramètre a et inconnue y 
    Sortie : valeur de g_a (équivalente à la fonction f(a,y)) évaluée en y=x+1
    Effet : /
    """
    return a*log((2*y-2)/y)-(y-1)/(2*y-1)



def racines_f(a : float)->float :
    """
    Entrée : paramètre a 
    Sortie : racine de f_a avec une précision de 8 décimales
    Effet : /
    """
    if isclose(a,1/(2*log(2))) :
        return []
    elif a<1/(2*log(2)) :
        l : float = -1
        g_l : float = g(l,a)
        while g_l>0 :
            l *= 2
            g_l = g(l,a)
        r : float = -1/8
        g_r : float = g(r,a)
        while g_r<0 :
            r *= 1/2
            g_r = g(r,a)
        root : float = opt.brentq(g,l,r,args=(a),xtol=1e-8) - 1
        return [root]
    else :
        l : float = 1/2 
        f_l : float = f(l,a)
        while f_l>0 :
            l *= 1/2
            f_l = f(l,a)
        r : float = 2
        f_r : float = f(r,a)
        while f_r<0 :
            r *= 2
            f_r = f(r,a)
        root : float = opt.brentq(f,l,r,args=(a),xtol=1e-8)
        return [root]
    

if __name__=='__main__':
    valeurs_a = [0.5, 1, 5]
    for a in valeurs_a:
        print(f"a = {a} : {racines_f(a)[0] :.8f}")