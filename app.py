import pandas as pd
import streamlit as st
from datetime import date

# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager


data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="App"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in
# --- END OF NEW CODE ---

# --- CODE UPDATE: load user data from data manager if not already present in session state --

#  ph-Rechner 
if 'resultate_ph_rechner' not in st.session_state:
    history = data_manager.load_user_data('ph_rechner_history.json', initial_value=[])
    df = pd.DataFrame(history)
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
    # Falls leer, sicherstellen, dass die erwarteten Spalten vorhanden sind
        df = pd.DataFrame(columns=[
        "timestamp", "Typ", "Konzentration (mol/L)", "pH", "Kategorie", "favorite"
        ])
    st.session_state['resultate_ph_rechner'] = df

# Molare Masse-Rechner
if 'resultate_molare_masse_rechner' not in st.session_state:
    history = data_manager.load_user_data('molare_masse_rechner_history.json', initial_value=[])
    df = pd.DataFrame(history)
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
    # Falls leer, sicherstellen, dass die erwarteten Spalten vorhanden sind
        df = pd.DataFrame(columns=[
        "timestamp", "Molekül", "Molare Masse (g/mol)", "favorite"
        ])
    st.session_state['resultate_molare_masse_rechner'] = df

# --- END OF CODE UPDATE ---
# Verdünnungsrechner
if 'resultate_verdünnungs_rechner' not in st.session_state:
    history = data_manager.load_user_data('verduennungs_history.json', initial_value=[])
    df = pd.DataFrame(history)
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
    # Falls leer, sicherstellen, dass die erwarteten Spalten vorhanden sind
        df = pd.DataFrame(columns=[
            "timestamp", "C1", "C2", "V2", "V1", "favorite"
        ])
    st.session_state['resultate_verdünnungs_rechner'] = df

# --- Bis hier hin ist Historie bereits eingefügt ---
# Titer-Rechner
if 'resultate_titer_rechner' not in st.session_state:
    history = data_manager.load_user_data('titer_history.json', initial_value=[])
    df = pd.DataFrame(history)
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
    # Falls leer, sicherstellen, dass die erwarteten Spalten vorhanden sind
        df = pd.DataFrame(columns=[
            "timestamp", "c_soll", "c_eff", "titer"
        ])
    st.session_state['resultate_titer_rechner'] = df

# Konzentrationsrechner
if 'resultate_konzentrations_rechner' not in st.session_state:
    history = data_manager.load_user_data('konzentrations_history.json', initial_value=[])
    df = pd.DataFrame(history)
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
    # Falls leer, sicherstellen, dass die erwarteten Spalten vorhanden sind
        df = pd.DataFrame(columns=[
            "timestamp", "Menge (g)", "Molmasse (g/mol)", "Volumen (L)", "Konzentration (mol/L)"
        ])
    st.session_state['resultate_konzentrations_rechner'] = df


# Einheitenumrechner
if 'resultate_einheitenumrechner' not in st.session_state:
    history = data_manager.load_user_data('einheitenumrechner_history.json', initial_value=[])
    df = pd.DataFrame(history)
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
    # Falls leer, sicherstellen, dass die erwarteten Spalten vorhanden sind
        df = pd.DataFrame(columns=[
            "timestamp", "Wert", "Von Einheit", "Zu Einheit", "Ergebnis"
        ])
    st.session_state['resultate_einheitenumrechner'] = df

pg_home = st.Page("views/home.py", title="Startseite", icon=":material/home:", default=True)
pg_second = st.Page("views/Einleitung.py", title="Einleitung", icon=":material/menu_book:")
pg_third = st.Page("views/Favoritenliste.py", title="Favoriten", icon=":material/star:")
pg_fourth = st.Page("views/PSE.py", title="Periodensystem", icon=":material/info:")
pg_fifth = st.Page("views/Einheitenumrechner.py", title="Einheitenumrechner", icon=":material/info:")
pg_sixth = st.Page("views/Konzentrationsrechner.py", title="Konzentrationsrechner", icon=":material/info:")
pg_seventh = st.Page("views/Molaremassenrechner.py", title="Molare Massen Rechner", icon=":material/info:")
pg_eighth = st.Page("views/pH_Werte_Rechner.py", title="pH-Rechner", icon=":material/info:")
pg_ninth = st.Page("views/Titer.py", title="Titer-Rechner", icon=":material/info:")
pg_tenth = st.Page("views/Verdünnungsrechner.py", title="Verdünnungsrechner", icon=":material/info:")
pg_eleventh = st.Page("views/Einstellungen.py", title="Einstellungen", icon=":material/settings:")

pg = st.navigation([pg_home, pg_second, pg_third, pg_fourth, pg_fifth, pg_sixth, pg_seventh, pg_eighth, pg_ninth, pg_tenth, pg_eleventh])
pg.run()




