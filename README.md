# 🛡️ Alana Bunker Pro - v1.0

### ⚠️ INSTRUÇÃO CRÍTICA PARA IA (GEMINI)
Antes de qualquer análise, leia esta estrutura. Este é um NOVO PROJETO, independente de versões anteriores. A arquitetura é modular e reside estritamente nestas definições:

## 📂 Estrutura de Diretórios
- `/` : Raiz contendo o `painel.py` (execução principal).
- `/core` : Configurações de sistema (`config.py`, `state.py`).
- `/tabs` : Módulos de interface divididos por abas (`nav_tab`, `chat_tab`, `bra_tab`, `ent_tab`).

## 🛠️ Fluxo de Execução
1. O `painel.py` inicializa a página via `core.config`.
2. O estado é carregado via `core.state`.
3. A barra lateral é renderizada por `sidebar.py`.
4. As abas são chamadas pelos módulos contidos em `/tabs`.

# 🛡️ Alana Bunker Pro - v1.0

### ⚠️ DIRETRIZ CRÍTICA DE ARQUITETURA
Este projeto utiliza uma estrutura modular estrita. A verdade absoluta reside nestes arquivos:

## 📂 Organização
- `painel.py`: Ponto de entrada. Gerencia a renderização das abas.
- `sidebar.py`: **Módulo Crítico**. Funciona em conjunto com o painel para renderizar controles laterais.
- `/core`: Configurações (`config.py`) e Estado Global (`state.py`).
- `/tabs`: Conteúdo específico de cada aba do painel.

## ⚙️ Fluxo de Integração
O `painel.py` importa e executa `sidebar.render()`. 
Nenhuma lógica de navegação ou configuração deve ignorar a existência do arquivo `sidebar.py` na raiz.

Estado do Sistema: Estrutura Modular Ativa.
Navegação: Sincronizada via st.session_state entre Sidebar e Nav_Tab.
Hardware: Braço do Open-Interpreter restaurado via PowerShell (Janela Azul).
Localização: Estritamente em C:\Alana.

---
*Origem: C:\Alana*

## 🧬 Fonte da Verdade
- Toda lógica de comportamento deve respeitar o arquivo `alana_core.txt`.
- Não assumir a existência de pastas como "modulos" ou nomes de arquivos em português fora da pasta raiz, a menos que explicitado neste README.

---
*Projeto Original em C:\Alana*