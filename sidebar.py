import streamlit as st
import streamlit.components.v1 as components
import pathlib
from core.functions import detectar_drives

# Caminho do avatar relativo a este arquivo
_AVATAR_PATH = pathlib.Path(__file__).parent / "avatar.html"

def render_avatar(state=None):
    """Injeta o avatar HTML e sincroniza o estado. Se state for fornecido, atualiza o session_state."""
    if state:
        st.session_state.ai_state = state

    avatar_html = _AVATAR_PATH.read_text(encoding="utf-8")
    curr_state = st.session_state.get("ai_state", "idle")

    # Script de sincronia robusto: envia postMessage para si mesmo dentro do iframe
    sync_script = f"""
    <script>
      (function() {{
        const s = '{curr_state}';
        const msg = {{ type: 'set_state', state: s }};
        window.postMessage(msg, '*');
        // Garantia para carregamento lento
        setTimeout(() => window.postMessage(msg, '*'), 100);
        setTimeout(() => window.postMessage(msg, '*'), 500);
      }})();
    </script>
    """

    components.html(
        avatar_html + sync_script,
        height=300,
        scrolling=False,
    )

def update_state(state):
    """Força a atualização visual do avatar se o placeholder estiver disponível."""
    st.session_state.ai_state = state
    if "avatar_placeholder" in st.session_state:
        with st.session_state.avatar_placeholder:
            render_avatar(state)

def render():
    with st.sidebar:
        # ── Avatar Dinâmico ─────────────────────────────
        # Criamos um placeholder que pode ser acessado por outros módulos
        st.session_state.avatar_placeholder = st.empty()
        with st.session_state.avatar_placeholder:
            render_avatar()

        # ── Título e Unidades ───────────────────────────
        st.title("🛡️ Alana Bunker")
        st.divider()

        # Detecção dinâmica de drives (Hardening de Hardware)
        unidades = detectar_drives()
        if not unidades:
            unidades = ["C:\\"]

        def mudar_drive():
            st.session_state.caminho_atual = st.session_state.drive_selector

        st.selectbox(
            "⚓ Selecionar Unidade:",
            unidades,
            index=0 if st.session_state.get("drive_selector") not in unidades else unidades.index(st.session_state.drive_selector),
            key="drive_selector",
            on_change=mudar_drive
        )