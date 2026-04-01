import streamlit as st
import os
from core.functions import obter_tamanho_formatado, obter_telemetria_visual, mapear_recursivo

def render():
    st.header("📂 Prometeus Cibernético")

    # Inicialização segura do GPS
    if "caminho_atual" not in st.session_state:
        st.session_state.caminho_atual = st.session_state.get("drive_selector", "C:\\")

    # Input manual de caminho
    caminho_input = st.text_input("📍 Explorar Caminho:", value=st.session_state.caminho_atual)

    if caminho_input != st.session_state.caminho_atual:
        if os.path.exists(caminho_input):
            st.session_state.caminho_atual = caminho_input
            st.rerun()

    caminho = st.session_state.caminho_atual

    # Modo de exibição: navegação ou varredura
    modo = st.radio("Modo:", ["🗂️ Navegação", "🔍 Varredura Recursiva"], horizontal=True)

    st.divider()

    # ── MODO VARREDURA ──────────────────────────────────────────────
    if modo == "🔍 Varredura Recursiva":
        profundidade = st.slider("Profundidade máxima", min_value=1, max_value=5, value=3)
        if st.button("🚀 Iniciar Varredura"):
            with st.spinner("Varrendo..."):
                resultado = mapear_recursivo(caminho, profundidade=profundidade)
            st.code(resultado, language="")
        return

    # ── MODO NAVEGAÇÃO ──────────────────────────────────────────────
    try:
        caminho_norm = os.path.normpath(caminho)
        itens = sorted(os.listdir(caminho_norm))

        pastas   = [i for i in itens if os.path.isdir(os.path.join(caminho_norm, i))]
        arquivos = [i for i in itens if os.path.isfile(os.path.join(caminho_norm, i))]

        st.success(f"Navegando em: {caminho_norm}")

        # Botão voltar
        pai = os.path.dirname(caminho_norm)
        if pai != caminho_norm:
            if st.button("⬅️ Voltar"):
                st.session_state.caminho_atual = pai
                st.rerun()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"📁 Pastas ({len(pastas)})")
            for p in pastas:
                if st.button(f"➡️ {p}", key=f"btn_{p}_{caminho_norm}"):
                    st.session_state.caminho_atual = os.path.join(caminho_norm, p)
                    st.rerun()

        with col2:
            st.subheader(f"📄 Arquivos ({len(arquivos)})")
            for f in arquivos:
                caminho_arq = os.path.join(caminho_norm, f)
                cor, status = obter_telemetria_visual(f)
                tamanho     = obter_tamanho_formatado(caminho_arq)
                st.markdown(
                    f":{cor}[**{status}**] &nbsp; `{f}` &nbsp; <sub>{tamanho}</sub>",
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"Erro de acesso ao diretório: {e}")