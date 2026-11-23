from math import sqrt
import matplotlib.pyplot as plt
from hulpfuncties import evalueer_plaatsing,get_random_coordinaten

# Project wetenschappelijk programmeren - opdracht 3
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


def sensorLocaties(coordinaten: list[tuple[float, float]], radius: float = 10) -> list[tuple[float, float]]:
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

        sensoren.append(kandidaat)

        # Alle nieuw gedekte bedrijven uit de lijst met ongedekte bedrijven halen
        nieuwe_ongedekt = []
        for bedrijf in ongedekt:
            if bedrijf not in meeste_gedekt:
                nieuwe_ongedekt.append(bedrijf)
        ongedekt = nieuwe_ongedekt

    return sensoren


evalueer_plaatsing(sensorLocaties, seed=42, radius=10, n=100)
plt.show()

# Gemiddelde testen
#seeds = range(100)
#r = 10
#totaal = 0
#for s in seeds:
#    coords = get_random_coordinaten(n=100, seed=s)
#    res = sensorLocaties(coords, radius=r)
#    print(f"seed {s}: {len(res)} sensoren")
#    totaal += len(res)
#print("gemiddeld aantal sensoren:", totaal / len(seeds))
#