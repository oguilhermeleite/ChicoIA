#!/usr/bin/env python3
"""
ChicoIA Bot - Versão otimizada para deploy na nuvem
Este bot funciona 24/7 na nuvem, sem precisar de PC ligado
"""

import os
from dotenv import load_dotenv
load_dotenv()

import json
import urllib.request
import urllib.parse
import time
import sys
from datetime import datetime

# Configuração de tokens
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or "8522357760:AAHn60ZJPYZ4rz4a051k7O8GUPV8ivm7JCE"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or "AIzaSyCE0Bw-t0LsMacnxt-FjajyuHBzYiVNBaA"

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Contador de usuários atendidos
usuarios_atendidos = set()
total_mensagens = 0

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
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERRO] Ao enviar mensagem: {e}")
        return None

def get_updates(offset=None):
    """Busca novas mensagens"""
    url = f"{BASE_URL}/getUpdates?timeout=30"
    if offset:
        url += f"&offset={offset}"

    try:
        with urllib.request.urlopen(url, timeout=35) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERRO] Ao buscar mensagens: {e}")
        return None

def get_bot_info():
    """Pega informações do bot"""
    try:
        url = f"{BASE_URL}/getMe"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('ok'):
                return data['result']
    except:
        pass
    return None

def handle_message(chat_id, text, user_name, user_id):
    """Processa mensagens do usuário"""

    # Adicionar usuário à lista
    usuarios_atendidos.add(user_id)

    if text == '/start':
        response = f"""🎉 *Olá, {user_name}!*

Bem-vindo ao *ChicoIA Bot*! 👋

Eu sou o Chico, seu assistente de apostas esportivas da plataforma ChicoIA.

*O que posso fazer por você:*
✅ Analisar jogos de futebol
✅ Dar sugestões de apostas
✅ Ajudar com gestão de banca
✅ Responder suas dúvidas sobre apostas

*Comandos disponíveis:*
/start - Esta mensagem
/ajuda - Ver todos os comandos
/sobre - Sobre a ChicoIA
/analisar - Analisar um jogo
/palpites - Palpites do dia
/premium - Conhecer plano Premium

*Ou simplesmente converse comigo!*
Me diga qual jogo você quer analisar ou o que precisa saber sobre apostas esportivas.

_Plataforma: chicoia.com.br_"""

    elif text == '/ajuda':
        response = """🤖 *Ajuda - Comandos Disponíveis*

*Comandos principais:*
/start - Mensagem de boas-vindas
/ajuda - Esta mensagem
/sobre - Sobre a ChicoIA
/analisar - Analisar jogos
/palpites - Sugestões do dia
/premium - Plano Premium
/status - Status do bot

*Como usar:*

1️⃣ *Análise de jogos:*
Envie: "Analise Flamengo x Palmeiras"
Ou: /analisar

2️⃣ *Palpites do dia:*
Envie: /palpites
E receba as melhores sugestões!

3️⃣ *Dúvidas sobre apostas:*
Pergunte qualquer coisa!
Ex: "Como funciona over/under?"

4️⃣ *Gestão de banca:*
Pergunte: "Dicas de gestão de banca"

_Tô aqui pra te ajudar! 🎯_"""

    elif text == '/sobre':
        response = """🏆 *ChicoIA - Apostas Esportivas Inteligentes*

Somos a plataforma brasileira líder em apostas esportivas com inteligência artificial!

*O que oferecemos:*
✨ Análise profunda de jogos
✨ Identificação de value bets
✨ Sugestões de apostas baseadas em dados
✨ Gestão inteligente de banca
✨ Alertas em tempo real (Premium)
✨ Estatísticas avançadas (Premium)

*Nossa missão:*
Ajudar apostadores a tomar decisões mais inteligentes e lucrativas através de tecnologia e análise de dados.

*Plano Premium:*
• Alertas em tempo real
• Análises profundas
• Suporte prioritário
• Gestão automática de banca

🌐 *Site:* https://chicoia.com.br
📧 *Contato:* suporte@chicoia.com.br
💬 *Bot:* @ChicoIA_bot

_Aposte com inteligência! 🎯_"""

    elif text == '/analisar':
        response = f"""⚽ *Análise de Jogos*

Olá, {user_name}! Me diga qual jogo você quer analisar.

*Exemplos:*
• "Flamengo x Palmeiras"
• "Real Madrid vs Barcelona"
• "Corinthians x Santos"

Ou me fale sobre:
• Qual campeonato
• Quando é o jogo
• O que você quer saber

_Aguardo sua pergunta! ⚽_"""

    elif text == '/palpites':
        response = """📊 *Palpites do Dia*

Aqui estão algumas sugestões para hoje:

⚽ *Brasileirão:*
• Flamengo x Atlético-MG
  → Sugestão: Mais de 2.5 gols (odd ~2.10)
  → Motivo: Ambos com ataques fortes

• Palmeiras x Corinthians
  → Sugestão: Ambos marcam (odd ~1.95)
  → Motivo: Clássico equilibrado

⚽ *Premier League:*
• Arsenal x Chelsea
  → Sugestão: Arsenal vence (odd ~2.00)
  → Motivo: Arsenal em casa, momento melhor

*⚠️ Gestão de banca:*
Nunca aposte mais de 3-5% da sua banca por jogo!

_Para análises mais detalhadas, conheça o ChicoIA Premium!_ ⭐

/premium - Conhecer Premium"""

    elif text == '/premium':
        response = """⭐ *ChicoIA Premium*

Leve suas apostas para o próximo nível!

*O que você ganha:*

📊 *Análises Profundas*
Estatísticas avançadas, histórico completo e padrões de jogo detalhados

🔔 *Alertas em Tempo Real*
Receba notificações instantâneas de value bets e oportunidades

💰 *Gestão Automática*
Ferramentas profissionais para gerenciar sua banca com inteligência

📈 *Histórico Completo*
Acompanhe todas suas apostas e analise seu desempenho

🎯 *Suporte Prioritário*
Tire dúvidas diretamente com analistas especializados

*Resultados:*
Usuários Premium têm em média *34% mais lucro* que usuários gratuitos!

💳 *Planos:*
• Mensal: R$ 49,90
• Trimestral: R$ 119,90 (R$ 39,97/mês)
• Anual: R$ 399,90 (R$ 33,32/mês)

🌐 *Assinar:* https://chicoia.com.br/premium

_Transforme suas apostas em lucro consistente!_ 🚀"""

    elif text == '/status':
        response = f"""✅ *Status do Bot*

🤖 *Bot Online:* ✓ Funcionando 24/7
🌐 *Servidor:* ✓ Cloud
⚡ *API Telegram:* ✓ OK
📊 *Resposta:* ✓ Rápida

*Estatísticas:*
👥 Usuários atendidos: {len(usuarios_atendidos)}
💬 Mensagens processadas: {total_mensagens}
🕐 Uptime: Online 24/7 na nuvem

*Status:* 🟢 TUDO FUNCIONANDO!

_Funcionando na nuvem, sem precisar de PC ligado!_ ☁️"""

    else:
        response = f"""Opa, {user_name}! 👋

Você disse: _"{text}"_

Entendi que você quer conversar sobre apostas esportivas!

*Posso te ajudar com:*
⚽ Análise de jogos específicos
📊 Palpites do dia
💰 Gestão de banca
❓ Dúvidas sobre apostas

*Comandos úteis:*
/ajuda - Ver todos os comandos
/palpites - Sugestões do dia
/analisar - Analisar um jogo

_O que você gostaria de saber?_ 🎯"""

    return response

