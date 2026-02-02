@echo off
REM ChicoIA Telegram Bot - Windows Run Script

echo ================================
echo ChicoIA Telegram Bot
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Ativando ambiente virtual...
call venv\Scripts\activate
echo.

REM Install/update dependencies
echo Instalando dependencias...
pip install -r requirements.txt --quiet
echo.

REM Check if .env exists
if not exist ".env" (
    echo ERRO: Arquivo .env nao encontrado!
    echo Por favor, copie .env.example para .env e configure suas credenciais.
    pause
    exit /b 1
)

REM Run the bot
echo Iniciando bot...
echo.
python bot/main.py

pause
