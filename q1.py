import csv
import matplotlib.pyplot as plt

x : list[float] = []
y : list[float] = []
x_avg : list[int] = []
y_avg : list[float] = []

def create_listes() :
    # Entrée : /
    # Sortie : /
    # Effet 1 : crée les listes x et y respectivement années de floraison et jours de floraison
    # lorsque un jour j est encodé dans le fichier 'cherry_blossoms' à l'année correspondante.
    # Effet 2 : crée les lites x_avg et y_avg sur base de x et y pour la moyenne glissante
    # sur 50 ans.
    with open('cherry_blossoms.csv', newline = '') as csvfile :
        reader = csv.reader(csvfile, delimiter = ";")
        for line in reader :
            if line[0] == 'year' :
                pass
            else :
                if line[1] != 'NA' :
                    x.append(int(line[0]))
                    y.append(int(line[1]))
        i = 0
        while i < len(x):
            j = 1
            count = 1
            somme = y[i]
            while j < 50 and j < len(x)-i :
                if x[i+j]-x[i] < 50 :
                    count += 1
                    somme += y[i+j]
                j += 1
            if count >= 5 :
                x_avg.append(x[i])
                y_avg.append(somme/count)
            i += 1
    
def resolution_q1() :
    # Entrée : /
    # Sortie : /
    # Effet : affiche le graphique de la q1
    create_listes()
    plt.plot(x,y,'ro',color='#D25C72',markersize=2, label='Date de floraison enregistrée')
    plt.plot(x_avg,y_avg,'k',label='Moyenne glissante sur 50 ans')
    plt.title("Date de pleine floraison des cerisiers japonais à Kyoto")
    plt.xticks([812,1000,1200,1400,1600,1800,2020])
    plt.yticks([80,90,100,110,120],['21 mars','31 mars','10 avril', '20 avril','30 avril'])
    plt.xlabel('Années de floraison')
    plt.ylabel('Jours de floraison')
    plt.legend()
    plt.show()
