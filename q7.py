import csv
import scipy.linalg as lins
import numpy as np
import matplotlib.pyplot as plt


x : list[float] = []
y : list[float] = []

def create_listes() :
    # Entrée : /
    # Sortie : /
    # Effet : si ce n'est pas déjà fait, crée les listes x et y respectivement années de floraison et jours de floraison
    # lorsque un jour j est encodé dans le fichier 'cherry_blossoms' à l'année correspondante.
    if len(x)==0 or len(y)==0 :
        with open('cherry_blossoms.csv', newline = '') as csvfile :
            reader = csv.reader(csvfile, delimiter = ";")
            for line in reader :
                if line[0] == 'year' :
                    pass
                else :
                    if line[1] != 'NA' :
                        x.append(int(line[0]))
                        y.append(int(line[1]))


def create_bornes() -> list[int] :
    # Entrée : /
    # Sortie : liste bornes contenant les bornes utilisées pour la q7
    # Effet : /
    bornes : list[int] = [812]
    borne = 850
    while borne <= 2000 :
        bornes.append(borne)
        borne += 50
    bornes.append(2015)
    return bornes


def create_matrice(x : float, bornes : list[int]) -> list[list[float]] :
    # Entrée : liste x (années de floraison) et liste bornes 
    # Sortie : matrice M utilisée pour résoudre la q7 (explications rapport q3)
    # Effet : /
    matrice : list[list[float]] = [[0 for _ in range (len(bornes))] for _ in range (len(x))]
    last_borne = 1
    ligne = 0 
    for abscisse in x :
        j = last_borne
        while abscisse > bornes[j]:
            j += 1
        matrice[ligne][j-1] = 1-(abscisse-bornes[j-1])/(bornes[j]-bornes[j-1])
        matrice[ligne][j] = (abscisse-bornes[j-1])/(bornes[j]-bornes[j-1])
        ligne += 1
        last_borne = j-1
    return matrice

        


def resolution_sci(m : list[list[float]], y : list[list[float]]) -> list[list[float]] :
    # Entrée : matrices m et y
    # Sortie : matrice contenant les images des bornes de la q7 générées par scipy
    # Effet : /
    return lins.lstsq(m,y)  

def resolution_np(m : list[list[float]], y : list[list[float]]) -> list[list[float]] : 
    # Entrée : matrices m et y
    # Sortie : matrice contenant les images des bornes de la q7 générées par numpy
    # Effet : /
    return np.linalg.solve(np.array(m),np.array(y)) 


def afficher_q7() :
    # Entrée : /
    # Sortie : /
    # Effet : affiche le nuage de points de la q1 ainsi que la résolution de la q7
    # avec les résolutions de scipy ou numpy superposées selon le package choisi par l'utilisateur
    pack = input('Veuillez entrer le package Python à utiliser parmi : \'numpy\' et \'scipy\'\n')
    create_listes()
    bornes = create_bornes()
    matrice = create_matrice(x,bornes)
    if pack == 'numpy' :
        tmp = np.array(matrice)
        matrice_t = tmp.transpose() 
        x_t = np.dot(matrice_t,matrice) # multiplie matrice par sa transposée matrice_t
        y_tmp= [[jour] for jour in y] # instancie y sous forme de matrice
        y_t = np.dot(matrice_t,y_tmp)
        plt.plot(x,y,'ro',color='#D25C72',markersize=2, label='Date de floraison enregistrée')
        plt.plot(bornes,resolution_np(x_t,y_t),color='#98FB98', label = "Approximation par la méthode des moindres carrés par morceaux (numpy)")
        plt.title("Date de pleine floraison des cerisiers japonais à Kyoto")
        plt.xticks([812,1000,1200,1400,1600,1800,2020])
        plt.yticks([80,90,100,110,120],['21 mars','31 mars','10 avril', '20 avril','30 avril'])
        plt.xlabel('Années de floraison')
        plt.ylabel('Jours de floraison')
        plt.legend()
        plt.show()
    elif pack == 'scipy' :
        plt.plot(x,y,'ro',color='#D25C72',markersize=2, label='Date de floraison enregistrée')
        plt.plot(bornes,resolution_sci(matrice,y)[0],label="Approximation par la méthode des moindres carrés par morceaux (scipy)")
        plt.title("Date de pleine floraison des cerisiers japonais à Kyoto")
        plt.xticks([812,1000,1200,1400,1600,1800,2020])
        plt.yticks([80,90,100,110,120],['21 mars','31 mars','10 avril', '20 avril','30 avril'])
        plt.xlabel('Années de floraison')
        plt.ylabel('Jours de floraison')
        plt.legend()
        plt.show()
    else :
        print('Veuillez entrer un package valide')
        afficher_q7()

