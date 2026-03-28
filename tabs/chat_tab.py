import streamlit as st

def render():
    st.subheader("💬 Célula de Diálogo Alana")
    prompt = st.chat_input("Discutir arquitetura ou arquivos...")
    if prompt:
        st.write(f"**Operador:** {prompt}")
        st.markdown(f"**Alana:** Analisando contexto em `{st.session_state.dir_atual}`...")
