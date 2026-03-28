import streamlit as st
from core.config import setup_page
from core.state import init_state
import sidebar

# Importação correta conforme a pasta /tabs do seu GitHub
from tabs import nav_tab
from tabs import chat_tab
from tabs import bra_tab
from tabs import ent_tab

# 1. Inicialização
setup_page()
init_state()

# 2. Renderiza a Sidebar (Integrada ao Painel)
sidebar.render()

# 3. Controle de Abas
aba = st.tabs(["📂 Navegação", "💬 Chat", "🛠️ Administração", "🧬 Entropia"])

with aba[0]:
    nav_tab.render()

with aba[1]:
    chat_tab.render()

with aba[2]:
    bra_tab.render()

with aba[3]:
    ent_tab.render()