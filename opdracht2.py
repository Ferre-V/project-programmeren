# Project Wetenschappelijk Programmeren - Opdracht 2


def verwerk_lege(waarde: str) -> float | None:
    """
    Zet een meetwaarde om naar een float, of naar None indien de waarde ontbreekt ('/').

    Parameters
    ----------
    waarde : str
        De onverwerkte string van 1 meetwaarde uit het bestand.

    Returns
    -------
    float | None
        De meetwaarde als float, of None wanneer de waarde '/' of leeg is.
    """
    proper = waarde.strip()

    if proper == "/" or proper == "":
        return None
    
    return float(proper)


def verwerk_meting(meting: list[str]) -> dict:
    """
    Verwerkt 1 reeds gesplitste rij uit het databestand tot een dictionary van de meetwaarden.

    Parameters
    ----------
    meting : list[str]
        Een lijst met 6 strings, nl. de string van de dag en die van de 5 meetwaarden.

    Returns
    -------
    dict
        Een dictionary met de sleutels 'dag', 'temp', 'ph', 'no3', 'po4' en 'o2'.
    """

    dag_nr = int(meting[0].replace("Dag", "").strip())

    return {
        "dag": dag_nr,
        "temp": verwerk_lege(meting[1]),
        "ph": verwerk_lege(meting[2]),
        "no3": verwerk_lege(meting[3]),
        "po4": verwerk_lege(meting[4]),
        "o2": verwerk_lege(meting[5]),
    }


def lees_bestand(pad: str) -> dict:
    """
    Leest het bestand met meetgegevens in en groepeert de waarden per parameter in lijsten.

    Parameters
    ----------
    pad : str
        Het bestandspad naar het tekstbestand met meetgegevens.

    Returns
    -------
    dict
        Een dictionary waarin elke parameter verwijst naar een lijst van meetwaarden over alle dagen.
    """
    resultaten = {
        "dag": [],
        "temp": [],
        "ph": [],
        "no3": [],
        "po4": [],
        "o2": [],
    }

    with open(pad, "r", encoding="utf-8") as f:  #encoding als extra veiligheid
        rijen = f.readlines()

    rijen.pop(0)  # 1ste rij met kolomheaders verwijderen

    for rij in rijen:
        rij = rij.strip()
        if rij == "":        #Lege rijen skippen (extra veiligheid)
            continue

        onverwerkte_waarden = rij.split(";")
        verwerkte_meting = verwerk_meting(onverwerkte_waarden)

        for param in resultaten:
            resultaten[param].append(verwerkte_meting[param])

    return resultaten


def bereken_wqi(temp: float, ph: float, no3: float, po4: float, o2: float) -> str:
    """
    Berekent het aantal strafpunten op basis van de 5 parameters en bepaalt de waterkwaliteit.

    Parameters
    ----------
    temp : float
        De watertemperatuur.
    ph : float
        De zuurtegraad (pH).
    no3 : float
        De nitraatconcentratie.
    po4 : float
        De fosfaatconcentratie.
    o2 : float
        De concentratie opgeloste zuurstof.
        
    Returns
    -------
    str
        De kwaliteitsklasse van het waterstaal ('hoog', 'gemiddeld' of 'slecht').
    """
    strafpunten = 0

    # Temperatuur
    if 20.0 <= temp <= 25.0:
        strafpunten += 1
    elif temp > 25.0:
        strafpunten += 2

    # pH
    if (5.5 < ph < 6.5) or (8.5 < ph < 9.0):
        strafpunten += 1
    elif ph <= 5.5 or ph >= 9.0:
        strafpunten += 2

    # Nitraat
    if 10.0 <= no3 <= 25.0:
        strafpunten += 1
    elif no3 > 25.0:
        strafpunten += 2

    # Fosfaat
    if 0.1 <= po4 <= 0.5:
        strafpunten += 1
    elif po4 > 0.5:
        strafpunten += 2

    # Zuurstof
    if 4.0 <= o2 <= 7.0:
        strafpunten += 1
    elif o2 < 4.0:
        strafpunten += 2

    if strafpunten <= 2:
        return "hoog"
    elif strafpunten <= 5:
        return "gemiddeld"
    return "slecht"


