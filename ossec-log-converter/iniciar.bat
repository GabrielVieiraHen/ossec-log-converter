@echo off
setlocal enabledelayedexpansion
title Instalador e Conversor de Logs OSSEC

echo ==========================================
echo      CONVERSOR DE LOGS OSSEC PARA PBI
echo ==========================================
echo.

:: 1. Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python nao encontrado.
    echo [*] Tentando instalar Python via Winget...
    
    :: Tenta instalar o Python 3.11
    winget install -e --id Python.Python.3.11 --accept-source-agreements --accept-package-agreements
    
    if %errorlevel% neq 0 (
        echo.
        echo [X] Nao foi possivel instalar o Python automaticamente.
        echo Por favor, instale manualmente em python.org e marque a opcao "Add to PATH".
        pause
        exit /b
    )
    
    echo [V] Python instalado com sucesso! Reiniciando variaveis de ambiente...
    call refreshenv >nul 2>&1
) else (
    echo [V] Python ja esta instalado.
)

:: 2. Verifica/Cria o Ambiente Virtual (venv) para isolar as bibliotecas
if not exist "venv" (
    echo.
    echo [*] Criando ambiente virtual (primeira vez)...
    python -m venv venv
)

:: 3. Ativa o ambiente e instala dependencias
echo.
echo [*] Verificando dependencias (pandas, openpyxl)...
call venv\Scripts\activate.bat

:: Instala sem mostrar muita sujeira na tela, a menos que de erro
pip install pandas openpyxl >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Erro ao instalar bibliotecas. Tentando novamente com saida detalhada:
    pip install pandas openpyxl
) else (
    echo [V] Dependencias prontas.
)

:: 4. Executa o Script Principal
echo.
echo ==========================================
echo     TUDO PRONTO. INICIANDO PROGRAMA...
echo ==========================================
echo.

:: Executa o seu script (certifique-se que o nome do arquivo py esta correto aqui)
python converter.py

:: 5. Pausa final para o usuario ver o resultado
echo.
echo Pressione qualquer tecla para sair...
pause >nul
