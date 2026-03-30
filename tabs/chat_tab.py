import streamlit as st
from openai import OpenAI
import sidebar
import re

def _load_alana_core_config():
    try:
        with open("alana_core.txt", "r", encoding="utf-8") as f:
            content = f.read()
        hardware_match = re.search(r"^- Hardware Base: (.+)", content, re.MULTILINE)
        if hardware_match:
            return hardware_match.group(1).strip()
    except FileNotFoundError:
        st.error("⚠️ Erro: alana_core.txt não encontrado.")
    return "Hardware Base: Desconhecido"

def _load_hardware_rules():
    try:
        with open("alana_core.txt", "r", encoding="utf-8") as f:
            content = f.read()
        hardware_rules_match = re.search(r"^\[REGRAS DE OURO DE HARDWARE \(RTX 4060 8GB\)\]\n(.*?)(?=\n\[|$)", content, re.MULTILINE | re.DOTALL)
        if hardware_rules_match:
            return hardware_rules_match.group(0).strip()
    except FileNotFoundError:
        st.error("⚠️ Erro: alana_core.txt não encontrado.")
    return ""

_ALANA_HARDWARE_CONFIG = _load_alana_core_config()
_HARDWARE_RULES = _load_hardware_rules()

# ── Cliente LM Studio ─────────────────────────────────────────────
_client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)
_MODEL = "google/gemma-3-4b"

_SYSTEM_PROMPT = f"""Você é Alana, uma assistente pessoal direta e eficiente.
Você está integrada ao Alana Bunker, um sistema de gerenciamento local.

[CONFIGURAÇÃO DO BUNKER]
- {_ALANA_HARDWARE_CONFIG}

Responda sempre em português brasileiro, de forma clara e objetiva."""


def render():
    st.header("💬 Chat com Alana")

    if "user_message_count" not in st.session_state:
        st.session_state.user_message_count = 0

    # Exibe histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada do usuário
    if prompt := st.chat_input("Como posso ajudar no Bunker hoje?"):
        st.session_state.user_message_count += 1

        # Salva e exibe mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Monta histórico para a API
        historico = [{"role": "system", "content": _SYSTEM_PROMPT}]

        # Injeta as regras de hardware a cada 5 mensagens do usuário
        if st.session_state.user_message_count % 5 == 0:
            historico.append({"role": "system", "content": _HARDWARE_RULES})

        for msg in st.session_state.messages:
            historico.append({"role": msg["role"], "content": msg["content"]})

        # Avatar → pensando (Atualização Forçada)
        sidebar.update_state("thinking")

        # Stream da resposta
        with st.chat_message("assistant"):
            try:
                stream = _client.chat.completions.create(
                    model=_MODEL,
                    messages=historico,
                    stream=True,
                    temperature=0.7,
                    max_tokens=1024,
                )

                # Avatar → respondendo (Início do Stream)
                sidebar.update_state("speaking")

                resposta = st.write_stream(
                    (chunk.choices[0].delta.content or ""
                     for chunk in stream
                     if chunk.choices[0].delta.content)
                )

            except Exception as e:
                resposta = f"⚠️ Erro: {e}"
                st.error(resposta)
            finally:
                # Independente do sucesso ou erro, volta ao estado de repouso
                sidebar.update_state("idle")

        # Salva resposta no histórico
        st.session_state.messages.append({"role": "assistant", "content": resposta})
