@echo off
title ChicoIA Bot - Rodando
color 0A
cls

echo.
echo ========================================================================
echo.
echo             BOT CHICOIA - INICIANDO AGORA
echo.
echo ========================================================================
echo.
echo Python foi instalado com sucesso!
echo Iniciando bot...
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

"C:\Users\Guilherme\AppData\Local\Programs\Python\Python312\python.exe" bot_simples_24_7.py 2>nul
if %errorlevel% neq 0 (
    "C:\Program Files\Python312\python.exe" bot_simples_24_7.py 2>nul
)
if %errorlevel% neq 0 (
    python bot_simples_24_7.py 2>nul
)
if %errorlevel% neq 0 (
    py bot_simples_24_7.py 2>nul
)
if %errorlevel% neq 0 (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" bot_simples_24_7.py 2>nul
)
if %errorlevel% neq 0 (
    "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" bot_simples_24_7.py
)

pause