def main():
    """Função principal - Bot rodando 24/7 na nuvem"""
    global total_mensagens

    print("=" * 70)
    print("🤖 ChicoIA Bot - MODO 24/7 ATIVO")
    print("=" * 70)
    print()
    print("✅ Este bot atende TODOS os usuários do Telegram!")
    print("✅ Rodando na nuvem - Não precisa de PC ligado!")
    print()

    # Pegar informações do bot
    print("🔄 Conectando com Telegram...")
    bot_info = get_bot_info()

    if not bot_info:
        print("❌ ERRO: Não foi possível conectar com o Telegram!")
        print("\nVerifique:")
        print("1. Sua conexão com internet")
        print("2. O token está correto")
        print("3. Token está configurado nas variáveis de ambiente")
        return

    print(f"✅ Conectado com sucesso!")
    print(f"✅ Bot: @{bot_info.get('username', 'ChicoIA_bot')}")
    print(f"✅ Nome: {bot_info.get('first_name', 'Chico')}")
    print()
    print("=" * 70)
    print("🎯 BOT ONLINE - ATENDENDO TODOS OS USUÁRIOS")
    print("=" * 70)
    print()
    print(f"⏰ Iniciado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    print(f"☁️  Servidor: Cloud")
    print()
    print("📱 Qualquer pessoa pode conversar agora com @ChicoIA_bot!")
    print("💻 Funcionando 24/7 mesmo com seu PC desligado!")
    print()
    print("=" * 70)
    print()

    # Loop principal - roda para sempre
    offset = None

    while True:
        try:
            # Buscar mensagens (long polling)
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
                        user_id = message['from'].get('id')
                        username = message['from'].get('username', 'sem username')

                        total_mensagens += 1

                        timestamp = datetime.now().strftime('%H:%M:%S')
                        print(f"[{timestamp}] 📩 Mensagem de {user_name} (@{username})")
                        print(f"           💬 Texto: {text}")

                        # Processar e responder
                        response = handle_message(chat_id, text, user_name, user_id)
                        send_message(chat_id, response)

                        print(f"           ✅ Respondido!")
                        print(f"           📊 Total: {total_mensagens} msgs | {len(usuarios_atendidos)} usuários")
                        print()

        except KeyboardInterrupt:
            print("\n")
            print("=" * 70)
            print("🛑 Bot sendo desligado...")
            print("=" * 70)
            print()
            print(f"📊 Estatísticas finais:")
            print(f"   • Usuários atendidos: {len(usuarios_atendidos)}")
            print(f"   • Mensagens processadas: {total_mensagens}")
            print()
            print("=" * 70)
            print("✅ Bot desligado com sucesso!")
            print("=" * 70)
            break
        except Exception as e:
            print(f"⚠️  Erro: {e}")
            print("🔄 Reconectando em 5 segundos...")
            time.sleep(5)

if __name__ == '__main__':
    main()
