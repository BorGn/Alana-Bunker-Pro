## =================================================================
# BLOCO 00: PROTOCOLO DE HARDENING (FIREWALL)
# Finalidade: Isolar a Alana com Validação Estrita de Privilégios
# =================================================================

Write-Host "🛡️ Iniciando Protocolo de Hardening no Bunker..." -ForegroundColor Cyan

$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "❌ ERRO CRÍTICO: Permissão Negada." -ForegroundColor Red
    Write-Host "👉 Execute o PowerShell como Administrador." -ForegroundColor Yellow
    pause
    return 
} else {
    try {
        Remove-NetFirewallRule -Name "Alana_Privacy_Guard" -ErrorAction SilentlyContinue
        New-NetFirewallRule -Name "Alana_Privacy_Guard" `
            -DisplayName "Alana_Privacy_Guard" `
            -Direction Inbound -Action Allow -Protocol TCP -LocalPort 1234 -RemoteAddress 127.0.0.1 `
            -Description "Bloqueio Externo Alana v19.20"
        Write-Host "✅ PORTA 1234 BLINDADA: Acesso restrito ao Localhost." -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Falha ao gravar regra de Firewall." -ForegroundColor Red
    }
}

# =================================================================
# BLOCO 01: GESTÃO DE VRAM E BACKEND (LM STUDIO)
# =================================================================

Write-Host "Limpando VRAM: Descarregando modelos anteriores..." -ForegroundColor Gray
lms unload --all

Write-Host "Verificando Servidor LM Studio..." -ForegroundColor Cyan
lms server start

Write-Host "Carregando Gemma-3-4B (Modo Otimizado - 16k)..." -ForegroundColor Yellow
# Carregamento com 16k de contexto para varredura total de drives
lms load google/gemma-3-4b --context-length 8192 --gpu max

Write-Host '🚀 MODO FLASH ATIVO: Gemma 3 otimizado para RTX 4060.' -ForegroundColor Cyan

Write-Host "`nSistema Pronto. Status da GPU:" -ForegroundColor Green
lms ps

# =================================================================
# BLOCO 02: LANÇAMENTO DA ESTAÇÃO ALANA (AUTO-REPARO)
# =================================================================

Write-Host "🖥️ Iniciando Estação Alana em..." -ForegroundColor Cyan

Set-Location "C:\Alana"

if (Test-Path "painel.py") {
    Write-Host "✅ painel.py localizado." -ForegroundColor Green
    
    # Validação de Dependências no 3.11
    Write-Host "🔍 Validando Streamlit no Python 3.11..." -ForegroundColor Gray
    $check = py -3.11 -m streamlit --version 2>$null
    if (-not $check) {
        Write-Host "⚠️ Streamlit não detectado no 3.11. Instalando agora..." -ForegroundColor Yellow
        py -3.11 -m pip install streamlit requests
    }

    Write-Host "🚀 Lançando Estação Alana..." -ForegroundColor Green
    py -3.11 -m streamlit run painel.py
} else {
    Write-Host "❌ ERRO CRÍTICO: painel.py não encontrado em C:\Alana!" -ForegroundColor Red
    pause
}