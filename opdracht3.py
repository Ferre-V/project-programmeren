from math import sqrt
import matplotlib.pyplot as plt
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import math

# <-- HULPFUNCTIES --> (uit helpfuncties.py)
def get_random_coordinaten(n = 100, low = 0, high = 100, seed = None):
    """
    Genereer een lijst van n willekeurige coördinaten binnen een vierkant van (low, low) tot (high, high).

    Parameters
    ----------
    n : int, optional
        De hoeveelheid random coördinaten die gegenereerd moeten worden. De default-waarde is 100.
    low : float, optional
        De laagste waarde voor de x- en y-coördinaten. De default-waarde is 0.
    high : float, optional
        De hoogste waarde voor de x- en y-coördinaten. De default-waarde is 100.
    seed : int, optional
        Random seed for reproduceerbaarheid. By default wordt er geen seed gebruikt.

    Returns
    -------
    list[tuple[float, float]]
        Een lijst van n willekeurige coördinaten binnen het opgegeven bereik.
    """
    if seed:
        random.seed(seed)
    return [(random.uniform(low, high), random.uniform(low, high)) for _ in range(n)]

def evalueer_plaatsing(f, seed = None, radius = 10, n = 100):
    """
    Evalueer en visualiseer een sensor plaatsing functie.

    Parameters
    ----------
    f : function(bedrijven_coords: list[tuple[float, float]], radius: float, ...) -> list[tuple[float, float]]
        De functie die de sensor coördinaten genereert.
    seed : int, optional
        Random seed for reproduceerbaarheid. By default wordt er geen seed gebruikt.
    radius : float, optional
        Het bereik van de sensoren. De default-waarde is 10.
    n : int, optional
        De hoeveelheid random coördinaten die gegenereerd moeten worden. De default-waarde is 100.

    Returns
    -------
    fig, ax : matplotlib.figure.Figure, matplotlib.axes._subplots.AxesSubplot
        De figuur en as objecten van de gegenereerde visualisatie.
    """
    b = get_random_coordinaten(n = n, seed = seed)
    res = f(b, radius)
    assert type(res) == list and all(len(x) == 2 for x in res), "Functie retourneert onverwacht resultaat. Verwacht: lijst van tuples/lijsten met 2 elementen (x,y)."
    valid = np.array([min((math.dist(x, y) for y in res), default=math.inf) < radius + 1e-9 for x in b])

    fig, ax = plt.subplots(figsize=(8, 8)) # 8

    point_kwargs = {"s": 50, "zorder": 3}
    circle_kwargs = {"facecolor": "#2a78d6", "alpha": 0.12,
                     "edgecolor": "#2a78d6", "linewidth": 1.2}

    ax.scatter(np.array(b)[valid,0], np.array(b)[valid,1], 
               c="g", label="bedrijf binnen sensor bereik", **point_kwargs)
    ax.scatter(np.array(b)[~valid,0], np.array(b)[~valid,1], 
               c="r", marker="X", label="bedrijf buiten sensor bereik", **point_kwargs)

    for cx, cy in res:
        ax.add_patch(Circle((cx, cy), radius, **circle_kwargs))

    if res:
        cxs, cys = zip(*res)
        ax.scatter(cxs, cys, marker="+", color="black", 
                   zorder=3, s = point_kwargs["s"] * 0.3, label="sensor")

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False)
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_title(f"{sum(valid)}/{n} bedrijven binnen bereik met {len(res)} sensoren")
    return fig, ax

# <-- ECHTE CODE -->


def bereken_afstand(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Berekent de Euclidische afstand tussen twee punten.

    Parameters
    ----------
    p1 : tuple[float, float]
        De (x, y)-coördinaten van het eerste punt.
    p2 : tuple[float, float]
        De (x, y)-coördinaten van het tweede punt.

    Returns
    -------
    float
        De Euclidische afstand tussen beide punten.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return sqrt(dx**2 + dy**2)

def check_bedrijven_gedekt(bedrijven: list[tuple[float, float]], sensor: tuple[float, float], radius: float) -> list[tuple[float, float]]:
    """
    Bepaalt welke bedrijven binnen het bereik van een sensor liggen.

    Parameters
    ----------
    bedrijven : list[tuple[float, float]]
        Een lijst met (x, y)-coördinaten van bedrijven.
    sensor : tuple[float, float]
        De (x, y)-coördinaten van de sensor.
    radius : float
        Het maximale bereik van de sensor.

    Returns
    -------
    list[tuple[float, float]]
        Een lijst met de coördinaten van alle gedekte bedrijven.
    """
    gedekt = []

    for bedrijf in bedrijven:
        afstand = bereken_afstand(bedrijf, sensor)

        if afstand <= radius:
            gedekt.append(bedrijf)

    return gedekt


def sensorLocaties(coordinaten: list[tuple[float, float]], radius:float = 10) -> list[tuple[float, float]]:
    """
    Bepaalt sensorlocaties zodat alle bedrijven gedekt zijn.
    Kiest telkens het ongedekte bedrijf dat de meeste andere bedrijven
    binnen bereik kan dekken en plaatst daar een sensor.

    Parameters
    ----------
    coordinaten : list[tuple[float, float]]
        Een lijst met (x, y)-coördinaten van de bedrijven.
    radius : float, optional
        Het bereik van elke sensor. De standaardwaarde is 10.

    Returns
    -------
    list[tuple[float, float]]
        Een lijst met de gekozen (x, y)-coördinaten van de sensoren.
    """
    sensoren = []
    ongedekt = coordinaten.copy()

    while len(ongedekt) > 0:
        meeste_gedekt = []
        kandidaat = None

        for bedrijf in ongedekt:
            mogelijk_gedekt = check_bedrijven_gedekt(ongedekt, bedrijf, radius)

            if len(mogelijk_gedekt) > len(meeste_gedekt):
                meeste_gedekt = mogelijk_gedekt
                kandidaat = bedrijf

        if kandidaat is not None:
            sensoren.append(kandidaat)

        ongedekt = [bedrijf for bedrijf in ongedekt if bedrijf not in meeste_gedekt]

    return sensoren


# Visualisatie van de sensoren en de bedrijven
evalueer_plaatsing(sensorLocaties, seed=42, radius=10, n=100)
plt.show()