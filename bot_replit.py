import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading
import google.generativeai as genai

# Config
TELEGRAM_BOT_TOKEN = "8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE"
GEMINI_API_KEY = "AIzaSyCE0Bw-t0LsMacnxt-FjajyuHBzYiVNBaA"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Flask app to keep alive on Render (Health Check)
app = Flask(__name__)

@app.route("/")
def home():
    return "ChicoIA Bot is running!"

@app.route("/healthz")
def health():
    return "OK", 200

# Chico system prompt
SYSTEM_PROMPT = """Você é o Chico, assistente virtual da ChicoIA - plataforma de apostas esportivas.
Você é empático, direto e parceiro estratégico.
Fala em português brasileiro de forma natural e leve.
Ajuda usuários a tomar decisões melhores em apostas esportivas.
Nunca dá garantias absolutas.
Sempre sugere ver a plataforma completa em chicoia.com.br"""

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para comando /start"""
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"🎯 E aí, {user_name}! Sou o Chico, seu parceiro estratégico na ChicoIA!\n\n"
        "Posso te ajudar com:\n"
        "⚽ Análise de jogos\n"
        "📊 Sugestões de apostas\n"
        "💡 Dicas de estratégia\n\n"
        "Me conta, qual jogo você quer analisar?"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para comando /ajuda"""
    await update.message.reply_text(
        "📌 Comandos disponíveis:\n\n"
        "/start - Começar conversa\n"
        "/ajuda - Ver essa lista\n"
        "/analisar - Analisar um jogo\n"
        "/palpites - Palpites de hoje\n\n"
        "Ou é só me mandar uma mensagem! 😊"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensagens de texto"""
    try:
        user_message = update.message.text
        user_name = update.effective_user.first_name
        logger.info(f"Mensagem de {user_name}: {user_message}")

        # Call Gemini
        prompt = f"{SYSTEM_PROMPT}\n\nUsuário: {user_message}\n\nResponda de forma natural e útil:"
        response = model.generate_content(prompt)

        await update.message.reply_text(response.text)
        logger.info(f"Resposta enviada para {user_name}")

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        await update.message.reply_text(
            "Ei, tive um problema aqui. Tenta de novo daqui a pouco! 😅"
        )

def run_bot():
    """Inicializa e roda o bot usando python-telegram-bot v20+"""
    logger.info("Inicializando ChicoIA Telegram Bot...")

    # Criar application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Adicionar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", help_command))
    application.add_handler(CommandHandler("analisar", handle_message))
    application.add_handler(CommandHandler("palpites", handle_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot handlers registrados")
    logger.info("Iniciando polling...")

    # Rodar bot com polling (sintaxe v20+)
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

def run_flask():
    """Roda servidor Flask para Health Check do Render"""
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Iniciando Flask na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    logger.info("=== ChicoIA Bot - Iniciando ===")

    # Rodar Flask em thread separada (para Health Check do Render)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask thread iniciada")

    # Rodar bot na thread principal
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Bot encerrado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        raise
