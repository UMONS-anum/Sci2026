import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def main():
    #question b
    def f(t, etat):
        x, y, vx, vy = etat
        # Milieu A
        if x + y <= 1:
            return [vx, vy, -y, x - 1]
        # Milieu B
        else:
            v = np.sqrt(vx**2 + vy**2)
            return [vx, vy, -v * vx, -v * vy - 1]


    def ord2(t,y):
        return y[1]-2


    def distance_s(s):
        sol = solve_ivp(f,[0,15],[-2,-2,s*1,s*2],method ="DOP853",
                        dense_output=True,events=ord2,
                        rtol=1e-13,atol=1e-13, max_step = 0.01)

        # Si le mobile n'atteint pas y = 2 : pas assez de vitesse initiale

        if len(sol.t_events) == 0:
            return -1

        return sol.y_events[0][1][0] - 2


    print("Reponse question b) :",brentq(distance_s, 10, 15, rtol=1e-12, maxiter=500))

    #question f (code non fini)

    def milieu_A(t, etat):
        x,y,vx,vy = etat
        return[-vx,-vy,-y,x-1]

    def abs_dep(t, y):
        return y[0] + 2

    def frontiere(t, y):
        return y[0] + y[1] - 1.001


    def atteindre(x):
        sol = solve_ivp(milieu_A,[0,-10],[x,1-x,-1/np.sqrt(2),1/np.sqrt(2)],
                        method ="DOP853",dense_output=True,
                        events=abs_dep,
                        rtol=1e-13,atol=1e-13, max_step = 0.01)


        if len(sol.t_events) == 0:
            return -1
        else :
            return sol.y_events[0][0][1] + 2


    arrive = brentq(atteindre, 2, 3, rtol=1e-12, maxiter=500)



    sol_final = solve_ivp(milieu_A,[0,10],
                            [arrive,1-arrive,1/np.sqrt(2),-1/np.sqrt(2)],
                            method="DOP853", events=abs_dep)

    print(sol_final.y_events[0][0][2],sol_final.y_events[0][0][3])


if __name__ == "__main__": main()