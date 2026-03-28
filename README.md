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

## 🧬 Fonte da Verdade
- Toda lógica de comportamento deve respeitar o arquivo `alana_core.txt`.
- Não assumir a existência de pastas como "modulos" ou nomes de arquivos em português fora da pasta raiz, a menos que explicitado neste README.

---
*Projeto Original em C:\Alana*