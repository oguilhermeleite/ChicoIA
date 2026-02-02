@echo off
chcp 65001 >nul
color 0A
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🤖 ChicoIA Bot - EXECUTAR AGORA                         ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo ✅ Bot ultra-simples - SEM dependências externas!
echo ✅ Usa apenas Python puro (biblioteca padrão)
echo ✅ Funciona IMEDIATAMENTE!
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Tentar diferentes comandos Python
echo [1/2] Procurando Python instalado...
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
echo Por favor, instale Python:
echo.
echo 1. Acesse: https://www.python.org/downloads/
echo 2. Baixe Python 3.11 ou superior
echo 3. Execute o instalador
echo 4. ⚠️  IMPORTANTE: Marque "Add Python to PATH"
echo 5. Execute este script novamente
echo.
echo OU instale pela Microsoft Store:
echo.
echo 1. Abra Microsoft Store
echo 2. Procure por "Python 3.11"
echo 3. Clique em "Instalar"
echo 4. Execute este script novamente
echo.
pause
exit /b 1

:run_bot
echo [2/2] Iniciando bot...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
python bot_ultra_simples.py
goto :end

:run_bot_py
echo [2/2] Iniciando bot...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
py bot_ultra_simples.py
goto :end

:run_bot_python3
echo [2/2] Iniciando bot...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
python3 bot_ultra_simples.py
goto :end

:end
echo.
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Bot encerrado!
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
