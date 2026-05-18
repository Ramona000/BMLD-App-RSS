# functions/Einheitenumrechner.py

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# FAKTOREN
gewicht_faktoren = {
    "µg": 1e-6,
    "mg": 1e-3,
    "g": 1,
    "kg": 1e3,
    "t": 1e6
}

volumen_faktoren = {
    "µl": 0.001,
    "ml": 1,
    "l": 1000,
    "cm³": 1,
    "mm³": 0.001,
    "m³": 1_000_000
}

# GEWICHT UMRECHNUNG
def umrechnen_gewicht(wert, von_einheit, zu_einheit):
    """
    Gewichtseinheiten umrechnen (Basis: g)
    """

    wert_g = wert * gewicht_faktoren[von_einheit]

    return wert_g / gewicht_faktoren[zu_einheit]

# VOLUMEN UMRECHNUNG
def umrechnen_volumen(wert, von_einheit, zu_einheit):
    """
    Volumeneinheiten umrechnen (Basis: ml)
    """

    wert_ml = wert * volumen_faktoren[von_einheit]

    return wert_ml / volumen_faktoren[zu_einheit]

# FLÜSSIGKEIT -> GEWICHT
def volumen_zu_gewicht(
    volumen,
    volumen_einheit,
    dichte,
    ziel_einheit
):
    """
    Masse = Volumen × Dichte
    """

    volumen_ml = volumen * volumen_faktoren[volumen_einheit]

    masse_g = volumen_ml * dichte

    return masse_g / gewicht_faktoren[ziel_einheit]


# GEWICHT -> FLÜSSIGKEIT
def gewicht_zu_volumen(
    gewicht,
    gewicht_einheit,
    dichte,
    ziel_einheit
):
    """
    Volumen = Masse / Dichte
    """

    gewicht_g = gewicht * gewicht_faktoren[gewicht_einheit]

    volumen_ml = gewicht_g / dichte

    return volumen_ml / volumen_faktoren[ziel_einheit]

# HISTORIE SPEICHERN
def speichere_historie(
    kategorie,
    eingabewert,
    eingabeeinheit,
    ausgabewert,
    ausgabeeinheit,
    substanz_kategorie="-",
    substanz="-",
    dichte="-"
):
    """
    Speichert eine Berechnung in der Streamlit-Historie
    """

    neuer_eintrag = pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "kategorie": kategorie,
        "eingabewert": eingabewert,
        "eingabeeinheit": eingabeeinheit,
        "ausgabewert": ausgabewert,
        "ausgabeeinheit": ausgabeeinheit,
        "substanz_kategorie": substanz_kategorie,
        "substanz": substanz,
        "dichte": dichte,
        "favorite": False
    }])

    if "resultate_einheitenumrechner" not in st.session_state:
        st.session_state["resultate_einheitenumrechner"] = neuer_eintrag
    else:
        st.session_state["resultate_einheitenumrechner"] = pd.concat(
            [
                st.session_state["resultate_einheitenumrechner"],
                neuer_eintrag
            ],
            ignore_index=True
        )

#Grafik
gewicht_vergleiche = [
    (1, "eine Büroklammer 📎"),
    (5, "eine Feder 🪶"),
    (50, "ein Ei 🥚"),
    (250, "ein Stück Butter 🧈"),
    (1000, "eine Wasserflasche 💧"),
    (5000, "eine Bowlingkugel 🎳"),
    (80000, "ein Mensch 🚶"),
    (1_000_000, "ein kleines Auto 🚗")
]

volumen_vergleiche = [
    (1, "ein Tropfen 💧"),
    (5, "ein Teelöffel 🥄"),
    (30, "ein Schnapsglas 🥃"),
    (330, "eine Cola-Dose 🥤"),
    (500, "eine Wasserflasche 💦"),
    (1000, "ein Milchkarton 🥛"),
    (5000, "ein Putzeimer 🪣"),
    (100000, "eine Badewanne 🛁")
]


def finde_vergleich(wert, liste):
    passender_text = None

    for grenze, text in liste:
        if wert >= grenze:
            passender_text = text
        else:
            break

    return passender_text