def frequentietabel(meetgegevens: dict) -> dict:
    """
    Telt hoe vaak elke waterkwaliteit voorkomt over alle volledige dagen in de dataset.

    Parameters
    ----------
    meetgegevens : dict
        De dictionary met lijsten van meetwaarden per parameter.

    Returns
    -------
    dict
        Een dictionary met de aantallen voor 'hoog', 'gemiddeld' en 'slecht'.
    """
    aantallen = {"hoog": 0, "gemiddeld": 0, "slecht": 0}

    for t, p, n, po, o in zip(  # zip om gelijktijdig over alle parameters te lopen
        meetgegevens["temp"],
        meetgegevens["ph"],
        meetgegevens["no3"],
        meetgegevens["po4"],
        meetgegevens["o2"],
    ):
        if None in (t, p, n, po, o):  # Wegfilteren van dagen met lege meetwaarden
            continue

        kwaliteit = bereken_wqi(t, p, n, po, o)
        aantallen[kwaliteit] += 1

    return aantallen


def print_frequentietabel(aantallen: dict) -> None:
    """
    Print een overzichtstabel van de waterkwaliteiten en hun aantallen naar de console.

    Parameters
    ----------
    aantallen : dict
        Een dictionary met de frequenties voor 'hoog', 'gemiddeld' en 'slecht'.

    Returns
    -------
    None
    """
    print("-" * 16)
    print("Kwaliteit Aantal")
    print("-" * 16)
    for kwaliteit, aantal in aantallen.items():
        print(f"{kwaliteit:<12} {aantal:>3}")
    print("-" * 16)


# Vanaf hier deel 2 (interpolatie)


def interpoleer_punt(x1: int, y1: float, x2: int, y2: float, x: int) -> float:
    """
    Berekent een ontbrekende waarde op tijdstip x via lineaire interpolatie tussen twee bekende punten.

    Parameters
    ----------
    x1 : int
        Het dagnummer van het vorige geldige meetpunt.
    y1 : float
        De meetwaarde op dag x1.
    x2 : int
        Het dagnummer van het volgende geldige meetpunt.
    y2 : float
        De meetwaarde op dag x2.
    x : int
        Het dagnummer waarvoor de waarde geïnterpoleerd wordt.

    Returns
    -------
    float
        De lineair geïnterpoleerde meetwaarde op dag x.
    """
    return y1 + ((y2 - y1) / (x2 - x1)) * (x - x1)


def interpoleer_parameter(dagen: list[int], waarden: list[float | None]) -> list[float]:
    """
    Vult alle ontbrekende waarden (None) in de tijdreeks van één parameter aan via lineaire interpolatie.

    Parameters
    ----------
    dagen : list[int]
        De lijst met opeenvolgende dagnummers.
    waarden : list[float | None]
        De lijst met meetwaarden van één parameter, inclusief None voor ontbrekende metingen.

    Returns
    -------
    list[float]
        Een nieuwe lijst waarin de ontbrekende waarden zijn aangevuld.
    """
    geinterpoleerd = list(waarden)
    aantal = len(waarden)

    for i in range(aantal):
        if geinterpoleerd[i] is None:
            l = i - 1  # Eerste punt links dat wel bestaat zoeken
            while l >= 0 and waarden[l] is None:   #l >= 0 anders kan pointer negatief worden.
                l -= 1

            r = i + 1  # Zelfde maar aan rechterkant
            while r < aantal and waarden[r] is None:  # r < aantal anders kan pointer OutOfIndex geven.
                r += 1

            if l >= 0 and r < aantal:
                x1 = dagen[l]
                x2 = dagen[r]
                y1 = waarden[l]
                y2 = waarden[r]
                x = dagen[i]

                geinterpoleerd[i] = interpoleer_punt(x1, y1, x2, y2, x)

    return geinterpoleerd 

def interpoleer_meetwaarden(meetgegevens: dict) -> dict:
    """
    Voert lineaire interpolatie uit op alle vijf waterkwaliteitsparameters.

    Parameters
    ----------
    meetgegevens : dict
        De dictionary met onvolledige meetreeksen per parameter.

    Returns
    -------
    dict
        Een nieuwe dictionary met aangevulde meetreeksen voor alle parameters.
    """
    aangevulde_data = {"dag": list(meetgegevens["dag"])}
    dagen = meetgegevens["dag"]

    for param in ("temp", "ph", "no3", "po4", "o2"):
        aangevulde_data[param] = interpoleer_parameter(dagen, meetgegevens[param])

    return aangevulde_data


PAD_MEETGEGEVENS = "meetgegevens.txt"
meetgegevens = lees_bestand(PAD_MEETGEGEVENS)
freq = frequentietabel(meetgegevens)
print_frequentietabel(freq)

geinterpoleerd = interpoleer_meetwaarden(meetgegevens)
freq2 = frequentietabel(geinterpoleerd)
print_frequentietabel(freq2)