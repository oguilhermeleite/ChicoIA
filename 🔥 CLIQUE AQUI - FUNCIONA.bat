@echo off
chcp 65001 >nul
title BOT CHICOIA - FUNCIONANDO
color 0A
cls

echo.
echo ██████████████████████████████████████████████████████████████████
echo.
echo              BOT CHICOIA - INICIANDO AGORA
echo.
echo ██████████████████████████████████████████████████████████████████
echo.
echo.

cd /d "C:\Users\Guilherme\Downloads\Chico - telegram"

echo Executando bot...
echo.
echo ══════════════════════════════════════════════════════════════════
echo.
echo ✅ QUANDO APARECER "BOT ONLINE - ATENDENDO TODOS OS USUARIOS"
echo    O BOT ESTA FUNCIONANDO!
echo.
echo ✅ DEIXE ESTA JANELA ABERTA!
echo.
echo ✅ VA PARA O TELEGRAM:
echo    1. Procure: @ChicoIA_bot
echo    2. Envie: /start
echo    3. BOT RESPONDE!
echo.
echo ══════════════════════════════════════════════════════════════════
echo.
echo Iniciando em 3 segundos...
timeout /t 3 /nobreak >nul
echo.

"C:\Users\Guilherme\AppData\Local\Programs\Python\Python312\python.exe" bot_simples_24_7.py

pause
