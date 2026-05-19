import streamlit as st

def show_help(title="Hilfe", text_lines=None):
    if text_lines is None:
        text_lines = [
            "Wähle eine Kategorie, gib die Werte ein und klicke auf Umrechnen.",
            "- Flüssigkeiten in Gewicht: Volumen → Masse",
            "- Gewicht in Flüssigkeit: Masse → Volumen",
            "- Gewicht in Gewicht: Gewichtseinheiten umrechnen",
            "- Flüssigkeit in Flüssigkeit: Volumeneinheiten umrechnen",
            "Du kommst immer noch nicht weiter? Dann gehts dir wie uns, also frag doch einfach ChatGPT! :)",
            "[Frag ChatGPT!](https://chat.openai.com)"
        ]

    if "help_modal_open" not in st.session_state:
        st.session_state.help_modal_open = False

    if st.button("Hilfe", key="help_button"):
        st.session_state.help_modal_open = True

    if st.session_state.help_modal_open:
        if hasattr(st, "modal"):
            with st.modal(title):
                st.markdown(f"### {title}")
                for line in text_lines:
                    if line.startswith("- ") or line.startswith("["):
                        st.markdown(line)
                    else:
                        st.write(line)
                if st.button("Schließen", key="close_help"):
                    st.session_state.help_modal_open = False
        else:
            with st.expander(title, expanded=True):
                st.markdown(f"### {title}")
                for line in text_lines:
                    if line.startswith("- ") or line.startswith("["):
                        st.markdown(line)
                    else:
                        st.write(line)
                if st.button("Schließen", key="close_help"):
                    st.session_state.help_modal_open = False



# ... bestehende show_help() Funktion ...

def show_navigation(current_page=None):
    st.markdown("""
    <style>
    .nav-button-container {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    .nav-button-container button {
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-button-container">', unsafe_allow_html=True)

    if st.button("Nav", key="nav_button"):
        st.session_state.nav_modal_open = True

    st.markdown('</div>', unsafe_allow_html=True)

    if "nav_modal_open" not in st.session_state:
        st.session_state.nav_modal_open = False

    if st.session_state.nav_modal_open:
        pages = {
            "Einheitenumrechner": "views/Einheitenumrechner.py",
            "Titer": "views/Titer.py",
            "Konzentrationsrechner": "views/Konzentrationsrechner.py",
            "Molare Masse Rechner": "views/Molaremasserechner.py",
            "pH-Werte Rechner": "views/pH_Werte_Rechner.py",
            "Verdünnungsrechner": "views/Verdünnungsrechner.py",
            "Favoriten": "views/Favoritenliste.py",
            "Zur Startseite": "views/home.py"
        }

        if hasattr(st, "modal"):
            with st.modal("Navigation"):
                st.markdown("### Wähle eine Unterseite")
                for name, path in pages.items():
                    if name != current_page:
                        if st.button(name, key=f"nav_{name}"):
                            st.switch_page(path)
                if st.button("Schließen", key="close_nav"):
                    st.session_state.nav_modal_open = False
        else:
            with st.expander("Navigation", expanded=True):
                st.markdown("### Wähle eine Unterseite")
                for name, path in pages.items():
                    if name != current_page:
                        if st.button(name, key=f"nav_{name}"):
                            st.switch_page(path)
                if st.button("Schließen", key="close_nav"):
                    st.session_state.nav_modal_open = False