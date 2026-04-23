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