#!/bin/bash
# ChicoIA Telegram Bot - Linux/Mac Run Script

echo "================================"
echo "ChicoIA Telegram Bot"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Ativando ambiente virtual..."
source venv/bin/activate
echo ""

# Install/update dependencies
echo "Instalando dependências..."
pip install -r requirements.txt --quiet
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERRO: Arquivo .env não encontrado!"
    echo "Por favor, copie .env.example para .env e configure suas credenciais."
    exit 1
fi

# Run the bot
echo "Iniciando bot..."
echo ""
python bot/main.py
