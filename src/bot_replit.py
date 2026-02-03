#!/usr/bin/env python3
"""
ChicoIA Telegram Bot - Deploy Render com proteção anti-conflito
"""

import os
import logging
import threading
import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import google.generativeai as genai

# Configuração
TELEGRAM_BOT_TOKEN = "8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE"
GEMINI_API_KEY = "AIzaSyCE0Bw-t0LsMacnxt-FjajyuHBzYiVNBaA"
BOT_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Flask app para Health Check
app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

@app.route("/health")
def health():
    return "OK", 200

# System Prompt
SYSTEM_PROMPT = """Você é o Chico, assistente virtual da ChicoIA - plataforma de apostas esportivas.
Você é empático, direto e parceiro estratégico.
Fala em português brasileiro de forma natural e leve.
Ajuda usuários a tomar decisões melhores em apostas esportivas.
Nunca dá garantias absolutas.
Sempre sugere ver a plataforma completa em chicoia.com.br"""

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"🎯 E aí, {user_name}! Sou o Chico, seu parceiro estratégico na ChicoIA!\n\n"
        "Posso te ajudar com:\n"
        "⚽ Análise de jogos\n"
        "📊 Sugestões de apostas\n"
        "💡 Dicas de estratégia\n\n"
        "Me conta, qual jogo você quer analisar?"
    )

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Comandos:\n\n"
        "/start - Começar\n"
        "/ajuda - Ajuda\n"
        "/analisar - Analisar jogo\n"
        "/palpites - Palpites\n\n"
        "Ou mande uma mensagem! 😊"
    )

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        user_name = update.effective_user.first_name
        logger.info(f"Mensagem de {user_name}: {user_text}")

        prompt = f"{SYSTEM_PROMPT}\n\nUsuário: {user_text}\n\nResponda:"
        response = model.generate_content(prompt)

        await update.message.reply_text(response.text)
        logger.info(f"Resposta enviada")

    except Exception as e:
        logger.error(f"Erro: {e}")
        await update.message.reply_text("Tive um problema. Tenta de novo! 😅")

def cleanup_telegram():
    """LIMPA TUDO - webhooks, updates pendentes, conexões antigas"""
    logger.info("🧹 LIMPANDO CONEXÕES ANTIGAS...")

    try:
        # 1. Deletar webhook
        logger.info("Deletando webhook...")
        response = requests.post(
            f"{BOT_API_URL}/deleteWebhook",
            json={"drop_pending_updates": True},
            timeout=10
        )
        logger.info(f"Webhook: {response.json()}")

        # 2. Limpar fila de updates
        logger.info("Limpando updates pendentes...")
        response = requests.post(
            f"{BOT_API_URL}/getUpdates",
            json={"offset": -1, "timeout": 1},
            timeout=5
        )
        logger.info(f"Updates limpos: {response.json()}")

        # 3. Aguardar um pouco
        time.sleep(2)
        logger.info("✅ Limpeza completa!")

    except Exception as e:
        logger.warning(f"Erro na limpeza (ignorando): {e}")

def start_flask():
    """Flask para Health Check"""
    port = int(os.getenv('PORT', 8080))
    logger.info(f"Flask iniciando na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def main():
    """Função principal"""
    logger.info("=" * 60)
    logger.info("🤖 ChicoIA Bot - RENDER DEPLOY")
    logger.info("=" * 60)

    # PASSO 1: Aguardar 15 segundos (processo antigo morrer)
    logger.info("⏳ Aguardando 15s para processo antigo encerrar...")
    time.sleep(15)

    # PASSO 2: Limpar TUDO do Telegram
    cleanup_telegram()

    # PASSO 3: Iniciar Flask
    logger.info("🌐 Iniciando Flask Health Check...")
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    time.sleep(2)

    # PASSO 4: Criar bot
    logger.info("⚙️  Criando application...")
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # PASSO 5: Registrar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", ajuda))
    application.add_handler(CommandHandler("analisar", mensagem))
    application.add_handler(CommandHandler("palpites", mensagem))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
    logger.info("✅ Handlers registrados")

    # PASSO 6: Iniciar polling
    logger.info("🚀 INICIANDO POLLING...")
    logger.info("=" * 60)

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot parado")
    except Exception as e:
        logger.error(f"ERRO FATAL: {e}")
        raise
