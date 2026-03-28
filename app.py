import streamlit as st
import streamlit.components.v1 as components
import time
import pathlib

# ── Configuração da página ──────────────────────────────────────────
st.set_page_config(
    page_title="Minha IA",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS global: remove padding da sidebar, fundo escuro ────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] {
      background: #0e0d0c !important;
      padding: 0 !important;
  }
  [data-testid="stSidebar"] > div:first-child {
      padding: 0 !important;
  }
  /* Remove a barra branca de topo da sidebar */
  [data-testid="stSidebarHeader"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Lê o HTML do avatar ────────────────────────────────────────────
AVATAR_PATH = pathlib.Path(__file__).parent / "avatar.html"
avatar_html = AVATAR_PATH.read_text(encoding="utf-8")

# ── Estado da sessão ───────────────────────────────────────────────
if "ai_state" not in st.session_state:
    st.session_state.ai_state = "idle"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar: avatar + controles de estado ─────────────────────────
with st.sidebar:
    # Injeta o avatar + script de comunicação
    state = st.session_state.ai_state
    inject_script = f"""
    <script>
      // Aguarda o iframe carregar e envia o estado atual
      setTimeout(() => {{
        const iframe = document.querySelector('iframe[title="avatar"]');
        if (iframe && iframe.contentWindow) {{
          iframe.contentWindow.postMessage({{ type: 'set_state', state: '{state}' }}, '*');
        }}
      }}, 300);
    </script>
    """
    components.html(
        avatar_html + inject_script,
        height=320,
        scrolling=False,
    )

    # Controles manuais de estado (para demo — remova em produção)
    st.markdown("---")
    st.caption("Estado do avatar")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Idle", use_container_width=True):
            st.session_state.ai_state = "idle"
            st.rerun()
    with col2:
        if st.button("Pensando", use_container_width=True):
            st.session_state.ai_state = "thinking"
            st.rerun()
    with col3:
        if st.button("Falando", use_container_width=True):
            st.session_state.ai_state = "speaking"
            st.rerun()

# ── Área principal: chat simples de exemplo ────────────────────────
st.title("Minha IA Pessoal")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Muda para "thinking"
    st.session_state.ai_state = "thinking"
    st.rerun()

# ── Lógica de resposta (adapte para sua IA local) ──────────────────
# Este bloco simula uma resposta. Substitua pela chamada real à sua IA.
if st.session_state.ai_state == "thinking" and st.session_state.messages:
    last = st.session_state.messages[-1]
    if last["role"] == "user":
        time.sleep(1.5)  # Simula processamento — substitua pela chamada real
        response = f"Resposta para: {last['content']}"  # <-- sua IA aqui

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.ai_state = "speaking"
        st.rerun()

# Volta para idle após "speaking" (opcional — remova se preferir controle manual)
if st.session_state.ai_state == "speaking":
    time.sleep(2)
    st.session_state.ai_state = "idle"
    st.rerun()
