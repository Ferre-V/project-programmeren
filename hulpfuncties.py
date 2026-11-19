import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import math

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

