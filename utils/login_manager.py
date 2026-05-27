import secrets
import streamlit as st
import streamlit_authenticator as stauth
from utils.data_manager import DataManager
import re
import bcrypt


class LoginManager:
    """
    Singleton class that manages user authentication for the application.

    Handles user login, registration, and session management using
    streamlit-authenticator. Credentials are stored in a YAML file via
    the DataManager.
    """

    def __new__(cls, *args, **kwargs):
        """
        Singleton: returns existing instance from session state if available.

        Returns:
            LoginManager: The singleton instance, either existing or newly created.
        """
        if 'login_manager' in st.session_state:
            return st.session_state.login_manager
        instance = super(LoginManager, cls).__new__(cls)
        st.session_state.login_manager = instance
        return instance

    def __init__(self, data_manager: DataManager = None,
                 auth_credentials_file: str = 'credentials.yaml',
                 auth_cookie_name: str = 'bmld_inf2_streamlit_app'):
        """
        Initializes authentication components if not already initialized.

        Args:
            data_manager (DataManager): The DataManager instance to use for credential storage.
            auth_credentials_file (str): Filename for storing user credentials.
            auth_cookie_name (str): Cookie name for session management.
        """
        if hasattr(self, 'authenticator'):
            return
        if data_manager is None:
            return

        self.data_manager = data_manager
        self.auth_credentials_file = auth_credentials_file
        self.auth_cookie_name = auth_cookie_name
        self.auth_cookie_key = secrets.token_urlsafe(32)
        self.auth_credentials = self._load_auth_credentials()
        self.authenticator = stauth.Authenticate(
            self.auth_credentials, self.auth_cookie_name, self.auth_cookie_key
        )

    def _save_auth_credentials(self):
        self.auth_credentials = self._normalize_auth_credentials(self.auth_credentials)
        self.data_manager.save_app_data(self.auth_credentials, self.auth_credentials_file)
    
    def _normalize_auth_credentials(self, auth_credentials):
        if auth_credentials is None:
            return {"usernames": {}}
        if "usernames" in auth_credentials:
            return auth_credentials
        if "credentials" in auth_credentials and isinstance(auth_credentials["credentials"], dict):
            return {"usernames": auth_credentials["credentials"].get("usernames", {})}
        return {"usernames": {}}
    
    def login_register(self, login_title='Login', register_title='Register new user'):
        """
        Handles authentication. When not logged in, shows the login/register page
        and stops further execution. When logged in, adds the logout button to the
        sidebar and returns, allowing app.py to set up its own navigation.

        Args:
            login_title (str): Label for the login tab.
            register_title (str): Label for the registration tab.
        """
        if st.session_state.get("authentication_status") is True:
            with st.sidebar:
                st.write(f"Angemeldet als: **{st.session_state.get('name')}**")
                self.authenticator.logout()
        else:
            page_fn = lambda: self._login_register_page(login_title, register_title)
            pg = st.navigation([st.Page(page_fn, title="Login", icon=":material/login:")])
            pg.run()
            st.stop()

    def _login_register_page(self, login_title, register_title):
        """Page function shown when the user is not authenticated."""
        login_tab, register_tab = st.tabs((login_title, register_title))
        with login_tab:
            self._login()
        with register_tab:
            self._register()

    def _login(self):
        """Renders the login form and handles authentication status messages."""
        self.authenticator.login()
        if st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")
        else:
            st.warning("Please enter your username and password")

    def _register(self):
        """
        Renders the registration form and handles user registration flow.

        Displays password requirements, processes registration attempts,
        and saves credentials on successful registration.
        """
        st.info("""
        The password must be 8-20 characters long and include at least one uppercase letter,
        one lowercase letter, one digit, and one special character from @$!%*?&.
        """)
        res = self.authenticator.register_user()
        if res[1] is not None:
            st.success(f"User {res[1]} registered successfully")
            self.auth_credentials = self._normalize_auth_credentials(self.auth_credentials)
            try:
                self._save_auth_credentials()
                st.success("Credentials saved successfully")
            except Exception as e:
                st.error(f"Failed to save credentials: {e}")

    def change_password(self, username: str, current_password: str, new_password: str) -> tuple[bool, str]:
        # DEBUG: Ausgeben, was wir erhalten
        print(f"DEBUG: username = {username}")
        print(f"DEBUG: auth_credentials keys = {self.auth_credentials.keys()}")
        print(f"DEBUG: full auth_credentials = {self.auth_credentials}")
        
        if not username:
            return False, "Nicht eingeloggt"

        usernames = self.auth_credentials.get('usernames', {})
        print(f"DEBUG: usernames = {usernames}")
        print(f"DEBUG: usernames.keys() = {list(usernames.keys())}")
    
        if username not in usernames:
            return False, "Benutzer nicht gefunden"

        user_creds = usernames[username]
        stored_hash = user_creds.get('password')
        if stored_hash is None:
            return False, "Kein gespeichertes Passwort gefunden"

        # Prüfen aktuelles Passwort (bcrypt)
        try:
            if not bcrypt.checkpw(current_password.encode(), stored_hash.encode()):
                return False, "Aktuelles Passwort ist falsch"
        except Exception as e:
            return False, f"Fehler bei Passwortüberprüfung: {e}"

        # Neues Passwort validieren
        if not validate_password(new_password):
            return False, ("Passwort muss 8-20 Zeichen lang sein und enthalten: "
                           "Grossbuchstaben, Kleinbuchstaben, Zahl und Sonderzeichen (@$!%*?&)")

        # Neues Passwort hashen
        try:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        except Exception as e:
            return False, f"Fehler beim Hashen des Passworts: {e}"

        # Passwort aktualisieren und speichern
        self.auth_credentials['usernames'][username]['password'] = hashed_password
        self._save_auth_credentials()
        return True, "Passwort erfolgreich geändert"
    
    def _normalize_auth_credentials(self, auth_credentials):
        if auth_credentials is None:
            return {"usernames": {}}
        if "usernames" in auth_credentials:
            return auth_credentials
        if "credentials" in auth_credentials and isinstance(auth_credentials["credentials"], dict):
            return {"usernames": auth_credentials["credentials"].get("usernames", {})}
        return {"usernames": {}}

    def _load_auth_credentials(self):
        auth_credentials = self.data_manager.load_app_data(
            self.auth_credentials_file,
            initial_value={"usernames": {}}
        )
        return self._normalize_auth_credentials(auth_credentials)

def validate_password(password):
    """
    Passwortregeln:
    - mindestens 8 Zeichen
    - mindestens 1 Grossbuchstabe
    - mindestens 1 Kleinbuchstabe
    - mindestens 1 Zahl
    """
    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True