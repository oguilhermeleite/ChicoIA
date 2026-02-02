@echo off
chcp 65001 >nul
color 0C
title ChicoIA Bot - EXECUTANDO AGORA
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🔴 BOT CHICOIA - INICIANDO AGORA                        ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo ⚡ Fazendo o bot funcionar AGORA no Telegram...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Testar Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
    python --version
    echo.
    echo 🚀 Iniciando bot...
    echo.
    echo ═══════════════════════════════════════════════════════════════════
    echo.
    echo ✅ BOT RODANDO!
    echo.
    echo 📱 AGORA FAÇA ISTO NO TELEGRAM:
    echo    1. Abra o Telegram
    echo    2. Procure: @ChicoIA_bot
    echo    3. Envie: /start
    echo    4. BOT RESPONDE! 🎉
    echo.
    echo ⚠️  DEIXE ESTA JANELA ABERTA enquanto usa o bot!
    echo.
    echo ═══════════════════════════════════════════════════════════════════
    echo.
    python bot_simples_24_7.py
    goto :end
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
    py --version
    echo.
    echo 🚀 Iniciando bot...
    echo.
    echo ═══════════════════════════════════════════════════════════════════
    echo.
    echo ✅ BOT RODANDO!
    echo.
    echo 📱 AGORA FAÇA ISTO NO TELEGRAM:
    echo    1. Abra o Telegram
    echo    2. Procure: @ChicoIA_bot
    echo    3. Envie: /start
    echo    4. BOT RESPONDE! 🎉
    echo.
    echo ⚠️  DEIXE ESTA JANELA ABERTA enquanto usa o bot!
    echo.
    echo ═══════════════════════════════════════════════════════════════════
    echo.
    py bot_simples_24_7.py
    goto :end
)

REM Python não encontrado
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          ❌ PYTHON NÃO ENCONTRADO!                               ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Você precisa instalar o Python primeiro!
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 📥 OPÇÃO 1 - Microsoft Store (MAIS FÁCIL):
echo.
echo    1. Abra a Microsoft Store
echo    2. Procure: "Python 3.12"
echo    3. Clique em "Obter"
echo    4. Execute este arquivo novamente
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 📥 OPÇÃO 2 - Site Oficial:
echo.
echo    1. Acesse: https://www.python.org/downloads/
echo    2. Baixe Python 3.11 ou superior
echo    3. Execute o instalador
echo    4. ⚠️  IMPORTANTE: Marque "Add Python to PATH"
echo    5. Execute este arquivo novamente
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Pressione ENTER para abrir o site do Python...
pause >nul
start https://www.python.org/downloads/
goto :end

:end
echo.
pause
