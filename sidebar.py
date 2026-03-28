import streamlit as st
import os

def render():
    with st.sidebar:
        st.title("🛡️ Alana Bunker")
        st.divider()
        
        # Seletor de Unidade (O que estava no sidebar e sumiu)
        unidades = ["C:\\", "D:\\", "E:\\"]
        drive_padrao = unidades.index("C:\\") if "C:\\" in unidades else 0
        
        escolha_drive = st.selectbox("⚓ Selecionar Unidade:", unidades, index=drive_padrao)
        
        # Atualiza o estado global para a aba de navegação usar
        if "caminho_atual" not in st.session_state or st.sidebar.button("Resetar para Raiz"):
            st.session_state.caminho_atual = escolha_drive
            
        st.divider()
        st.info(f"📍 GPS: {st.session_state.caminho_atual}")