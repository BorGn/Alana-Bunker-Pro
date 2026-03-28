import streamlit as st

def render():
    with st.sidebar:
        st.title("🛡️ Alana Bunker")
        st.divider()
        
        # Lista de drives incluindo o F:
        unidades = ["C:\\", "D:\\", "E:\\", "F:\\"]
        
        # O segredo: On_change garante que a troca de disco limpe o GPS antigo
        def mudar_drive():
            st.session_state.caminho_atual = st.session_state.drive_selector

        st.selectbox(
            "⚓ Selecionar Unidade:", 
            unidades, 
            key="drive_selector",
            on_change=mudar_drive
        )