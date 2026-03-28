import streamlit as st

def render():
    st.subheader("🦾 Comando Open Interpreter (Admin)")
    tarefa = st.text_area("Ordem direta para o hardware:")
    if st.button("Executar via Janela Azul"):
        st.success("✅ Janela Admin disparada.")
