import streamlit as st
import pandas as pd
from views.Hilfefenster import show_help, show_navigation

show_navigation(current_page="Favoritenliste")
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
if "rechner" not in favoriten.columns:
    favoriten["rechner"] = "Unbekannt"

if favoriten.empty:
    st.info("Noch keine Favoriten markiert.")
    st.stop()

# 🔽 Filter nach Rechner
rechner_liste = ["Alle"] + sorted(
    favoriten["rechner"]
    .dropna()
    .astype(str)
    .unique()
)
auswahl = st.selectbox("Rechner filtern", rechner_liste)

if auswahl != "Alle":
    favoriten = favoriten[favoriten["rechner"] == auswahl]

# 🔽 nur sinnvolle Spalten behalten (nicht nur komplett leere)
anzeigen_df = favoriten.copy()

# Spalten entfernen, wenn ALLE Werte None/NaN sind
anzeigen_df = anzeigen_df.dropna(axis=1, how="all")

st.dataframe(
    anzeigen_df,
    use_container_width=True,
    hide_index=True,
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zu den Favoriten", 
              text_lines=[
                  "Hier siehst du alle Berechnungen, die du als Favorit markiert hast.",
                  "Du kannst nach Rechner filtern, um z.B. nur deine gewählten Titer-Berechnungen zu sehen.",
                  "Die Daten werden automatisch synchronisiert, wenn du neue Favoriten in den Rechnern markierst.",
                  "Willst du einen Favoriten entfernen, gehe zurück zum entsprechenden Rechner und deaktiviere die Checkbox.",
                  "Du kommst immer noch nicht weiter? Dann gehts dir wie uns, also frag doch einfach ChatGPT! :)",
                    "[Frag ChatGPT!](https://chat.openai.com)"
                ])