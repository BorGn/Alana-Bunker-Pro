import streamlit as st
import os
import pathlib
from core.functions import (obter_tamanho_formatado, obter_telemetria_visual, 
                            mapear_recursivo, read_file_content, write_file_content, 
                            create_folder, create_file, rename_item, delete_item)

def get_icon_for_file(filename):
    ext = pathlib.Path(filename).suffix.lower()
    if ext == '.py':
        return '🐍'
    elif ext in ('.json', '.yaml', '.yml', '.toml'):
        return '⚙️'
    elif ext in ('.txt', '.md', '.log'):
        return '📄'
    elif ext in ('.png', '.jpg', '.jpeg', '.gif', '.svg'):
        return '🖼️'
    elif ext in ('.zip', '.tar', '.gz', '.rar'):
        return '📦'
    return '📄'

def render():
    st.header("📂 Prometeus Cibernético")

    # Inicialização segura do GPS e estados de edição/criação
    if "caminho_atual" not in st.session_state:
        st.session_state.caminho_atual = st.session_state.get("drive_selector", "C:")
    if "editing_file" not in st.session_state:
        st.session_state.editing_file = False
    if "file_to_edit" not in st.session_state:
        st.session_state.file_to_edit = ""
    if "file_content" not in st.session_state:
        st.session_state.file_content = ""
    if "creating_item" not in st.session_state:
        st.session_state.creating_item = False
    if "renaming_item" not in st.session_state:
        st.session_state.renaming_item = False
    if "item_to_rename" not in st.session_state:
        st.session_state.item_to_rename = ""

    # --- ÁREA DE EDIÇÃO ISOLADA ---
    if st.session_state.editing_file:
        st.subheader(f"Editando: {st.session_state.file_to_edit}")
        edited_content = st.text_area(
            "Conteúdo do Arquivo:", 
            value=st.session_state.file_content, 
            height=400, 
            key="editor_area"
        )

        col_edit1, col_edit2 = st.columns([1, 10])
        with col_edit1:
            if st.button("💾 Salvar", key="save_file_btn"):
                st.session_state.confirm_save = True
        with col_edit2:
            if st.session_state.get("confirm_save", False):
                confirm_save_checkbox = st.checkbox("Confirmar salvamento? Isso sobrescreverá o arquivo.", key="confirm_save_cb")
                if confirm_save_checkbox:
                    result = write_file_content(st.session_state.file_to_edit, edited_content)
                    if result is True:
                        st.success(f"Arquivo {os.path.basename(st.session_state.file_to_edit)} salvo com sucesso!")
                        st.session_state.editing_file = False
                        st.session_state.confirm_save = False
                        st.rerun()
                    else:
                        st.error(f"Falha ao salvar: {result}")
                else:
                    st.session_state.confirm_save = False # Reset if checkbox is unchecked

        if st.button("❌ Cancelar", key="cancel_edit_btn"):
            st.session_state.editing_file = False
            st.session_state.confirm_save = False
            st.rerun()
        return

    # --- MODO VARREDURA (mantido como estava) ---
    modo = st.radio("Modo:", ["🗂️ Navegação", "🔍 Varredura Recursiva"], horizontal=True, key="nav_mode_radio")
    st.divider()

    if modo == "🔍 Varredura Recursiva":
        profundidade = st.slider("Profundidade máxima", min_value=1, max_value=5, value=3, key="scan_depth_slider")
        if st.button("🚀 Iniciar Varredura", key="start_scan_btn"):
            with st.spinner("Varrendo..."):
                resultado = mapear_recursivo(st.session_state.caminho_atual, profundidade=profundidade)
            st.code(resultado, language="")
        return

    # --- MODO NAVEGAÇÃO ---
    caminho_norm = pathlib.Path(st.session_state.caminho_atual)

    # Breadcrumbs
    st.subheader("📍 Caminho:")
    breadcrumbs = []
    current_path_segment = pathlib.Path(caminho_norm.anchor) if caminho_norm.anchor else pathlib.Path("")

    for part in caminho_norm.parts:
        if part == caminho_norm.anchor:
            current_path_segment = pathlib.Path(part)
        else:
            current_path_segment = current_path_segment / part
        breadcrumbs.append((part, str(current_path_segment)))

    cols = st.columns(len(breadcrumbs))
    for i, (name, path) in enumerate(breadcrumbs):
        with cols[i]:
            if st.button(name, key=f"breadcrumb_btn_{path}"):
                st.session_state.caminho_atual = path
                st.rerun()

    st.divider()

    # Controles de criação
    if st.button("➕ Criar Novo Item", key="create_new_item_btn"):
        st.session_state.creating_item = True

    if st.session_state.creating_item:
        with st.form("create_item_form", clear_on_submit=True):
            item_type = st.radio("Tipo de item:", ["📁 Pasta", "📄 Arquivo"], horizontal=True, key="new_item_type_radio")
            item_name = st.text_input("Nome do novo item:", key="new_item_name_input")
            submit_create = st.form_submit_button("Confirmar Criação")

            if submit_create:
                if item_name:
                    new_path = os.path.join(caminho_norm, item_name)
                    if item_type == "📁 Pasta":
                        result = create_folder(caminho_norm, item_name)
                    else:
                        result = create_file(caminho_norm, item_name)
                    
                    if result is True:
                        st.success(f"{item_type.replace('📁 ', '').replace('📄 ', '')} '{item_name}' criado com sucesso!")
                        st.session_state.creating_item = False
                        st.rerun()
                    else:
                        st.error(f"Falha ao criar item: {result}")
                else:
                    st.warning("Por favor, insira um nome para o novo item.")

        if st.button("Cancelar Criação", key="cancel_create_btn"):
            st.session_state.creating_item = False
            st.rerun()
        st.divider()

    # Listagem de Pastas e Arquivos
    try:
        itens = sorted(os.listdir(caminho_norm))
        pastas   = [i for i in itens if os.path.isdir(os.path.join(caminho_norm, i))]
        arquivos = [i for i in itens if os.path.isfile(os.path.join(caminho_norm, i))]

        st.success(f"Conteúdo de: {caminho_norm}")

        # Tabela de itens
        st.markdown("**Ícone | Nome | Detalhes | Ações**")
        st.markdown("--- ")

        # Pastas
        for p in pastas:
            full_path = os.path.join(caminho_norm, p)
            col_icon, col_name, col_details, col_actions = st.columns([0.5, 3, 2, 3])
            with col_icon:
                st.markdown("📁")
            with col_name:
                if st.button(p, key=f"folder_btn_{full_path}"):
                    st.session_state.caminho_atual = full_path
                    st.rerun()
            with col_details:
                st.write(" ") # placeholder para alinhar
            with col_actions:
                col_rename, col_delete = st.columns(2)
                with col_rename:
                    if st.button("✏️", key=f"rename_folder_btn_{full_path}"):
                        st.session_state.renaming_item = True
                        st.session_state.item_to_rename = full_path
                        st.session_state.new_item_name = p
                with col_delete:
                    if st.button("🗑️", key=f"delete_folder_btn_{full_path}"):
                        st.session_state.confirm_delete = True
                        st.session_state.item_to_delete = full_path
                        st.rerun() # para exibir a confirmação

        # Arquivos
        for f in arquivos:
            full_path = os.path.join(caminho_norm, f)
            cor, status = obter_telemetria_visual(f)
            tamanho_data = f"{obter_tamanho_formatado(full_path)} | {os.path.getmtime(full_path)}"
            icon = get_icon_for_file(f)

            col_icon, col_name, col_details, col_actions = st.columns([0.5, 3, 2, 3])
            with col_icon:
                st.markdown(icon)
            with col_name:
                st.markdown(f"`{f}`")
            with col_details:
                st.markdown(f":{cor}[**{status}**] &nbsp; <sub>{tamanho_data}</sub>", unsafe_allow_html=True)
            with col_actions:
                col_edit, col_rename, col_delete = st.columns(3)
                with col_edit:
                    if st.button("📝", key=f"edit_file_btn_{full_path}"):
                        st.session_state.file_to_edit = full_path
                        st.session_state.file_content = read_file_content(full_path)
                        if "Erro" not in st.session_state.file_content:
                            st.session_state.editing_file = True
                        else:
                            st.error(st.session_state.file_content)
                        st.rerun()
                with col_rename:
                    if st.button("✏️", key=f"rename_file_btn_{full_path}"):
                        st.session_state.renaming_item = True
                        st.session_state.item_to_rename = full_path
                        st.session_state.new_item_name = f
                with col_delete:
                    if st.button("🗑️", key=f"delete_file_btn_{full_path}"):
                        st.session_state.confirm_delete = True
                        st.session_state.item_to_delete = full_path
                        st.rerun() # para exibir a confirmação
        
        # Confirmação de Exclusão (Pop-up)
        if st.session_state.get("confirm_delete", False):
            st.warning(f"Tem certeza que deseja excluir '{os.path.basename(st.session_state.item_to_delete)}'?")
            col_del_conf1, col_del_conf2 = st.columns(2)
            with col_del_conf1:
                if st.button("✅ Sim, Excluir", key="confirm_delete_btn"):
                    result = delete_item(st.session_state.item_to_delete)
                    if result is True:
                        st.success(f"'{os.path.basename(st.session_state.item_to_delete)}' excluído com sucesso.")
                        st.session_state.confirm_delete = False
                        st.session_state.item_to_delete = ""
                        st.rerun()
                    else:
                        st.error(f"Falha ao excluir: {result}")
            with col_del_conf2:
                if st.button("❌ Não, Cancelar", key="cancel_delete_btn"):
                    st.session_state.confirm_delete = False
                    st.session_state.item_to_delete = ""
                    st.rerun()

        # Confirmação de Renomeação (Pop-up)
        if st.session_state.get("renaming_item", False) and st.session_state.item_to_rename:
            current_name = os.path.basename(st.session_state.item_to_rename)
            st.warning(f"Renomear '{current_name}':")
            new_name = st.text_input("Novo nome:", value=st.session_state.new_item_name, key="new_rename_name_input")
            
            col_ren_conf1, col_ren_conf2 = st.columns(2)
            with col_ren_conf1:
                if st.button("✅ Confirmar Renomear", key="confirm_rename_btn"):
                    if new_name and new_name != current_name:
                        result = rename_item(st.session_state.item_to_rename, new_name)
                        if result is True:
                            st.success(f"'{current_name}' renomeado para '{new_name}' com sucesso.")
                            st.session_state.renaming_item = False
                            st.session_state.item_to_rename = ""
                            st.rerun()
                        else:
                            st.error(f"Falha ao renomear: {result}")
                    else:
                        st.warning("Por favor, insira um novo nome válido.")
            with col_ren_conf2:
                if st.button("❌ Cancelar Renomear", key="cancel_rename_btn"):
                    st.session_state.renaming_item = False
                    st.session_state.item_to_rename = ""
                    st.rerun()

    except Exception as e:
        st.error(f"Erro de acesso ao diretório: {e}")