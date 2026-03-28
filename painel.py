import streamlit as st

# Importa configuração e estado
from core.config import setup_page
from core.state import init_state

# Importa a barra lateral
import sidebar

# Importa as abas
# No painel.py, substitua as linhas 11-14 por:
from tabs import nav_tab    # Se o arquivo for nav_tab.py
from tabs import chat_tab   # Se o arquivo for chat_tab.py
from tabs import bra_tab    # Se o arquivo for bra_tab.py
from tabs import ent_tab    # Se o arquivo for ent_tab.py

# Inicialização da página
setup_page()
init_state()

# Renderiza a sidebar
sidebar.render()

# Controle de abas
aba = st.tabs(["📂 Navegação", "💬 Chat", "🛠️ Administração", "🧬 Entropia"])

with aba[0]:
    nav_tab.render()

with aba[1]:
    chat_tab.render()

with aba[2]:
    bra_tab.render()

with aba[3]:
    ent_tab.render()
