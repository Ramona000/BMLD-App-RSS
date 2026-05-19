import streamlit as st
import pandas as pd

from utils.data_manager import DataManager
from views.Hilfefenster import show_help, show_navigation
from functions import show_header
from functions.Verdünnungsrechner import (
    verduennungsrechner,
    speichere_verlauf,
    plot_verduennung
)

# SESSION STATE INIT
if "resultate_verdünnungs_rechner" not in st.session_state:
    st.session_state["resultate_verdünnungs_rechner"] = pd.DataFrame(
        columns=["timestamp", "rechner", "C1", "C2", "V2", "V1", "favorite"]
    )

# Safety: favorite immer sicherstellen
df = st.session_state["resultate_verdünnungs_rechner"]

if "favorite" not in df.columns:
    df["favorite"] = False

df["favorite"] = df["favorite"].fillna(False).astype(bool)
st.session_state["resultate_verdünnungs_rechner"] = df

# HEADER
show_navigation(current_page="Verdünnungsrechner")
show_header("Verdünnungsrechner")


# INPUT
C1 = st.number_input("Anfangskonzentration (C1)", min_value=0.01)
C2 = st.number_input("Zielkonzentration (C2)", min_value=0.01)
V2 = st.number_input("Endvolumen (V2)", min_value=0.01)

# BERECHNUNG
if st.button("Berechnen"):

    if C1 > 0 and C2 > 0 and V2 > 0:

        result = verduennungsrechner(C1, C2, V2)

        st.success(f"V1: {result['V1']} ml")

        fig = plot_verduennung(C1, C2, V2, result["V1"])
        st.pyplot(fig)

        speichere_verlauf(result)
       
        # SwitchDrive speichern (nur nach neuer Berechnung)
        data_manager = DataManager()
        df = st.session_state["resultate_verdünnungs_rechner"].copy()
        df["timestamp"] = df["timestamp"].astype(str)    # Timestamp → ISO-String
        history = df.to_dict(orient="records")
        if st.session_state.get("username") is None:
            st.warning("Nicht angemeldet: Verlauf wurde nicht auf SwitchDrive gespeichert.")
        else:
            data_manager.save_user_data(history, "verduennungs_history.json")
    else:
        st.error("Fehlerhafte Eingabe")

# HISTORIE
st.subheader("Berechnungshistorie")

edited_df = st.data_editor(
    st.session_state["resultate_verdünnungs_rechner"],
    use_container_width=True,
    column_config={
        "favorite": st.column_config.CheckboxColumn("Favorit")
    },
    disabled=[
        "timestamp",
        "rechner",
        "C1",
        "C2",
        "V2",
        "V1"
    ]
)

st.session_state["resultate_verdünnungs_rechner"]= edited_df


# NAVIGATION / HELP
help_text = [
    "C1 eingeben",
    "C2 eingeben",
    "V2 eingeben",
    "Berechnen klicken"
]

col1, col2 = st.columns(2)

with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe", text_lines=help_text)