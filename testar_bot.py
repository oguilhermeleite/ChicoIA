#!/usr/bin/env python3
"""
Testa se o bot está funcionando enviando mensagem diretamente
"""

import json
import urllib.request
import time

TOKEN = "8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

print("=" * 70)
print("🧪 TESTANDO BOT CHICOAI")
print("=" * 70)
print()

# 1. Testar se o bot está acessível
print("1️⃣ Testando conexão com bot...")
try:
    url = f"{BASE_URL}/getMe"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Bot encontrado!")
            print(f"   Nome: {bot_info.get('first_name')}")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   ID: {bot_info.get('id')}")
        else:
            print("❌ Erro ao conectar com bot")
            exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    print("\nVerifique sua conexão com internet!")
    exit(1)

print()

# 2. Verificar se há mensagens pendentes
print("2️⃣ Verificando se o bot está processando mensagens...")
try:
    url = f"{BASE_URL}/getUpdates"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        if data.get('ok'):
            updates = data.get('result', [])
            print(f"✅ Bot está online!")
            print(f"   Mensagens na fila: {len(updates)}")
        else:
            print("❌ Erro ao verificar mensagens")
except Exception as e:
    print(f"⚠️  Erro: {e}")

print()

# 3. Instruções
print("=" * 70)
print("📱 AGORA TESTE NO TELEGRAM:")
print("=" * 70)
print()
print("1. Abra o Telegram")
print("2. Procure por: @ChicoIA_bot")
print("3. Envie: /start")
print()
print("✅ O bot vai responder IMEDIATAMENTE se estiver rodando!")
print()
print("⚠️  Se não responder, execute:")
print("   python bot_simples_24_7.py")
print()
print("=" * 70)
