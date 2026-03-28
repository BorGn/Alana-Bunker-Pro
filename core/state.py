import os
import streamlit as st

def init_state():
    if 'dir_atual' not in st.session_state:
        st.session_state.dir_atual = os.path.normpath(os.getcwd())
    if 'arquivo_foco' not in st.session_state:
        st.session_state.arquivo_foco = None
    if 'mapa_recursivo' not in st.session_state:
        st.session_state.mapa_recursivo = None

