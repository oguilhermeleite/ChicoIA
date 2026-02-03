#!/usr/bin/env python3
"""
ChicoIA Telegram Bot - Versão para deploy no Render
Usa python-telegram-bot v20+ com Flask para Health Check
"""

import os
import logging
import threading
import time
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import google.generativeai as genai

# Configuração
TELEGRAM_BOT_TOKEN = "8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE"
GEMINI_API_KEY = "AIzaSyCE0Bw-t0LsMacnxt-FjajyuHBzYiVNBaA"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Flask app para Health Check do Render
app = Flask(__name__)

@app.route("/")
def home():
    """Health check endpoint"""
    return "OK"

@app.route("/health")
def health():
    """Health check endpoint"""
    return "OK", 200

# System Prompt do Chico
SYSTEM_PROMPT = """Você é o Chico, assistente virtual da ChicoIA - plataforma de apostas esportivas.
Você é empático, direto e parceiro estratégico.
Fala em português brasileiro de forma natural e leve.
Ajuda usuários a tomar decisões melhores em apostas esportivas.
Nunca dá garantias absolutas.
Sempre sugere ver a plataforma completa em chicoia.com.br"""

# Handlers do Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler do comando /start"""
    user_name = update.effective_user.first_name
    message = (
        f"🎯 E aí, {user_name}! Sou o Chico, seu parceiro estratégico na ChicoIA!\n\n"
        "Posso te ajudar com:\n"
        "⚽ Análise de jogos\n"
        "📊 Sugestões de apostas\n"
        "💡 Dicas de estratégia\n\n"
        "Me conta, qual jogo você quer analisar?"
    )
    await update.message.reply_text(message)
    logger.info(f"Comando /start de {user_name}")

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler do comando /ajuda"""
    message = (
        "📌 Comandos disponíveis:\n\n"
        "/start - Começar conversa\n"
        "/ajuda - Ver essa lista\n"
        "/analisar - Analisar um jogo\n"
        "/palpites - Palpites de hoje\n\n"
        "Ou é só me mandar uma mensagem! 😊"
    )
    await update.message.reply_text(message)

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler de mensagens de texto"""
    try:
        user_text = update.message.text
        user_name = update.effective_user.first_name
        logger.info(f"Mensagem de {user_name}: {user_text}")

        # Gerar resposta com Gemini
        prompt = f"{SYSTEM_PROMPT}\n\nUsuário: {user_text}\n\nResponda de forma natural:"
        response = model.generate_content(prompt)

        await update.message.reply_text(response.text)
        logger.info(f"Resposta enviada para {user_name}")

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        await update.message.reply_text(
            "Ei, tive um problema aqui. Tenta de novo daqui a pouco! 😅"
        )

async def post_init(application):
    """Função executada após inicialização para limpar webhooks"""
    try:
        logger.info("Limpando webhooks antigos...")
        await application.bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhooks limpos com sucesso")
    except Exception as e:
        logger.warning(f"Erro ao limpar webhook: {e}")

def start_flask():
    """Inicia servidor Flask em thread separada"""
    port = int(os.getenv('PORT', 8080))
    logger.info(f"Iniciando Flask na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def main():
    """Função principal"""
    # ATRASO PROPOSITAL: Aguardar 10 segundos para Render matar processo antigo
    logger.info("=== ChicoIA Bot - Aguardando inicialização ===")
    logger.info("Aguardando 10 segundos para evitar conflitos de deploy...")
    time.sleep(10)
    logger.info("Iniciando bot agora...")

    # Iniciar Flask em thread separada (OBRIGATÓRIO para Render)
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask Health Check iniciado")

    # Criar e configurar bot
    logger.info("Configurando bot...")
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Registrar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", ajuda))
    application.add_handler(CommandHandler("analisar", mensagem))
    application.add_handler(CommandHandler("palpites", mensagem))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))

    logger.info("Handlers registrados")

    # Limpar webhook antes de iniciar polling (evita conflitos)
    logger.info("Preparando para limpar webhooks...")
    asyncio.run(post_init(application))

    logger.info("Iniciando polling...")

    # IMPORTANTE: Usar run_polling da versão 20+
    # NÃO usar updater.start() que é da versão 13
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot encerrado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        raise
