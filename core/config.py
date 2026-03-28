import streamlit as st

def setup_page():
    """Configuração centralizada da interface do Bunker."""
    st.set_page_config(
        page_title="Alana Bunker Pro v1.0",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )