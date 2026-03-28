import streamlit as st

def render():
    st.header("💬 Chat com Alana")
    
    # Exibe o histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Campo de entrada do usuário
    if prompt := st.chat_input("Como posso ajudar no Bunker hoje?"):
        # Adiciona mensagem do usuário ao estado
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Resposta da Alana (Aqui é onde a mágica acontece)
        with st.chat_message("assistant"):
            # AQUI: Substitua pela chamada real da sua API ou lógica de resposta
            resposta = f"Recebi seu comando: '{prompt}'. Analisando diretrizes do alana_core.txt..."
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})