@echo off
chcp 65001 >nul
color 0A

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🤖 ChicoIA Bot - Instalação e Execução                  ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo ✗ Python NÃO está instalado!
        echo.
        echo Por favor, instale o Python 3.11 ou superior:
        echo 1. Acesse: https://www.python.org/downloads/
        echo 2. Baixe Python 3.11 ou superior
        echo 3. Execute o instalador
        echo 4. ⚠️  IMPORTANTE: Marque "Add Python to PATH"
        echo 5. Execute este script novamente
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo ✓ Python encontrado!
%PYTHON_CMD% --version
echo.

REM Verificar/Criar ambiente virtual
echo [2/5] Configurando ambiente virtual...
if not exist "venv\" (
    echo Criando ambiente virtual...
    %PYTHON_CMD% -m venv venv
    echo ✓ Ambiente virtual criado!
) else (
    echo ✓ Ambiente virtual já existe!
)
echo.

REM Ativar ambiente virtual
echo [3/5] Ativando ambiente virtual...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ✗ Erro ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✓ Ambiente virtual ativado!
echo.

REM Instalar dependências
echo [4/5] Instalando dependências...
echo (Isso pode demorar alguns minutos na primeira vez...)
echo.
pip install --upgrade pip >nul 2>&1
pip install python-telegram-bot python-dotenv >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Erro ao instalar dependências
    echo Tentando novamente...
    pip install python-telegram-bot python-dotenv
    if %errorlevel% neq 0 (
        pause
        exit /b 1
    )
)
echo ✓ Dependências instaladas!
echo.

REM Verificar .env
echo [5/5] Verificando configuração...
if not exist ".env" (
    echo ✗ Arquivo .env não encontrado!
    echo Criando .env...
    copy .env.example .env >nul
)
echo ✓ Configuração OK!
echo.

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║                    ✅ TUDO PRONTO!                                ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Iniciando bot de teste (SEM banco de dados)...
echo.
echo ⚠️  IMPORTANTE: Depois que o bot iniciar:
echo    1. Abra o Telegram
echo    2. Procure por: @ChicoIA_bot
echo    3. Envie: /start
echo.
echo Pressione Ctrl+C para parar o bot
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Executar bot de teste
python test_bot_simple.py

echo.
pause
