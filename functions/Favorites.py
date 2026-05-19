import pandas as pd

RECHNER_NAMEN = {
    "verdünnung": "Verdünnungsrechner",
    "titer": "Titer-Rechner",
    "ph": "pH-Rechner",
    "molare_masse": "Molaremassen-Rechner",
    "konzentration": "Konzentrationsrechner",
    "einheiten": "Einheitenumrechner"
}

def normalize_df(df, rechner_name: str):
    """
    Sorgt dafür, dass ALLE DataFrames gleich aufgebaut sind.
    """
    if df is None or df.empty:
        return df

    df = df.copy()

    # Pflichtspalten
    if "favorite" not in df.columns:
        df["favorite"] = False

    if "rechner" not in df.columns:
        df["rechner"] = rechner_name

    df["favorite"] = df["favorite"].fillna(False).astype(bool)
    df["rechner"] = df["rechner"].fillna(rechner_name).astype(str)

    return df