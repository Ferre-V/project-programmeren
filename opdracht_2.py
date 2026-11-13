# project wet. progr. Opdracht 2

def verwerk_lege(waarde: str) -> float:
    """TODO: docstr aanvullen"""
    proper = waarde.strip()
    if proper == "/" or proper == "":
        return None
    return float(proper)

def verwerk_meting(meting: list) -> dict:
    """TODO: docstr aanvullen"""
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
    """TODO: docstr aanvullen"""
    resultaten = {
        "dag": [],
        "temp": [],
        "ph": [],
        "no3": [],
        "po4": [],
        "o2": [],
    }

    with open(pad, "r") as f:
        rijen = f.readlines()

    rijen.pop(0) # 1ste rij met titels verwijderen

    for rij in rijen:
        rij = rij.strip()

        onverwerkte_waarden = rij.split(";")
        verwerkte_meting = verwerk_meting(onverwerkte_waarden)

        for param in resultaten:
            resultaten[param].append(verwerkte_meting[param])
    return resultaten

def bereken_wqi(temp, ph, no3, po4, o2) -> str:
    """TODO: docstr aanvullen"""
    strafpunten = 0

    # Temp.
    if 20.0 <= temp <= 25.0:
        strafpunten += 1
    elif temp > 25.0:
        strafpunten += 2

    # ph
    if (5.5 < ph < 6.5) or (8.5 < ph < 9.0):
        strafpunten += 1
    elif ph <= 5.5 or ph >= 9.0:
        strafpunten += 2

    # no3
    if 10.0 <= no3 <= 25.0:
        strafpunten += 1
    elif no3 > 25.0:
        strafpunten += 2

    # po4
    if 0.1 <= po4 <= 0.5:
        strafpunten += 1
    elif po4 > 0.5:
        strafpunten += 2

    # o2
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
    """TODO: docstr aanvullen"""
    aantallen: dict = {"hoog": 0, "gemiddeld": 0, "slecht": 0}

    for t, p, n, po, o in zip(  #zip hier om direct over alle param. te lopen
        meetgegevens["temp"],
        meetgegevens["ph"],
        meetgegevens["no3"],
        meetgegevens["po4"],
        meetgegevens["o2"],
    ):
        if None in (t, p, n, po, o):  #Wegfilteren van dagen met lege meetwaarden
            continue

        kwaliteit = bereken_wqi(t, p, n, po, o)
        aantallen[kwaliteit] += 1

    return aantallen

def print_frequentietabel(aantallen: dict) -> None:
    """TODO: docstr aanvullen"""
    print("-"*16)
    print(f"{'Kwaliteit'} {'Aantal'}")
    print("-"*16)
    for kwaliteit, aantal in aantallen.items():
        print(f"{kwaliteit:<12} {aantal:>3}")
    print("-"*16)


# Vanaf hier deel 2 (inerpolatie)

def interpoleer_punt(x1,y1,x2,y2,x) -> float:
    """TODO: docstr aanvullen"""
    return y1 + ( (y2-y1) / (x2-x1) ) * (x-x1) # Formule overgenomen uit wikipedia

def interpoleer_parameter(dagen: list, waarden: list) -> list:
    """TODO: docstr aanvullen"""

    geinterpoleerd = list(waarden)
    aantal = len(waarden)

    for i in range(aantal):
        if geinterpoleerd[i] is None:
            l = i-1  # Eerste punt links dat wel bestaat zoeken
            while waarden[l] is None: 
                l-=1

            r = i+1 # Zelfde maar a,n rechterkant
            while waarden[r] is None:
                r+=1

            x1 = dagen[l]
            x2 = dagen[r]
            y1 = waarden[l]
            y2 = waarden[r]
            x = dagen[i]

            geinterpoleerd[i] = interpoleer_punt(x1,y1,x2,y2,x)

    return geinterpoleerd

def interpoleer_meetwaarden(meetgegevens:dict) -> dict:
    """TODO: docstr aanvullen"""

    aangevulde_data = {"dag":list(meetgegevens["dag"])}
    dagen = meetgegevens["dag"]

    for param in ("temp", "ph", "no3", "po4", "o2"):
        aangevulde_data[param] = interpoleer_parameter(dagen, meetgegevens[param])

    return aangevulde_data



PAD_MEETGEGEVENS = "bestanden/meetgegevens.txt"
meetgegevens = lees_bestand(PAD_MEETGEGEVENS)
freq = frequentietabel(meetgegevens)
print_frequentietabel(freq)

geinterpoleerd = interpoleer_meetwaarden(meetgegevens)
freq2 = frequentietabel(geinterpoleerd)
print_frequentietabel(freq2)
