# Project wetenschappelijk programmeren - opdracht 1

def controle_input(staal: str) -> bool:
    """
    Controleert of de input bestaat uit 5 geldige meetwaarden die binnen hun natuurlijk bereik liggen.

    Parameters
    ----------
    staal : str
        De ingevoerde string met 5 meetwaarden gescheiden door ';'

    Returns
    -------
    bool
        True indien het staal geldig is, anders False.
    """
    waarden = staal.split(";")

    if len(waarden) != 5:
        return False

    nieuwe_waarden = []

    for waarde in waarden:
        waarde = waarde.strip()

        if waarde.count(".") > 1:
            return False
        
        if waarde == "" or waarde == ".":
            return False 
        
        for kar in waarde:
            if kar not in "0123456789.":
                return False

        nieuwe_waarden.append(waarde)   

    temp = float(nieuwe_waarden[0])
    pH = float(nieuwe_waarden[1])
    nitraat = float(nieuwe_waarden[2])
    fosfaat = float(nieuwe_waarden[3])
    zuurstof = float(nieuwe_waarden[4])

    if temp < 0 or temp > 50:
        return False
    
    if pH <= 0 or pH > 14:
        return False
    
    if nitraat < 0 or fosfaat < 0 or zuurstof < 0:
        return False
    
    else:
        return True   


def bereken_strafpunten(staal: str) -> int:
    """
    Berekent de som van de strafpunten van een geldig waterstaal.

    Parameters
    ----------
    staal : str
        De vijf meetwaarden gescheiden door een ';'.

    Returns
    -------
    int
        Het totaal aantal strafpunten van een staal.
    """
    waarden = staal.split(";")

    for i in range(len(waarden)):
        waarden[i] = waarden[i].strip()

    temp = float(waarden[0])
    pH = float(waarden[1])
    nitraat = float(waarden[2])
    fosfaat = float(waarden[3])
    zuurstof = float(waarden[4])

    strafpunten = 0
    
    if temp > 25:
        strafpunten += 2
    elif temp >= 20:
        strafpunten += 1

    if pH <= 5.5 or pH >= 9:
        strafpunten += 2
    elif pH < 6.5 or pH > 8.5:
        strafpunten += 1  

    if nitraat > 25:
        strafpunten += 2
    elif nitraat >= 10:
        strafpunten += 1             

    if fosfaat > 0.5:
        strafpunten += 2
    elif fosfaat >= 0.1:
        strafpunten += 1

    if zuurstof < 4:
        strafpunten += 2
    elif zuurstof <= 7:
        strafpunten += 1

    return strafpunten


def bereken_WQI(strafpunten: int) -> str:
    """
    Bepaalt de waterkwaliteit aan de hand van het aantal strafpunten.

    Parameters
    ----------
    strafpunten : int
        De totale som van de strafpunten.

    Returns
    -------
    str
        De kwaliteitsklasse ('hoog', 'gemiddeld' of 'slecht').
    """
    if strafpunten <= 2:
        return "hoog"
    elif strafpunten <= 5:
        return "gemiddeld"
    else:
        return "slecht"


staal = input("Geef een staal: ")
while staal.strip().lower() != "stop":

    if controle_input(staal):
        strafpunten = bereken_strafpunten(staal)
        kwaliteit = bereken_WQI(strafpunten)
        print("WQI:", kwaliteit)

    else:
        print("Ongeldige input")

    staal = input("Geef een nieuw staal: ")
print("Programma stopt")