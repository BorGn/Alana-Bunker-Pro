import streamlit as st
import os

def render():
    st.header("📂 Prometeus Cibernético")
    
    # Inicialização segura do GPS
    if "caminho_atual" not in st.session_state:
        st.session_state.caminho_atual = st.session_state.get("drive_selector", "C:\\")

    # Input manual - Se o usuário der ENTER, ele navega
    caminho_input = st.text_input("📍 Explorar Caminho:", value=st.session_state.caminho_atual)
    
    if caminho_input != st.session_state.caminho_atual:
        if os.path.exists(caminho_input):
            st.session_state.caminho_atual = caminho_input
            st.rerun()

    caminho = st.session_state.caminho_atual

    try:
        # Normalização de caminho para Windows
        caminho_norm = os.path.normpath(caminho)
        itens = sorted(os.listdir(caminho_norm))
        
        pastas = [i for i in itens if os.path.isdir(os.path.join(caminho_norm, i))]
        arquivos = [i for i in itens if os.path.isfile(os.path.join(caminho_norm, i))]

        st.success(f"Navegando em: {caminho_norm}")

        # Botão para subir de nível
        pai = os.path.dirname(caminho_norm)
        if pai != caminho_norm:
            if st.button("⬅️ Voltar"):
                st.session_state.caminho_atual = pai
                st.rerun()

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"📁 Pastas ({len(pastas)})")
            for p in pastas:
                # O Clique aqui agora é mandatório
                if st.button(f"➡️ {p}", key=f"btn_{p}_{caminho_norm}"):
                    st.session_state.caminho_atual = os.path.join(caminho_norm, p)
                    st.rerun()

        with col2:
            st.subheader(f"📄 Arquivos ({len(arquivos)})")
            for f in arquivos:
                st.text(f"📄 {f}")

    except Exception as e:
        st.error(f"Erro de acesso ao diretório: {e}")