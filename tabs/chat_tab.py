import streamlit as st
from openai import OpenAI

# ── Cliente LM Studio ─────────────────────────────────────────────
_client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)
_MODEL = "google/gemma-3-4b"

_SYSTEM_PROMPT = """Você é Alana, uma assistente pessoal direta e eficiente.
Você está integrada ao Alana Bunker, um sistema de gerenciamento local.
Responda sempre em português brasileiro, de forma clara e objetiva."""


def render():
    st.header("💬 Chat com Alana")

    # Exibe histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada do usuário
    if prompt := st.chat_input("Como posso ajudar no Bunker hoje?"):

        # Salva e exibe mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Monta histórico para a API
        historico = [{"role": "system", "content": _SYSTEM_PROMPT}]
        for msg in st.session_state.messages:
            historico.append({"role": msg["role"], "content": msg["content"]})

        # Avatar → pensando
        st.session_state.ai_state = "thinking"

        # Stream da resposta — tudo dentro do mesmo bloco, sem rerun
        with st.chat_message("assistant"):
            try:
                stream = _client.chat.completions.create(
                    model=_MODEL,
                    messages=historico,
                    stream=True,
                    temperature=0.7,
                    max_tokens=1024,
                )

                # Avatar → respondendo antes de começar a escrever
                st.session_state.ai_state = "speaking"

                resposta = st.write_stream(
                    (chunk.choices[0].delta.content or ""
                     for chunk in stream
                     if chunk.choices[0].delta.content)
                )

            except Exception as e:
                resposta = f"⚠️ Erro: {e}"
                st.error(resposta)

        # Salva resposta e volta ao idle
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        st.session_state.ai_state = "idle"
