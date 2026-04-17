import csv
import numpy as np
import scipy.linalg as spla
import matplotlib.pyplot as plt


donnees_floraison = {} 

with open('cherry_blossoms.csv', mode='r') as fichier:
    lecteur = csv.DictReader(fichier, delimiter=';') 
    for ligne in lecteur:
        if ligne['year'] and ligne['doy'] and ligne['doy'] != 'NA':
            annee = int(ligne['year'])
            doy = float(ligne['doy'])
            donnees_floraison[annee] = doy

# Listes pour nuages de point de la Q1
annees_enregistrees = list(donnees_floraison.keys())
dates_enregistrees = list(donnees_floraison.values())

# Tableaux numpy pour les calculs matriciels de Q7
a = np.array(annees_enregistrees)
D = np.array(dates_enregistrees)
K = len(a)


# CALCULS QUESTION 1 : Moyenne glissante

annees_moyenne = []
dates_moyenne = []

# On itère sur toutes les années où une floraison est enregistrée
for annee in annees_enregistrees:
    dates_dans_intervalle = []
    for annee_test in range(annee, annee + 50):
        if annee_test in donnees_floraison:
            dates_dans_intervalle.append(donnees_floraison[annee_test])
    
    # Condition (5 années enregistrées dans un intervalle de 50 ans)
    if len(dates_dans_intervalle) >= 5:
        moyenne = sum(dates_dans_intervalle) / len(dates_dans_intervalle)
        annees_moyenne.append(annee)
        dates_moyenne.append(moyenne)


# CALCULS QUESTION 7 : Moindres carrés

# Définition des nœuds (x_i) de 812 à 2015
noeuds = [812] + list(range(850, 2001, 50)) + [2015]
x = np.array(noeuds)
N = len(x) - 1

# Construction de la matrice M
M = np.zeros((K, N + 1))
for j in range(K):
    aj = a[j]
    for i in range(N):
        if x[i] <= aj <= x[i+1]:
            largeur = x[i+1] - x[i]
            M[j, i] = (x[i+1] - aj) / largeur
            M[j, i+1] = (aj - x[i]) / largeur 
            break

Mt = M.T
C_numpy = np.linalg.solve(Mt @ M, Mt @ D)

C_scipy, _, _, _ = spla.lstsq(M, D) 

# Affichage dans la console pour vérifier l'équivalence numérique entre les deux résolutions
diff = np.max(np.abs(C_numpy - C_scipy))
print(f"Vérification Q7 : La différence entre numpy et scipy est de {diff:.2e}")



plt.figure(figsize=(12, 6))

# Données brutes (points roses)
plt.scatter(annees_enregistrees, dates_enregistrees, s=6, color='palevioletred', 
            alpha=0.8, label='Date de floraison enregistrée')

# Résultat Q1 (Courbe noire)
plt.plot(annees_moyenne, dates_moyenne, color='black', linewidth=1.5, 
         label='Moyenne glissante sur 50 ans')

# Résultat Q7 (Courbe bleue avec points aux nœuds)
plt.plot(x, C_numpy, color='blue', linewidth=1.5, marker='o', markersize=4, 
         label='Moindres carrés (affine par morceaux)')

# Élargissement des limites du graphique pour commencer à 800 et finir un peu après 2020
plt.xlim(800, 2040)

valeurs_x = [812, 1000, 1200, 1400, 1600, 1800, 2020]
plt.xticks(valeurs_x)

valeurs_y = [80, 90, 100, 110, 120]
labels_y = ['21 mars', '31 mars', '10 avril', '20 avril', '30 avril']
plt.yticks(valeurs_y, labels_y)
plt.ylim(80, 125) 

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False, markerscale=2)

ax = plt.gca() 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False) 

ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False, markersize=6) 
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False, markersize=6) 

plt.tight_layout(rect=[0, 0, 1, 0.95]) # Ajustement pour ne pas couper la légende
plt.show()