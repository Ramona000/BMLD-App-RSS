print("Konzentrationsrechner MODULE GELADEN")
import pandas as pd
def berechne_konzentration(stoffmenge: float, volumen: float) -> float | None:
    if volumen <= 0:
        return None
    return stoffmenge / volumen


def erstelle_verlaufseintrag(stoffmenge, volumen, konzentration):
    return pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "stoffmenge": stoffmenge,
        "volumen": volumen,
        "konzentration": konzentration
    }])

def speichere_verlauf(data_manager, dataframe, filename="data.csv"):
    data_manager.save_user_data(dataframe, filename)

def validiere_eingaben(stoffmenge: float, volumen: float) -> tuple[bool, str]:
    if volumen <= 0:
        return False, "Volumen muss größer als 0 sein"
    return True, ""