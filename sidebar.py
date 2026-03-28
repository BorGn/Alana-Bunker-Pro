import streamlit as st

def render():
    with st.sidebar:
        st.title("🛡️ Alana Bunker")
        st.divider()
        
        unidades = ["C:\\", "D:\\", "E:\\"]
        
        # O segredo é a 'key'. Ela vincula o selectbox diretamente ao session_state
        if "escolha_drive" not in st.session_state:
            st.session_state.escolha_drive = "C:\\"

        drive = st.selectbox(
            "⚓ Selecionar Unidade:", 
            unidades, 
            key="drive_selector"
        )

        # Se o drive selecionado for diferente do caminho atual, nós resetamos o GPS
        if st.session_state.drive_selector != st.session_state.get('caminho_atual', ''):
            st.session_state.caminho_atual = st.session_state.drive_selector
            # O st.rerun() aqui é opcional, mas ajuda a sincronizar na hora