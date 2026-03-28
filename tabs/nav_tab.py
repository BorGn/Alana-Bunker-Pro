import streamlit as st
import os

def render():
    st.header("📂 Prometeus Cibernético")
    
    # Campo de texto responsivo (Lê o que está no estado e permite edição)
    caminho = st.text_input("Explorar Caminho:", value=st.session_state.get('caminho_atual', 'C:\\'))
    
    # Valida se o caminho existe
    if os.path.exists(caminho):
        st.session_state.caminho_atual = caminho
        
        try:
            # Lista pastas e arquivos
            itens = os.listdir(caminho)
            pastas = [f for f in itens if os.path.isdir(os.path.join(caminho, f))]
            arquivos = [f for f in itens if os.path.isfile(f)]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📁 Diretorios")
                for p in pastas:
                    if st.button(f"➡️ {p}", key=f"dir_{p}"):
                        st.session_state.caminho_atual = os.path.join(caminho, p)
                        st.rerun()
            
            with col2:
                st.subheader("📄 Arquivos")
                for arq in arquivos:
                    st.text(f"📄 {arq}")
                    
        except Exception as e:
            st.error(f"Erro de Acesso: {e}")
    else:
        st.error("Caminho não encontrado ou inacessível.")