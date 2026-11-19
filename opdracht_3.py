
from hulpfuncties import get_random_coordinaten, evalueer_plaatsing
from math import sqrt
import matplotlib.pyplot as plt


def bereken_afstand(p1: tuple, p2: tuple) -> float:
    """
    Bereken de Euclidische afstand tussen twee punten.

    Parameters:
        p1 (tuple): Coördinaten van het eerste punt.
        p2 (tuple): Coördinaten van het tweede punt.

    Returns:
        float: De afstand tussen beide punten.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return sqrt(dx**2 + dy**2)


def check_bedrijven_gedekt(
    bedrijven: list[tuple], sensor: tuple, radius: float) -> list[tuple]:
    """
    Bepaal welke bedrijven binnen het bereik van een sensor liggen.

    Parameters:
        bedrijven (list[tuple]): Lijst met bedrijfcoördinaten.
        sensor (tuple): Coördinaten van de sensor.
        radius (float): Maximaal bereik van de sensor.

    Returns:
        list[tuple]: Lijst met gedekte bedrijven.
    """
    gedekt = []

    for bedrijf in bedrijven:
        afstand = bereken_afstand(bedrijf, sensor)

        if afstand <= radius:
            gedekt.append(bedrijf)

    return gedekt


def sensorLocaties(coordinaten: list[tuple], radius: float = 10) -> list[tuple]:
    """
    Bepaal sensorlocaties zodat alle bedrijven gedekt zijn.

    Gebruikt een greedy algoritme dat telkens een sensor plaatst
    op de locatie waar de meeste nog ongedekte bedrijven liggen.

    Parameters:
        coordinaten (list[tuple]): Lijst met bedrijfcoördinaten.
        radius (float): Bereik van elke sensor. Standaard 10.

    Returns:
        list[tuple]: Lijst met gekozen sensorlocaties.
    """
    sensoren = []
    ongedekt = coordinaten.copy()

    while len(ongedekt) > 0:
        meeste_gedekt = []
        kandidaat = None

        for bedrijf in ongedekt:
            mogelijk_gedekt = check_bedrijven_gedekt(
                ongedekt, bedrijf, radius
            )

            if len(mogelijk_gedekt) > len(meeste_gedekt):
                meeste_gedekt = mogelijk_gedekt
                kandidaat = bedrijf

        sensoren.append(kandidaat)

        ongedekt = [
            bedrijf for bedrijf in ongedekt
            if bedrijf not in meeste_gedekt
        ]

    return sensoren


# Tests
seeds = range(1000)
sensor_aantallen = []

for seed in seeds:
    coordinaten = get_random_coordinaten(seed=seed)
    sensoren = sensorLocaties(coordinaten)

    sensor_aantallen.append(len(sensoren))

    print(f"TEST {seed}: aantal sensoren = {len(sensoren)}")


# BGemiddelde
gemiddelde = sum(sensor_aantallen) / len(sensor_aantallen)
print(f"Gemiddelde: {gemiddelde}")


# Voorbeeld
evalueer_plaatsing(sensorLocaties, seed=42, radius=10, n=100)
plt.show()
