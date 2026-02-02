@echo off
chcp 65001 >nul
color 0A
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🤖 ChicoIA Bot - MODO 24/7 (TODOS USUÁRIOS)             ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo ✅ Este bot atende QUALQUER pessoa no Telegram!
echo ✅ Funciona para TODOS os usuários que procurarem @ChicoIA_bot
echo ✅ Roda continuamente até você parar
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

echo [1/2] Verificando Python...
echo.

REM Tentar python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
    python --version
    echo.
    goto :run_bot
)

REM Tentar py
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
    py --version
    echo.
    goto :run_bot_py
)

REM Tentar python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
    python3 --version
    echo.
    goto :run_bot_python3
)

REM Python não encontrado
echo.
echo ═══════════════════════════════════════════════════════════════════
echo ❌ PYTHON NÃO ENCONTRADO!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo SOLUÇÃO RÁPIDA - Microsoft Store (3 cliques):
echo.
echo 1. Abra Microsoft Store
echo 2. Procure "Python 3.12"
echo 3. Clique em "Obter"
echo.
echo Ou baixe do site oficial:
echo https://www.python.org/downloads/
echo (Marque "Add Python to PATH" na instalação)
echo.
pause
exit /b 1

:run_bot
echo [2/2] Iniciando bot modo 24/7...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
python bot_simples_24_7.py
goto :end

:run_bot_py
echo [2/2] Iniciando bot modo 24/7...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
py bot_simples_24_7.py
goto :end

:run_bot_python3
echo [2/2] Iniciando bot modo 24/7...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
python3 bot_simples_24_7.py
goto :end

:end
echo.
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Bot encerrado!
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
