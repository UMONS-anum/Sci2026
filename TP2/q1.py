import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def load_csv_data(filename: str):
    ''' Charge les données depuis un fichier csv

    Args:
        filename (str) : le chemin d'accès vers le fichier

    Returns:
        np.ndarray : les années de floraison
        np.ndarray : les dates de floraison
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

def rolling_mean_50(years: np.ndarray, days: np.ndarray):
    '''
    Renvoie les moyennes glissantes sur 50 ans pour lesquelles il y a au 
    moins 5 dates de floraison dans l'intervalle de 50 ans

    Args:
        years (np.ndarray) : les années de floraison
        days (np.ndarray) : les jours de floraison

    Returns:
        np.ndarray : les années pour lesquelles il y a une moyenne
        np.ndarray : les moyennes sur 50 ans
    '''
    mean_years = []
    mean_days = []

    for i in range(len(years)):
        start_year = years[i]
        end_year = start_year + 49

        mask = (years >= start_year) & (years <= end_year)
        window_days = days[mask]

        valid_days = window_days[~np.isnan(window_days)]

        if len(valid_days) >= 5:
            mean_years.append(start_year)
            mean_days.append(np.mean(valid_days))

    return np.array(mean_years), np.array(mean_days)


def day_of_year_to_date_str(day_of_year, reference_year=2021):
    '''Renvoie les dates en str'''
    date = datetime(reference_year, 1, 1) + timedelta(days=int(day_of_year) - 1)
    return date.strftime("%d %B")


if __name__ == "__main__":
    years, days = load_csv_data("cherry_blossoms.csv")
    mean_years, mean_days = rolling_mean_50(years, days)

    plt.figure(figsize=(10, 6))
    plt.scatter(years, days, s=4, label="Date de floraison enregistrée", color="pink")
    plt.plot(mean_years, mean_days, label="Moyenne glissante sur 50 ans", color="black")

    yticks = [80, 90, 100, 110, 120]
    ylabels = [day_of_year_to_date_str(d) for d in yticks]
    plt.yticks(yticks, ylabels)

    plt.xlabel("Année")
    plt.ylabel("Date de floraison")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()