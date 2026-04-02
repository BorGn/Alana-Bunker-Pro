import os
import string
import shutil
import pathlib
from datetime import datetime

def detectar_drives():
    drives = []
    for letra in string.ascii_uppercase:
        caminho = letra + ":\\"
        if os.path.exists(caminho):
            drives.append(caminho)
    return drives

def obter_tamanho_formatado(caminho):
    try:
        tamanho = os.path.getsize(caminho)
        for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
            if tamanho < 1024:
                return f"{tamanho:.2f} {unidade}"
            tamanho /= 1024
    except:
        return "0 B"

def read_file_content(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

def write_file_content(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except:
        return False

def create_folder(path, folder_name):
    try:
        full_path = os.path.join(path, folder_name)
        os.makedirs(full_path, exist_ok=True)
        return True
    except:
        return False

def create_file(path, file_name, content=""):
    try:
        full_path = os.path.join(path, file_name)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except:
        return False

def rename_item(old_path, new_name):
    try:
        parent = os.path.dirname(old_path)
        new_path = os.path.join(parent, new_name)
        os.rename(old_path, new_path)
        return True
    except:
        return False

def delete_item(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    except:
        return False

def obter_telemetria_visual(nome_arquivo):
    """Retorna a cor e o status de segurança baseado na extensão do arquivo."""
    extensoes_seguras = ['.py', '.txt', '.md', '.json', '.yaml', '.yml', '.html', '.css', '.js']
    extensao = pathlib.Path(nome_arquivo).suffix.lower()
    
    if extensao in extensoes_seguras:
        return "green", "Seguro"
    return "orange", "Analisar"

def mapear_recursivo(caminho, profundidade=3, nivel_atual=0):
    """Gera uma árvore de diretórios em formato de texto para varredura."""
    if nivel_atual > profundidade:
        return ""
    
    resultado = ""
    try:
        itens = os.listdir(caminho)
        for item in itens:
            full_path = os.path.join(caminho, item)
            prefixo = "  " * nivel_atual + "|-- "
            resultado += f"{prefixo}{item}\n"
            if os.path.isdir(full_path):
                resultado += mapear_recursivo(full_path, profundidade, nivel_atual + 1)
    except Exception as e:
        resultado += f"{'  ' * nivel_atual}|-- [Erro de Acesso: {e}]\n"
        
    return resultado
def check_server(host="127.0.0.1", port=1234):
    """Verifica se o backend do LM Studio está rodando e respondendo."""
    import socket
    try:
        # Tenta abrir uma conexão rápida com a porta do LM Studio
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False