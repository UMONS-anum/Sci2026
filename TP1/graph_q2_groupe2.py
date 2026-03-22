import math
import matplotlib.pyplot as plt
import numpy as np

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

def graph_s(x : float):
    """
    Trace le graphe de f(x, y) pour une certaine valeur de x fixée.

    Args:
        y : variable
    """
    y = np.linspace(1e-3, 10, 1000)
    s_y = [f_x(c, x) for c in y]
    y_x = ((2*x)/math.pi)**(1/(math.pi - 2))
    
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(y_x, f_x(y_x, x), color='red')
    ax.plot(y, s_y, label = 's(y)', color='blue')
    ax.legend()
    ax.grid(True)
    plt.show()

if __name__=='__main__':
    #graph_s(0.5) # J'ai pris 1000 points entre 1e-3 et 2
    graph_s(10) # J'ai pris 1000 points entre 1e-3 et 10
