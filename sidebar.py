# Conectado ao Qwen
import streamlit as st
import streamlit.components.v1 as components
import pathlib

_AVATAR_PATH = pathlib.Path(__file__).parent / "avatar.html"

# HTML lido UMA vez no import — conteúdo nunca muda entre reruns,
# então o Streamlit reutiliza o iframe em vez de recriar.
_AVATAR_HTML = _AVATAR_PATH.read_text(encoding="utf-8") if _AVATAR_PATH.exists() else None

def render_avatar():
    if _AVATAR_HTML is None:
        st.warning("avatar.html não encontrado.")
        return

    # HTML 100% estático — sem injeção de estado aqui.
    # Isso é intencional: conteúdo idêntico = iframe preservado no rerun.
    components.html(_AVATAR_HTML, height=300, scrolling=False)

    # Estado enviado via iframe de 0px separado.
    # Usa broadcast para todos os iframes porque não temos referência direta.
    curr_state = st.session_state.get("ai_state", "idle")
    components.html(
        f"""
        <script>
        (function() {{
            var state = "{curr_state}";
            // sessionStorage do próprio mini-iframe não ajuda aqui.
            // Precisamos alcançar o iframe da Alana via parent.
            var iframes = window.parent.document.querySelectorAll('iframe');
            iframes.forEach(function(f) {{
                try {{
                    f.contentWindow.postMessage(
                        {{ type: 'set_state', state: state }}, '*'
                    );
                }} catch(e) {{}}
            }});
        }})();
        </script>
        """,
        height=0,
    )

def render():
    with st.sidebar:
        render_avatar()
        
        if st.session_state.get("hardware_busy", False):
            st.warning("🦾 OPERAÇÃO EM CURSO")
            if st.button("🚨 ABORTAR MISSÃO", type="primary", use_container_width=True):
                st.session_state.ai_state = "emergency"
                st.session_state.hardware_busy = False
                st.rerun()
            st.stop()

        st.title("🛡️ Alana Bunker")
        st.divider()
        # O seletor foi removido daqui para a aba central