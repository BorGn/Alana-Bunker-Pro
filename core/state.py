import streamlit as st
from core.functions import detectar_drives

def update_state(state):
    """Garante que a função tenha corpo para não quebrar a compilação."""
    st.session_state.ai_state = state

def render_sidebar():
    """Esta função PRECISA estar no nível 0 de indentação."""
    with st.sidebar:
        st.title("🛡️ Alana Bunker")
def init_state():
    """Inicializa as variáveis de estado global do Bunker."""
    
    # --- Mantendo seu código original ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "alana_model" not in st.session_state:
        st.session_state.alana_model = "Analista Técnica"
    if "bunker_unlocked" not in st.session_state:
        st.session_state.bunker_unlocked = False
    if "core_rules" not in st.session_state:
        st.session_state.core_rules = ""

    # --- INJETANDO SEGURANÇA DE HARDWARE ---
    if "hardware_busy" not in st.session_state:
        st.session_state.hardware_busy = False
    if "cleaning_vram" not in st.session_state:
        st.session_state.cleaning_vram = False
    if "current_pid" not in st.session_state:
        st.session_state.current_pid = None
    if "ai_state" not in st.session_state:
        st.session_state.ai_state = "idle"