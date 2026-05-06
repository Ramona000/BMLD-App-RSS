from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import math

def calculate_ph(typ, konzentration):

    if typ == "starke Säure":
        pH = -math.log10(konzentration)
    else:
        pOH = -math.log10(konzentration)
        pH = 14 - pOH

    if pH < 7:
        category = "sauer"
    elif pH == 7:
        category = "neutral"
    else:
        category = "basisch"

    return {
        "timestamp": datetime.now(pytz.timezone("Europe/Zurich")),
        "Typ": typ,
        "Konzentration (mol/L)": konzentration,
        "pH": round(pH, 2),
        "Kategorie": category,
        "favorite": False
    }