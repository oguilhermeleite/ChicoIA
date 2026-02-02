@echo off
title ChicoIA Bot - RODANDO AGORA
color 0A
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🤖 BOT CHICOIA - EXECUTANDO AGORA                       ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo ✅ Python encontrado: Python 3.12.10
echo ✅ Iniciando bot ChicoIA...
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

"C:\Users\Guilherme\AppData\Local\Programs\Python\Python312\python.exe" bot_simples_24_7.py

echo.
echo ═══════════════════════════════════════════════════════════════════
echo Bot encerrado!
echo ═══════════════════════════════════════════════════════════════════
pause
