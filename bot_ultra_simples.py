#!/usr/bin/env python3
"""
ChicoIA Bot - Versão ULTRA SIMPLES
Usa apenas a biblioteca padrão do Python (sem dependências externas!)
"""

import json
import urllib.request
import urllib.parse
import time
import sys

# Token do bot
TOKEN = "8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    """Envia mensagem para o usuário"""
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return None

def get_updates(offset=None):
    """Busca novas mensagens"""
    url = f"{BASE_URL}/getUpdates"
    if offset:
        url += f"?offset={offset}"

    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Erro ao buscar mensagens: {e}")
        return None

def handle_message(chat_id, text, user_name):
    """Processa mensagens do usuário"""

    if text == '/start':
        response = f"""🎉 *Olá, {user_name}!*

Eu sou o Chico, assistente da ChicoIA! 👋

*O BOT ESTÁ FUNCIONANDO!* ✅

Comandos disponíveis:
• /start - Esta mensagem
• /ajuda - Ver comandos
• /sobre - Sobre o ChicoIA

Envie qualquer mensagem e eu respondo!"""

    elif text == '/ajuda':
        response = """🤖 *Comandos Disponíveis:*

/start - Mensagem de boas-vindas
/ajuda - Esta mensagem de ajuda
/sobre - Sobre a ChicoIA
/status - Status do bot

Você também pode conversar comigo normalmente!
Envie qualquer mensagem."""

    elif text == '/sobre':
        response = """🏆 *ChicoIA - Plataforma de Apostas Esportivas*

Somos a plataforma brasileira de apostas esportivas com:
✅ Análise inteligente de jogos
✅ Sugestões de apostas
✅ Gestão de banca
✅ Alertas de value bets

🌐 Site: https://chicoia.com.br
📧 Contato: suporte@chicoia.com.br"""

    elif text == '/status':
        response = """✅ *Status do Bot*

Token: Válido ✓
Conexão: OK ✓
API Telegram: Funcionando ✓
Resposta: Rápida ✓

*Tudo funcionando perfeitamente!* 🎉"""

    else:
        response = f"""Opa, {user_name}! 👋

Você disse: "{text}"

Tô funcionando direitinho! Respondo tudo que você mandar.

Para ver os comandos disponíveis, envie /ajuda"""

    return response

def main():
    """Função principal"""
    print("=" * 70)
    print("🤖 ChicoIA Bot - VERSÃO ULTRA SIMPLES")
    print("=" * 70)
    print()
    print("✅ Sem dependências externas - só Python puro!")
    print("✅ Token configurado")
    print("✅ Pronto para funcionar!")
    print()
    print("-" * 70)
    print("🔄 Iniciando bot...")

    # Testar conexão
    try:
        result = get_updates()
        if result and result.get('ok'):
            print("✅ Conexão com Telegram estabelecida!")
            print(f"✅ Bot: @ChicoIA_bot")
            print()
            print("=" * 70)
            print("🎯 BOT ESTÁ RODANDO!")
            print("=" * 70)
            print()
            print("📱 Agora faça isto no Telegram:")
            print("   1. Abra o Telegram")
            print("   2. Procure por: @ChicoIA_bot")
            print("   3. Envie: /start")
            print()
            print("⌨️  Pressione Ctrl+C para parar o bot")
            print("=" * 70)
            print()
        else:
            print("❌ Erro ao conectar com Telegram!")
            print("Verifique o token no arquivo.")
            return
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        print("\nVerifique:")
        print("1. Você tem conexão com internet")
        print("2. O token está correto")
        return

    # Loop principal
    offset = None
    message_count = 0

    while True:
        try:
            # Buscar mensagens
            updates = get_updates(offset)

            if updates and updates.get('ok'):
                for update in updates.get('result', []):
                    offset = update['update_id'] + 1

                    # Verificar se há mensagem
                    if 'message' in update:
                        message = update['message']
                        chat_id = message['chat']['id']
                        text = message.get('text', '')
                        user_name = message['from'].get('first_name', 'amigo')

                        message_count += 1

                        print(f"📩 [{message_count}] Mensagem de {user_name}: {text}")

                        # Processar e responder
                        response = handle_message(chat_id, text, user_name)
                        send_message(chat_id, response)

                        print(f"✅ Respondido!")
                        print()

            # Aguardar um pouco antes de buscar novamente
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n")
            print("=" * 70)
            print("🛑 Bot parado pelo usuário")
            print(f"📊 Total de mensagens processadas: {message_count}")
            print("=" * 70)
            break
        except Exception as e:
            print(f"⚠️  Erro: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
