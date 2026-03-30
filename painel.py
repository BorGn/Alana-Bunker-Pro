import streamlit as st
from core.config import setup_page
from core.state import init_state
import sidebar
from core import functions
from tabs import nav_tab
from tabs import chat_tab
from tabs import bra_tab
from tabs import ent_tab

# 1. Inicialização
setup_page()
init_state()

# 2. Garante que ai_state existe (caso init_state não cubra)
if "ai_state" not in st.session_state:
    st.session_state.ai_state = "idle"

# 3. Renderiza a Sidebar (com avatar)
sidebar.render()

# 4. Controle de Abas
aba = st.tabs(["📂 Navegação", "💬 Chat", "🛠️ Administração", "🧬 Entropia"])

with aba[0]:
    nav_tab.render()

with aba[1]:
    chat_tab.render()

with aba[2]:
    bra_tab.render()

with aba[3]:
    ent_tab.render()
