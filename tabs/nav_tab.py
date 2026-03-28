import os
import streamlit as st
from core.functions import obter_telemetria_visual, obter_tamanho_formatado

def render():
    # Normalização de caminho para drives (F: -> F:\)
    caminho_alvo = st.session_state.dir_atual
    if len(caminho_alvo) == 2 and caminho_alvo[1] == ':':
        caminho_alvo += os.sep

    c1, c2 = st.columns([0.8, 0.2])
    c1.info(f"📍 Caminho: `{caminho_alvo}`")
    
    pai = os.path.dirname(caminho_alvo)
    if c2.button("⬆️ Subir", use_container_width=True, disabled=(len(caminho_alvo) <= 3)):
        st.session_state.dir_atual = pai
        st.rerun()

    try:
        itens = sorted(os.listdir(caminho_alvo))
        
        for i, item in enumerate(itens):
            # Blindagem contra arquivos de sistema
            if item.startswith('$') or item == 'System Volume Information':
                continue
                
            caminho = os.path.join(caminho_alvo, item)
            
            if os.path.isdir(caminho):
                if st.button(f"📂 {item}", key=f"n_{i}", use_container_width=True):
                    st.session_state.dir_atual = caminho
                    st.rerun()
            else:
                col_i, col_f = st.columns([0.85, 0.15])
                cor, status = obter_telemetria_visual(item)
                tamanho = obter_tamanho_formatado(caminho)
                
                # Exibição: Nome | Status | Tamanho
                col_i.markdown(f"📄 **{item}** | :{cor}[{status}] | `{tamanho}`")
                
                # Popover de Telemetria com Botão de Foco
                with col_f.popover("🚀"):
                    st.write(f"**Arquivo:** {item}")
                    st.write(f"**Tamanho:** {tamanho}")
                    st.write(f"**Status:** :{cor}[{status}]")
                    st.divider()
                    if st.button("Focar no Arquivo", key=f"f_{i}"):
                        st.session_state.arquivo_foco = caminho
                        st.toast(f"Foco definido: {item}")

    except PermissionError:
        st.error(f"🚨 ACESSO NEGADO em `{caminho_alvo}`. Tente rodar como Administrador.")
    except Exception as e:
        st.error(f"🚨 Erro: {str(e)}")