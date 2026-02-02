@echo off
chcp 65001 >nul
color 0A
title Instalando Python - Aguarde...
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🔧 INSTALANDO PYTHON AUTOMATICAMENTE                    ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Por favor, aguarde...
echo.

REM Verificar se Python já está instalado
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python já está instalado!
    python --version
    echo.
    echo Pressione qualquer tecla para continuar...
    pause >nul
    goto :iniciar_bot
)

REM Tentar instalar via winget (mais rápido)
echo 📥 Baixando e instalando Python...
echo.
winget install Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements >nul 2>&1

REM Aguardar instalação
timeout /t 30 /nobreak >nul

REM Verificar se instalou
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python instalado com sucesso!
    python --version
    echo.
    goto :iniciar_bot
)

REM Se winget falhar, abrir Microsoft Store
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          📦 ABRIR MICROSOFT STORE                                ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo A instalação automática não funcionou.
echo.
echo Vou abrir a Microsoft Store para você instalar manualmente:
echo.
echo 1. Procure por "Python 3.12"
echo 2. Clique em "Obter" ou "Instalar"
echo 3. Aguarde a instalação (2-3 minutos)
echo 4. Execute este arquivo novamente
echo.
echo Pressione qualquer tecla para abrir a Microsoft Store...
pause >nul
start ms-windows-store://pdp/?ProductId=9NCVDN91XZQP
echo.
echo Após instalar o Python na Microsoft Store,
echo execute este arquivo novamente!
echo.
pause
exit /b 1

:iniciar_bot
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🚀 INICIANDO BOT CHICOIA                                ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo ✅ Python instalado!
echo ✅ Iniciando bot...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

python bot_simples_24_7.py

echo.
echo ═══════════════════════════════════════════════════════════════════
echo Bot encerrado!
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
