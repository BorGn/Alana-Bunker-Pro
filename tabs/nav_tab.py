import streamlit as st
import os

def render():
    st.header("📂 Prometeus Cibernético")
    
    # 1. Garantia de Estado
    if "caminho_atual" not in st.session_state:
        st.session_state.caminho_atual = "C:\\"

    # 2. Input de Caminho (Sincronizado)
    caminho_input = st.text_input("Explorar Caminho:", value=st.session_state.caminho_atual)

    # 3. Se o usuário digitar manualmente, atualiza o GPS
    if caminho_input != st.session_state.caminho_atual:
        if os.path.exists(caminho_input):
            st.session_state.caminho_atual = caminho_input
            st.rerun()

    caminho = st.session_state.caminho_atual

    # 4. Verificação de Integridade do Diretório
    if os.path.exists(caminho) and os.path.isdir(caminho):
        try:
            # Normaliza o caminho para evitar barras duplas ou faltantes
            caminho_norm = os.path.abspath(caminho)
            itens = sorted(os.listdir(caminho_norm))
            
            # Separação com verificação robusta
            pastas = []
            arquivos = []
            
            for item in itens:
                full_path = os.path.join(caminho_norm, item)
                if os.path.isdir(full_path):
                    pastas.append(item)
                else:
                    arquivos.append(item)

            st.success(f"📍 Explorando: {caminho_norm}")

            # Botão de Voltar (Subir nível)
            parent_dir = os.path.dirname(caminho_norm)
            if caminho_norm != parent_dir: # Se não for a raiz do disco
                if st.button("⬅️ Subir um Nível"):
                    st.session_state.caminho_atual = parent_dir
                    st.rerun()

            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"📁 Pastas ({len(pastas)})")
                for p in pastas:
                    # Chave única baseada no caminho completo para evitar conflitos
                    if st.button(f"➡️ {p}", key=f"dir_{os.path.join(caminho_norm, p)}"):
                        st.session_state.caminho_atual = os.path.join(caminho_norm, p)
                        st.rerun()
            
            with col2:
                st.subheader(f"📄 Arquivos ({len(arquivos)})")
                if arquivos:
                    for arq in arquivos:
                        # Exibe o arquivo e um botão de ação rápida opcional
                        st.text(f"📄 {arq}")
                else:
                    st.write("⚠️ Nenhum arquivo visível aqui.")

        except Exception as e:
            st.error(f"🚫 Erro ao acessar: {e}")
    else:
        st.error("❌ Diretório não encontrado.")