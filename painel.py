import streamlit as st
from modulos import aba_navegacao, aba_inspecao, aba_organizacao

# 1. Definições de Funções (QUE FALTAM NO SEU CÓDIGO ATUAL)
def chamar_alana_api(prompt):
    pass # Coloque aqui sua lógica de API

def ler_diretrizes_core():
    pass # Coloque aqui sua lógica de leitura do TXT

EXTENSOES_TEXTO = [".py", ".txt", ".md"]

# 2. Configuração
st.set_page_config(page_title="Alana Bunker", layout="wide")

# 3. Definição das Abas
# Note: Usei os mesmos nomes que você colou na parte de baixo
tab_nav, tab_insp, tab_org = st.tabs(["📂 Navegação", "🔬 Inspeção Técnica", "🧬 Entropia"])

with tab_nav:
    aba_navegacao.renderizar()

with tab_insp:
    aba_inspecao.renderizar(chamar_alana_api, ler_diretrizes_core, EXTENSOES_TEXTO)

with tab_org:
    st.header("🧬 Varredura de Entropia")
    aba_organizacao.renderizar(chamar_alana_api, ler_diretrizes_core)