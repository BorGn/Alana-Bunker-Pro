import streamlit as st
import subprocess

def render():
    st.header("🛠️ Administração do Bunker")
    
    # --- BRAÇO OPERACIONAL: OPEN-INTERPRETER EM POWERSHELL ---
    st.subheader("🦾 Comando Open Interpreter (PowerShell)")
    tarefa = st.text_area("Ordem direta para o hardware:", placeholder="Digite o comando para o Interpreter...")
    
    if st.button("Executar via Janela Azul (PowerShell)"):
        if tarefa:
            try:
                # Comando que abre o PowerShell, executa o interpreter e NÃO fecha a janela (-NoExit)
                ps_command = f'interpreter --task "{tarefa}"'
                subprocess.Popen([
                    "powershell", 
                    "-NoExit", 
                    "-Command", 
                    ps_command
                ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                
                st.success("✅ PowerShell disparado com Open-Interpreter.")
            except Exception as e:
                st.error(f"Erro ao invocar PowerShell: {e}")
        else:
            st.warning("⚠️ O campo de tarefa está vazio.")

    st.divider()
    
    # --- MONITORAMENTO DE ESTADO ---
    st.write(f"Sessão ativa: {st.session_state.get('alana_model', 'Padrão')}")
    if st.button("Limpar Histórico do Chat"):
        st.session_state.messages = []
        st.rerun()