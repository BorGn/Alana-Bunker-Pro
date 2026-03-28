import streamlit as st

def init_state():
    """Inicializa as variáveis de estado global do Bunker."""
    
    # Histórico do Chat (Fundamental para a aba chat_tab)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Configurações da Alana (Selecionadas no sidebar)
    if "alana_model" not in st.session_state:
        st.session_state.alana_model = "Analista Técnica"

    # Controle de Autenticação/Status
    if "bunker_unlocked" not in st.session_state:
        st.session_state.bunker_unlocked = False

    # Diretrizes do Core (Cache para não ler o TXT toda hora)
    if "core_rules" not in st.session_state:
        st.session_state.core_rules = ""