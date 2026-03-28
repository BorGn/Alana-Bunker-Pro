import streamlit as st

def render():
    st.header("🛠️ Administração do Bunker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Estado do Sistema")
        st.write(f"Modelo Ativo: {st.session_state.get('alana_model', 'Não definido')}")
        if st.button("Reiniciar Memória (Chat)"):
            st.session_state.messages = []
            st.rerun()

    with col2:
        st.subheader("Diretrizes da Alana")
        # Aqui ele lê o coração do projeto
        try:
            with open("alana_core.txt", "r", encoding="utf-8") as f:
                core_content = f.read()
            st.text_area("Coração (alana_core.txt):", value=core_content, height=200)
        except Exception as e:
            st.error("Não foi possível carregar o alana_core.txt")