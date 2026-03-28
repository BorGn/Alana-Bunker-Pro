import os, string

def detectar_drives():
    """Recupera unidades físicas (C, D, E, F)"""
    return [f"{l}:\\" for l in string.ascii_uppercase if os.path.exists(f"{l}:\\")]

def obter_tamanho_formatado(caminho):
    """Calcula o tamanho do arquivo e formata para leitura humana."""
    try:
        tamanho = os.path.getsize(caminho)
        for unidade in ['B', 'KB', 'MB', 'GB']:
            if tamanho < 1024:
                return f"{tamanho:.1f} {unidade}"
            tamanho /= 1024
    except:
        return "---"

def obter_telemetria_visual(nome_arq):
    """Define as cores e status baseados na extensão."""
    if nome_arq.endswith(('.py.txt', '.ps1.txt')): 
        return "blue", "HIBERNAÇÃO"
    
    ext = os.path.splitext(nome_arq)[1].lower()
    
    # Verde: Código e Configuração
    if ext in ['.py', '.txt', '.ps1', '.yaml', '.json', '.md']: 
        return "green", "CÓDIGO VIVO"
    
    # Azul: Acervo e Biblioteca (Perry Rhodan, etc)
    if ext in ['.epub', '.pdf', '.mobi', '.opf']:
        return "blue", "BIBLIOTECA"
        
    # Vermelho: Binários e Estrutura
    return "red", "ESTRUTURA/BIN"

def mapear_recursivo(diretorio, profundidade=3):
    """Varredura blindada contra pastas de sistema."""
    mapa = []
    ignorar = {'.git', '__pycache__', 'node_modules', '.venv', '$RECYCLE.BIN', 'System Volume Information'}
    try:
        diretorio = os.path.normpath(diretorio)
        for raiz, pastas, arquivos in os.walk(diretorio):
            pastas[:] = [d for d in pastas if d not in ignorar and not d.startswith('$')]
            nivel = raiz.replace(diretorio, '').count(os.sep)
            if nivel > profundidade: continue
            indent = "    " * nivel
            mapa.append(f"{indent}📂 {os.path.basename(raiz) or raiz}/")
            for f in arquivos:
                mapa.append(f"{indent}    📄 {f}")
        return "\n".join(mapa)
    except:
        return "🚨 Acesso Negado."