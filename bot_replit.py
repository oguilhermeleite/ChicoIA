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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Flask app to keep alive on Render
app = Flask(__name__)

@app.route("/")
def home():
    return "ChicoIA Bot is running!"

@app.route("/healthz")
def health():
    return "OK"

# Chico system prompt
SYSTEM_PROMPT = """Você é o Chico, assistente virtual da ChicoIA - plataforma de apostas esportivas.
Você é empático, direto e parceiro estratégico.
Fala em português brasileiro de forma natural e leve.
Ajuda usuários a tomar decisões melhores em apostas esportivas.
Nunca dá garantias absolutas.
Sempre sugere ver a plataforma completa em chicoia.com.br"""

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 E aí! Sou o Chico, seu parceiro estratégico na ChicoIA!\n\n"
        "Posso te ajudar com:\n"
        "⚽ Análise de jogos\n"
        "📊 Sugestões de apostas\n"
        "💡 Dicas de estratégia\n\n"
        "Me conta, qual jogo você quer analisar?"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Comandos disponíveis:\n\n"
        "/start - Começar conversa\n"
        "/ajuda - Ver essa lista\n"
        "/analisar - Analisar um jogo\n"
        "/palpites - Palpites de hoje\n\n"
        "Ou é só me mandar uma mensagem! 😊"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text
        logger.info(f"Mensagem de {update.message.user.first_name}: {user_message}")

        # Call Gemini
        prompt = f"{SYSTEM_PROMPT}\n\nUsuário: {user_message}\n\nResponda de forma natural e útil:"
        response = model.generate_content(prompt)

        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Erro: {e}")
        await update.message.reply_text("Ei, tive um problema aqui. Tenta de novo daqui a pouco! 😅")

# Bot setup
async def run_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", help_command))
    application.add_handler(CommandHandler("analisar", handle_message))
    application.add_handler(CommandHandler("palpites", handle_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.start()
    await application.updater.start()
    await application.updater.stop()
    await application.stop()

# Main - Run Flask + Bot together
if __name__ == "__main__":
    import asyncio

    # Run bot in background thread
    def start_bot():
        asyncio.run(run_bot())

    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    # Run Flask (keeps Render alive)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
