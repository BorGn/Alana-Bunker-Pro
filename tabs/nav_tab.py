import streamlit as st
import os

def render():
    st.header("📂 Navegação de Arquivos")
    st.info("Diretório atual: C:\\Alana")

    # Lista arquivos na raiz, ignorando pastas de sistema como .git
    arquivos = [f for f in os.listdir('.') if os.path.isfile(f) and not f.startswith('.')]
    
    if arquivos:
        arquivo_selecionado = st.selectbox("Selecione um arquivo para inspeção rápida:", arquivos)
        
        if st.button("Ler Conteúdo"):
            try:
                with open(arquivo_selecionado, "r", encoding="utf-8") as f:
                    conteúdo = f.read()
                st.code(conteúdo, language="python" if arquivo_selecionado.endswith(".py") else "markdown")
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")
    else:
        st.warning("Nenhum arquivo encontrado na raiz.")