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
if 'resultate_ph_rechner' not in st.session_state:
    st.session_state['resultate_ph_rechner'] = data_manager.load_user_data(
        'ph_rechner.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---
# --- CODE UPDATE: load user data from data manager if not already present in session state --
if 'resultate_mm_rechner' not in st.session_state:
    st.session_state['resultate_mm_rechner'] = data_manager.load_user_data(
        'mm_rechner.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---


pg_home = st.Page("views/home.py", title="Startseite", icon=":material/home:", default=True)
pg_second = st.Page("views/Einleitung.py", title="Einleitung", icon=":material/info:")
pg_third = st.Page("views/PSE.py", title="Periodensystem", icon=":material/info:")
pg_fourth = st.Page("views/Einheitenumrechner.py", title="Einheitenumrechner", icon=":material/info:")
pg_fifth = st.Page("views/Konzentrationsrechner.py", title="Konzentrationsrechner", icon=":material/info:")
pg_sixth = st.Page("views/Molaremasserechner.py", title="Molare Massen Rechner", icon=":material/info:")
pg_seventh = st.Page("views/pH_Werte_Rechner.py", title="pH-Rechner", icon=":material/info:")
pg_eighth = st.Page("views/Titer.py", title="Titer-Rechner", icon=":material/info:")
pg_ninth = st.Page("views/Verdünngsrechner.py", title="Verdünngsrechner", icon=":material/info:")
pg_tenth = st.Page("views/Einstellungen.py", title="Einstellungen", icon=":material/settings:")

pg = st.navigation([pg_home, pg_second, pg_third, pg_fourth, pg_fifth, pg_sixth, pg_seventh, pg_eighth, pg_ninth, pg_tenth])
pg.run()




