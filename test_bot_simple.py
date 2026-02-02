"""
Script de teste simples - Verifica se o bot consegue responder
SEM NECESSIDADE DE BANCO DE DADOS
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se python-telegram-bot está instalado
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    print("✓ python-telegram-bot instalado")
except ImportError:
    print("✗ python-telegram-bot NÃO instalado")
    print("\nInstale com: pip install python-telegram-bot")
    sys.exit(1)

# Pegar token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("✗ TELEGRAM_BOT_TOKEN não encontrado no .env")
    sys.exit(1)

print(f"✓ Token encontrado: {TOKEN[:20]}...")

# Handlers simples
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde ao comando /start"""
    user = update.effective_user
    welcome_message = f"""🎉 *Olá, {user.first_name}!*

Eu sou o Chico, assistente da ChicoIA! 👋

O bot está *FUNCIONANDO*! ✅

Comandos disponíveis:
• /start - Esta mensagem
• /ajuda - Ver ajuda
• /teste - Testar resposta

Envie qualquer mensagem e eu respondo!"""

    await update.message.reply_text(welcome_message, parse_mode='Markdown')
    print(f"✓ /start enviado para {user.first_name} (ID: {user.id})")


async def ajuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde ao comando /ajuda"""
    await update.message.reply_text(
        "🤖 *Comandos Disponíveis:*\n\n"
        "/start - Começar\n"
        "/ajuda - Esta mensagem\n"
        "/teste - Testar bot\n\n"
        "Envie qualquer mensagem e eu respondo!",
        parse_mode='Markdown'
    )


async def teste_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde ao comando /teste"""
    await update.message.reply_text(
        "✅ *Bot funcionando perfeitamente!*\n\n"
        "Token: Válido ✓\n"
        "Conexão: OK ✓\n"
        "Resposta: Rápida ✓\n\n"
        "Tudo pronto! 🎉",
        parse_mode='Markdown'
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a qualquer mensagem"""
    user_message = update.message.text
    user_name = update.effective_user.first_name

    response = f"""Opa, {user_name}! 👋

Você disse: "{user_message}"

Tô funcionando direitinho! O bot está *online* e respondendo.

Para integrar com o Gemini AI e banco de dados, use o bot completo em bot/main.py

Por enquanto, pode testar:
• /start
• /ajuda
• /teste"""

    await update.message.reply_text(response, parse_mode='Markdown')
    print(f"✓ Mensagem respondida para {user_name}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trata erros"""
    print(f"✗ Erro: {context.error}")


def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🤖 ChicoIA Bot - Teste Simples (SEM banco de dados)")
    print("="*60 + "\n")

    try:
        # Criar aplicação
        print("Criando aplicação...")
        application = Application.builder().token(TOKEN).build()

        # Adicionar handlers
        print("Adicionando handlers...")
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("ajuda", ajuda_command))
        application.add_handler(CommandHandler("teste", teste_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)

        # Iniciar bot
        print("\n✅ Bot iniciado com sucesso!")
        print(f"✅ Nome do bot: @ChicoIA_bot")
        print(f"✅ Aguardando mensagens...")
        print("\n" + "="*60)
        print("Abra o Telegram e envie /start para @ChicoIA_bot")
        print("Pressione Ctrl+C para parar")
        print("="*60 + "\n")

        # Rodar bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        print("\nVerifique:")
        print("1. Token do Telegram está correto no .env")
        print("2. python-telegram-bot está instalado")
        print("3. Você tem conexão com a internet")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Bot parado pelo usuário")
        sys.exit(0)
