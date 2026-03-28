import streamlit as st

def render():
    with st.sidebar:
        st.title("🛡️ Alana Bunker")
        st.divider()
        
        # Exemplo de controle global que as abas vão usar
        st.subheader("Configurações de IA")
        modelo = st.selectbox(
            "Selecione a Personalidade:",
            ["Analista Técnica", "Desenvolvedora", "Segurança Cibernética"],
            key="alana_model" # Isso salva no session_state automaticamente
        )
        
        st.divider()
        st.info("Status: Bunker Operacional")