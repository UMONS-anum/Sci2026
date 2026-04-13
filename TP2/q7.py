import csv
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def load_csv_data(filename: str):
    ''' Charge les données depuis un fichier csv

    Args:
        filename (str) : le chemin d'accès vers le fichier

    Returns:
        np.array : les années de floraison
        np.array : les dates de floraison
    '''
    years = []
    days = []

    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader)  # ignorer l'en-tête

        for row in reader:
            year = int(row[0])

            if row[1] == "NA":
                day = np.nan
            else:
                day = float(row[1])

            years.append(year)
            days.append(day)

    return np.array(years, dtype=float), np.array(days, dtype=float)


def build_breakpoints():
    '''
    Renvoie les points de rupture interne {850, 900, ..., 1950, 2000}
    '''
    breakpoints = list(range(850, 2001, 50))
    return breakpoints


def build_matrix(x: np.ndarray, breakpoints: list[int]) -> np.ndarray:
    '''
    Retourne la matrice M pour le problème min||MB-D|| (voir rapport).
    Args:
        x (np.ndarray) : les années de floraison
        breakpoints (list[int]) : les breakpoints internes (x_i, i in {1, ..., N-1})
    '''
    columns = [np.ones(len(x)), x]

    for c in breakpoints:
        columns.append(np.maximum(0, x - c))

    return np.column_stack(columns)


def continuous_least_squares(x: np.ndarray, y: np.ndarray, breakpoints: list[int]):
    ''' Utilise sp.linalg.lstsq pour calculer les coefficients beta
    
    Args:
        x (np.ndarray) : les années de floraison
        y (np.ndarray) : les dates de floraison
    
    Return:
        beta : les coefficients beta
        M : la matrice M
        x_valid : les années pour lesquelles on a une date de floraison non-nulle
        y_valid : les dates de floraisons non-nulles
    '''
    valid_mask = ~np.isnan(y)
    x_valid = x[valid_mask]
    y_valid = y[valid_mask]

    M = build_matrix(x_valid, breakpoints)
    beta, residuals, rank, singular_values = sp.linalg.lstsq(M, y_valid)

    return beta, M, x_valid, y_valid


def continuous_solve(x: np.ndarray, y: np.ndarray, breakpoints: list[int]):
    '''Utilise np.linalg.solve pour résoudre le système linéaire associé
    
    Args:
        x (np.ndarray) : les années de floraison
        y (np.ndarray) : les dates de floraison
    
    Return:
        beta : les coefficients beta
        M : la matrice M
        x_valid : les années pour lesquelles on a une date de floraison non-nulle
        y_valid : les dates de floraisons non-nulles
    '''
    valid_mask = ~np.isnan(y)
    x_valid = x[valid_mask]
    y_valid = y[valid_mask]

    M = build_matrix(x_valid, breakpoints)
    MT = np.transpose(M)
    MT_M = np.matmul(MT, M)
    MT_y = np.matmul(MT, y_valid)
    beta = np.linalg.solve(MT_M, MT_y)

    return beta, M, x_valid, y_valid


def evaluate_model(x: np.ndarray, beta: np.ndarray, breakpoints: list[int]) -> np.ndarray:
    '''Construit la matrice M et calcule MB
    
    Args:
        x (np.ndarray) : les années de floraison
        beta (np.ndarray) : les coefficients beta
        breakpoints (list[int]) : les points de rupture internes
    
    Returns:
        le produit matriciel des matrices M et beta (B)
    '''
    M = build_matrix(x, breakpoints)
    return M @ beta


def day_of_year_to_date_str(day_of_year, reference_year=2021):
    '''Renvoie les dates en str'''
    date = datetime(reference_year, 1, 1) + timedelta(days=int(round(day_of_year)) - 1)
    return date.strftime("%d %B")


if __name__ == "__main__":
    years, days = load_csv_data("cherry_blossoms.csv")
    breakpoints = build_breakpoints()

    # True si on veut utiliser scipy.linalg.lstsq, False si on veut utiliser np.linalg.solve
    mode_lstsq = True
    
    if(mode_lstsq):
        beta, M, x_valid, y_valid = continuous_least_squares(years, days, breakpoints)
    else:
        beta, M, x_valid, y_valid = continuous_solve(years, days, breakpoints)

    # Courbe ajustée
    x_plot = np.linspace(812, 2015, 2000)
    y_plot = evaluate_model(x_plot, beta, breakpoints)

    plt.figure(figsize=(10, 6))
    plt.scatter(x_valid, y_valid, s=4, label="Dates observées", color="pink")
    plt.plot(x_plot, y_plot, label="Approximation affine continue par morceaux", color="black")

    # Lignes verticales aux breakpoints
    for c in breakpoints:
        plt.axvline(c, linewidth=0.5, alpha=0.2)

    yticks = [80, 90, 100, 110, 120]
    ylabels = [day_of_year_to_date_str(d) for d in yticks]
    plt.yticks(yticks, ylabels)

    plt.xlabel("Année")
    plt.ylabel("Date de floraison")
    plt.title("Floraison des cerisiers")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()