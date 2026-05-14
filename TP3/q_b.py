import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
#constante au problème donné:
Tf=20 #choix arbitraire
X0=-2
Y0=-2
#début du code
def systeme(t : float, U : list[float]) -> list[float] :
    '''
    Cette fonction construit le système de l'EDO réduite à l'ordre 1.
    '''
    x, y, vx, vy = U
    v = np.array([vx, vy])
    norme_v = np.linalg.norm(v)

    F = np.array([0.0, -1.0])

    if x + y < 1 :  # Milieu A
        F += np.array([-y, x])
    elif x + y > 1 :           # Milieu B
        F += -norme_v * v  # norme ||v||^2, direction -v/||v||

    return [vx, vy, F[0], F[1]]

def solu(tf : float, x0 : float, y0 : float , vx0 : float, vy0 : float) :
    '''
    Cette fonction résout l'EDO réduite à l'ordre 1 en utilisant les conditions 
    initiales fournies en paramètres (pour la valeur de retour voir la documentation
    de scipy.integrate.solve_ivp).
    '''
    U0 = [x0,y0,vx0,vy0]
    X = np.linspace(0,tf,int(1e3*tf))
    return solve_ivp(systeme, t_span=(0, tf), y0=U0,t_eval=X,dense_output=True)


def distance_min(s : float) -> float :
    '''
    Cette fonction retourne la distance minimale entre le graphe de la solution de l'EDO d'ordre 1
    et le point (2,2).
    '''
    sol = solu(Tf,X0,Y0,s,2*s) 
    def dist_t(t):
        x, y = sol.sol(t)[0], sol.sol(t)[1]
        return np.sqrt((x-2)**2 + (y-2)**2)

    res_t = minimize_scalar(dist_t, bounds=(0, 50), method='bounded')
    return res_t.fun # type: ignore

def minimizes( n = 100) -> float :
    '''
    Cette fonction divise l'intervalle [10,20] en n intervalles de tailles égales et minimise la distance 
    entre le graphe de la solution de l'EDO d'ordre 1 et le point (2,2) sur chaque intervalle tant que cette 
    distance est >= 1e-6. Si une distance < 1e-6 n'est pas trouvée, elle recommence avec n = n+1.
    '''
    a = 10
    b = 20
    i = 0
    while i < n-1 :
        res = minimize_scalar(distance_min, bounds = (a+i*(b-a)/n,a+(i+1)*(b-a)/n), method = "bounded")
        if res.fun < 1e-6 :
            break
        if i == n-2 :
            return minimizes(n+1)
        i += 1
    return res.x
    
def main():
    '''
    Cette fonction affiche la valeur de la distance minimale entre le graphe de la solution de l'EDO et le 
    point (2,2).
    '''
    #Calcul du minimum de distance min
    s=minimizes()
    print(f"Valeur de s qui minimise la distance: {s:.16f}, distance minimale: {distance_min(s):.16f}") # type: ignore
    #résolution du système
    sol = solu(Tf,X0,Y0,s,2*s) # type: ignore
    x, y   = sol.y[0], sol.y[1]
    #création des graphes
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    # Trajectoire + frontière
    axes[0].plot(x, y,color="#CF490B" ,label='trajectoire')
    xlim = axes[0].get_xlim()
    xf = np.linspace(xlim[0], xlim[1], 100)
    yf = 1 - xf
    axes[0].plot(xf, yf, color="#13C0C0", label='frontière x+y=1')
    axes[0].legend(); axes[0].set_title("Trajectoire (x, y)")
    axes[0].grid()
    
    axes[0].axhline(0, color="black", lw=0.7)
    axes[0].axvline(0, color="black", lw=0.7)
    # fonction f
    S = np.linspace(0, 20, 1000)
    vals = [distance_min(k) for k in S]
    axes[1].plot(S, vals)
    axes[1].set_title(r"$\mathrm{distance\_min}(s)$ en fonction de $s$")
    axes[1].set_xlabel("s")
    axes[1].grid()

    axes[1].axhline(0, color="black", lw=0.7)
    axes[1].axvline(0, color="black", lw=0.7)
    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    main()