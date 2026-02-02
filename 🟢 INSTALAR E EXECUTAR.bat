@echo off
chcp 65001 >nul
color 0A
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║     🟢 INSTALAR PYTHON E EXECUTAR BOT - TUDO AUTOMÁTICO          ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Este script vai:
echo ✓ Verificar se Python está instalado
echo ✓ Instalar Python automaticamente (se necessário)
echo ✓ Executar o bot ChicoIA
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Pressione qualquer tecla para começar...
pause >nul

cls
echo.
echo [1/3] Verificando Python...
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
    python --version
    goto :bot_start
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
    py --version
    goto :bot_start_py
)

REM Python não encontrado - instalar
echo ❌ Python não encontrado!
echo.
echo [2/3] Instalando Python via Microsoft Store...
echo.
echo ⚠️  IMPORTANTE: Uma janela da Microsoft Store vai abrir.
echo    Clique em "Obter" ou "Instalar" e aguarde.
echo.
echo Pressione qualquer tecla para abrir a Microsoft Store...
pause >nul

REM Abrir Microsoft Store na página do Python
start ms-windows-store://pdp/?ProductId=9NCVDN91XZQP

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 📦 Microsoft Store aberta!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo FAÇA ISTO NA MICROSOFT STORE:
echo.
echo 1. Clique em "Obter" ou "Instalar"
echo 2. Aguarde a instalação terminar (2-3 minutos)
echo 3. Volte aqui e pressione qualquer tecla
echo.
echo Aguardando você instalar o Python...
pause >nul

REM Verificar se Python foi instalado
cls
echo.
echo [3/3] Verificando se Python foi instalado...
echo.

timeout /t 3 /nobreak >nul

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python instalado com sucesso!
    python --version
    goto :bot_start
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python instalado com sucesso!
    py --version
    goto :bot_start_py
)

REM Ainda não encontrou Python
echo ❌ Python ainda não foi detectado.
echo.
echo Possíveis soluções:
echo.
echo 1. Feche e abra o Prompt de Comando novamente
echo 2. Reinicie o computador
echo 3. Execute este arquivo novamente
echo.
echo Ou tente instalar manualmente:
echo https://www.python.org/downloads/
echo (Marque "Add Python to PATH" na instalação)
echo.
pause
exit /b 1

:bot_start
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          ✅ PYTHON INSTALADO - INICIANDO BOT                     ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Iniciando bot ChicoIA...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

python bot_simples_24_7.py
goto :end

:bot_start_py
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          ✅ PYTHON INSTALADO - INICIANDO BOT                     ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Iniciando bot ChicoIA...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

py bot_simples_24_7.py
goto :end

:end
echo.
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Bot encerrado!
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
