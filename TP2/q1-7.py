import matplotlib.pyplot as plt
import scipy.linalg
import numpy as np
import csv

# Lecture du fichier CSV
with open('cherry_blossoms.csv', newline = '') as csvfile:
    lecteur = csv.DictReader(csvfile, delimiter = ';')
    fig, graf = plt.subplots() 
    x = []
    y = []
    for line in lecteur:
        x.append(int(line['year']))
        if line['doy'] == "NA":
            y.append(None)
        else:
            y.append(int(line['doy']))

# Affichage des données 
graf.plot(x,y,color='#D25C72', marker = 'o', markersize =1, linestyle = 'none',
          label = 'Date de floraison enregistée')
graf.margins(y=.3)
plt.xticks([812, 1000,1200,1400,1600,1800,2020])
plt.yticks([80, 90, 100, 110, 120],['21 mars', '31 mars', '10 avril', '20 avril', '30 avril'])

# Calcul de la moyenne glissante sur 50 ans 
xmoy = []
ymoy = []
for j in range(len(y)):
    if y[j] is not None:
        liste = []
        for k in range(j+1,j+50):
            if k < len(y):
                if y[k] != None:
                    liste.append(y[k])
        if len(liste) >= 4:
            moy = y[j]
            for data in liste:
                moy += data
            moy = moy /(len(liste)+1)
            xmoy.append(x[j])
            ymoy.append(moy)
graf.plot(xmoy,ymoy,color='black',linewidth=.8,label = 'Moyenne glissante sur 50 ans')
graf.legend()
plt.show()

def gbase(i:int,a:int,X:list[float])-> float:
    """
    Entrée: i un indice entre 0 et N
            a un point d'évaluation
            X une liste des x_0, ...,x_N de taille N+1

    Sortie: Valeur réelle de la fonction en a
    """
    N = len(X)-1
    if i == 0:
        if X[0] <= a and a <= X[1]:
            return (1-(a-X[0])/(X[1]-X[0]))
        else:
            return 0
    if i == N:
        if X[N-1] <= a and a <= X[N]:
            return ((a-X[N-1])/(X[N]-X[N-1]))
        else:
            return 0
    if X[i-1] <= a and a <= X[i]:
            return ((a-X[i-1])/(X[i]-X[i-1]))

    if X[i] <= a and a <= X[i+1]:
            return (1-(a-X[i])/(X[i+1]-X[i]))

    return 0
    
        
def matriceM(X:list[float],A:list[int])->list[list[float]]:
    """
    Cette fonction construit la matrice M
    Entrée: X une liste des x_0, ...,x_N de taille N+1
            A abscisses des points de données
    Sortie: M une liste de listes 
    """
    K = len(A)
    N = len(X)-1
    M = []
    for k in range(K):
        L = []
        for i in range(N+1):
            L.append(gbase(i,A[k],X))
        M.append(L)
    return M



def solution()-> tuple[np.ndarray, np.ndarray]:
    """
    Calcule une approximation par la méthode des moindres carrés des
    données de floraison dans la base calculée dans la fonction du dessus.
    On cherche un vecteur sol qui réalise le minimum du carré de la norme de
    (M•sol-D) au sens des moindres carrés,
    où M est la matrice obtenue au dessus et D le vecteur des dates.
    Sortie : coefficients obtenus par les fonctions np.linalg.solve
    et scipy.linalg.lstsq.
    """
    X = [812,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450
         ,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000,2015]
    A = []
    D = []
    for k in range(len(x)):
        if y[k] is not None:
            A.append(x[k])
            D.append(y[k])
    
    M = matriceM(X,A)
    Mt = np.array(np.transpose(M))
    M = np.array(M)
    D = np.array(D)
    At = Mt @ M
    Dt = Mt @ D
    sol1 = np.linalg.solve(At,Dt)
    sol2 = scipy.linalg.lstsq(M,D)[0]
    return sol1,sol2

print(solution())


