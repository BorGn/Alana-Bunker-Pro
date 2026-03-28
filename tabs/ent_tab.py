import streamlit as st
import os
from core.functions import mapear_recursivo # Certifique-se que este caminho está correto

def render():
    # Inicialização de segurança para evitar quebras de interface
    if 'mapa_recursivo' not in st.session_state:
        st.session_state.mapa_recursivo = None

    st.title("🧬 Varredura de Estrutura & Entropia")
    
    # Feedback visual do diretório ativo na sidebar
    diretorio_alvo = st.session_state.get('dir_atual', os.getcwd())
    st.warning(f"🎯 Alvo Selecionado: **{diretorio_alvo}**")
    st.caption("Analise a hierarquia para identificar redundâncias e 'Código Fóssil'.")

    prof = st.slider("Profundidade da Árvore", 1, 5, 3)
    
    if st.button("🔍 Escanear Estrutura Atual", type="primary", use_container_width=True):
        with st.spinner("Mapeando diretórios..."):
            # A chamada agora é protegida pelo estado global
            st.session_state.mapa_recursivo = mapear_recursivo(diretorio_alvo, prof)
            st.success("✅ Varredura Concluída.")

    # Só mostra resultados e download se houver dados
    if st.session_state.mapa_recursivo:
        st.divider()
        st.subheader("📋 Mapa de Diretórios")
        st.code(st.session_state.mapa_recursivo, language="text")

        # Geração de script baseada no alvo real atualizado
        ps = f'$O="{diretorio_alvo}"; $S="C:\\Alana_Sandbox"; if(Test-Path $S){{rm $S -Recurse -F}}; ni $S -ItemType Directory; gci $O -MaxDepth {prof} | %{{$D=$_.FullName.Replace($O,$S); if($_.PSIsContainer){{ni $D -ItemType Directory -F}}else{{ni $D -ItemType File -F}}}}'
        st.download_button(
            label="📥 Baixar Script de Simulação (.ps1)",
            data=ps,
            file_name="Simular_Sandbox.ps1",
            use_container_width=True
        )