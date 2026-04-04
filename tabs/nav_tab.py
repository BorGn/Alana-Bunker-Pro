import streamlit as st
import os

def render():
    st.header("📂 Navegador de Arquivos")

    # --- NOVO SELETOR DE UNIDADES (CENTRALIZADO) ---
    unidades = ["C:\\", "D:\\", "E:\\", "G:\\"] # Lista manual para garantir visibilidade
    
    col1, col2 = st.columns([1, 2])
    with col1:
        unidade_escolhida = st.selectbox(
            "💽 Selecionar Unidade:",
            unidades,
            key="nav_drive_selector"
        )

    # Se a unidade mudar, reseta o caminho_atual para a raiz dela
    if unidade_escolhida != st.session_state.get("caminho_atual", "")[:3]:
        st.session_state.caminho_atual = unidade_escolhida
        st.rerun()

    st.divider()

    # 1. Âncora de Estado (Mantido)
    caminho_atual = st.session_state.get("caminho_atual", "C:\\")
    # ... resto do código original

    # 2. Blindagem de Permissão e Listagem
    try:
        conteudo = os.listdir(caminho_atual)
        st.caption(f"📍 Explorando: **{caminho_atual}**")

        # 3. Renderização de Itens
        for item in conteudo:
            caminho_full = os.path.join(caminho_atual, item)
            
            if os.path.isdir(caminho_full):
                # Entrada em pastas com Rerun obrigatório
                if st.button(f"📁 {item}", key=f"nav_{item}", use_container_width=True):
                    st.session_state.caminho_atual = caminho_full
                    st.rerun() # Regra de Ouro: Rerun na entrada
            else:
                st.text(f"📄 {item}")

    except PermissionError:
        st.error(f"🚫 **Acesso Negado:** O drive ou pasta {caminho_atual} está protegido.")
        if st.button("🔄 Voltar para a Raiz"):
            st.session_state.caminho_atual = "C:\\"
            st.rerun()

    except FileNotFoundError:
        st.warning("⚠️ Caminho não localizado. Sincronizando com a raiz...")
        st.session_state.caminho_atual = "C:\\"
        st.rerun()