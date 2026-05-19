import streamlit as st
import pandas as pd

st.title("⭐ Favoriten")

# Alle DataFrames sammeln
dfs = [
    st.session_state.get("resultate_verdünnungs_rechner"),
    st.session_state.get("resultate_titer_rechner"),
    st.session_state.get("resultate_ph_rechner"),
    st.session_state.get("resultate_molare_masse_rechner"),
    st.session_state.get("resultate_konzentrations_rechner"),
    st.session_state.get("resultate_einheitenumrechner"),
]

# Nur gültige DataFrames
dfs = [df for df in dfs if df is not None and not df.empty]

if not dfs:
    st.info("Noch keine Daten vorhanden.")
    st.stop()

# Zusammenführen
df = pd.concat(dfs, ignore_index=True)

# Safety: favorite absichern
if "favorite" not in df.columns:
    st.info("Keine Favoriten-Spalte gefunden.")
    st.stop()

df["favorite"] = df["favorite"].fillna(False)

# Nur Favoriten
favoriten = df[df["favorite"] == True]

if favoriten.empty:
    st.info("Noch keine Favoriten markiert.")
    st.stop()

# 🔽 Filter nach Rechner
rechner_liste = ["Alle"] + sorted(favoriten["rechner"].unique())
auswahl = st.selectbox("Rechner filtern", rechner_liste)

if auswahl != "Alle":
    favoriten = favoriten[favoriten["rechner"] == auswahl]

st.dataframe(favoriten, use_container_width=True)