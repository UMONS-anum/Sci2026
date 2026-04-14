import csv
import matplotlib.pyplot as plt
from scipy.linalg import lstsq
import numpy as np

def moyenne_glissante_50(years : list[int], days : list[int]) -> list[int]:
    #Retourne les deux listes qui permettent de représenter la moyenne glissante sur 50 ans
    i = 0
    number_years = len(years)
    moyenne_years = []
    moyenne_days = []
    while i < number_years-4:
        sum_days = days[i]
        number_days = 1
        j = i+1
        while j < number_years and years[j] - years[i] <= 50:
            sum_days += days[j]
            number_days += 1
            j += 1
        if number_days >= 5:
            moyenne_years.append(years[i])
            moyenne_days.append(sum_days / number_days)
        i += 1
    return moyenne_years, moyenne_days

#Def de phi_i élement de la base de A ronde
def phi_i(i, x, x_i : list[int]):
    if x == x_i[i]:
        return 1
    elif i!=0 and x_i[i-1] < x < x_i[i]:
        return 1 + (x-x_i[i])/(x_i[i]-x_i[i-1])
    elif i!=len(x_i) and x_i[i] < x < x_i[i+1]:
        return 1-(x-x_i[i])/(x_i[i+1]-x_i[i]) 
    else:
        return 0


# Listes pour stocker les années et les jours de l'année
years : list[int] = []
days  : list[int] = []

# 1. Chargement des données depuis le fichier CSV
with open('cherry_blossoms.csv', newline='') as csvfile:    
    spamreader = csv.reader(csvfile, delimiter=';')    
    for row in spamreader:
        year = row[0]
        day = row[1]
        # On récupère l'année (colonne 'year') et le jour de floraison (colonne 'doy') uniquement si on a une donnée pour l'année
        if day != 'NA' and year != 'year':
            years.append(int(year))
            days.append(int(day))

# 2. Moyenne glissante sur 50 ans

years_moyenne, days_moyenne = moyenne_glissante_50(years, days)

#Question 7

#Création de la liste des x_i demandés dans l'énoncé
x_i = [812]
borne = 850
while borne <= 2000:
    x_i.append(borne)
    borne += 50
x_i.append(2015)

#Construction de la matrice de l'application linéaire A
A = [[0 for _ in range(len(x_i))] for _ in range(len(years))]
i = 0        #indice pour le point a_(i+1) i.e. une année dans years
while i < len(years): 
    j=0      #indice pour phi_j
    while j < len(x_i):
        A[i][j] = phi_i(j, years[i], x_i)
        j+=1
    i+=1

#Procédure des moindres carrés grâce à scipy.linalg.lstsq
y, res, rank, s = lstsq(A, days)
i=0
while i < len(y):
    y[i]= y[i]*phi_i(i, x_i[i], x_i)
    i+=1

#Procédure des moindres carrés grâce à numpy.linalg.solve
A_array = np.array(A)
A_t = A_array.transpose()
A_prod = np.dot(A_t, A) # multiplie matrice A par sa transposée
y_tmp = [[jour] for jour in days]  #instancie y  sous forme de matrice
y_t = np.dot(A_t, y_tmp)


#Création du graphique
plt.plot(years, days, 'o', color='#D25C72', markersize = 2, label ='Date de floraison enregistrée')
plt.plot(years_moyenne, days_moyenne, 'k', label='Moyenne glissante sur 50 ans')
plt.plot(x_i, y, color='green', label='Moindres carrés grâce à scipy')
plt.plot(x_i, np.linalg.solve(np.array(A_prod), np.array(y_t)), color='blue', label = 'Moindres carrés grâce à numpy')
plt.xticks([812, 1000, 1200, 1400, 1600, 1800, 2020])
plt.ylim(80, 125)
plt.yticks([80, 90, 100, 110, 120],['21 mars', '31 mars', '10 avril', '20 avril', '30 avril'])
plt.title('Date de pleine floraison des cerisiers japonais à Kyoto')
plt.ylabel('Jours')
plt.xlabel('Années')


plt.legend()
ax = plt.gca()

# Supprimer le cadre
ax.spines[:].set_visible(False)

xmin, xmax = ax.get_xlim()
ymin, ymax = ax.get_ylim()

# Dessiner les axes avec flèches
ax.annotate('', xy=(xmax, ymin), xytext=(xmin, ymin),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='black'))

ax.annotate('', xy=(xmin, ymax), xytext=(xmin, ymin),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='black'))


plt.show()
