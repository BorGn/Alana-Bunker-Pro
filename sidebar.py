import streamlit as st
import streamlit.components.v1 as components
import pathlib

# Caminho do avatar relativo a este arquivo
_AVATAR_PATH = pathlib.Path(__file__).parent / "avatar.html"

def _render_avatar():
    """Injeta o avatar HTML e sincroniza o estado via postMessage."""
    avatar_html = _AVATAR_PATH.read_text(encoding="utf-8")
    state = st.session_state.get("ai_state", "idle")

    sync_script = f"""
    <script>
      (function() {{
        function send() {{
          const iframe = document.querySelector('iframe[title="avatar"]');
          if (iframe && iframe.contentWindow) {{
            iframe.contentWindow.postMessage({{ type: 'set_state', state: '{state}' }}, '*');
          }}
        }}
        // Tenta imediatamente e depois com delay (iframe pode ainda estar carregando)
        send();
        setTimeout(send, 400);
      }})();
    </script>
    """

    components.html(
        avatar_html + sync_script,
        height=300,
        scrolling=False,
    )

def render():
    with st.sidebar:
        # ── Avatar no topo ──────────────────────────────
        _render_avatar()

        # ── Restante da sidebar original ────────────────
        st.title("🛡️ Alana Bunker")
        st.divider()

        unidades = ["C:\\", "D:\\", "E:\\", "F:\\"]

        def mudar_drive():
            st.session_state.caminho_atual = st.session_state.drive_selector

        st.selectbox(
            "⚓ Selecionar Unidade:",
            unidades,
            key="drive_selector",
            on_change=mudar_drive
        )