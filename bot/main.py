"""
ChicoIA Telegram Bot - Main entry point
"""

import os
import sys
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from bot.gemini_service import GeminiService
from bot.database import DatabaseManager
from bot.onboarding import OnboardingManager
from bot.handlers import BotHandlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('chicobot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def load_environment():
    """Load environment variables"""
    load_dotenv()

    required_vars = ['TELEGRAM_BOT_TOKEN', 'GEMINI_API_KEY', 'DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    return {
        'telegram_token': os.getenv('TELEGRAM_BOT_TOKEN'),
        'gemini_key': os.getenv('GEMINI_API_KEY'),
        'database_url': os.getenv('DATABASE_URL'),
        'platform_url': os.getenv('PLATFORM_URL', 'https://chicoia.com.br')
    }


def main():
    """Main function to run the bot"""
    logger.info("Starting ChicoIA Telegram Bot...")

    # Load environment variables
    env = load_environment()

    try:
        # Initialize database
        logger.info("Initializing database...")
        db_manager = DatabaseManager(env['database_url'])
        db_manager.init_db()

        # Initialize Gemini service
        logger.info("Initializing Gemini AI service...")
        gemini_service = GeminiService(env['gemini_key'])

        # Initialize onboarding manager
        onboarding_manager = OnboardingManager(db_manager)

        # Initialize handlers
        handlers = BotHandlers(gemini_service, db_manager, onboarding_manager)

        # Create application
        application = Application.builder().token(env['telegram_token']).build()

        # Register command handlers
        application.add_handler(CommandHandler("start", handlers.start_command))
        application.add_handler(CommandHandler("ajuda", handlers.help_command))
        application.add_handler(CommandHandler("analisar", handlers.analyze_command))
        application.add_handler(CommandHandler("palpites", handlers.tips_command))
        application.add_handler(CommandHandler("meusdados", handlers.mydata_command))
        application.add_handler(CommandHandler("premium", handlers.premium_command))

        # Register message handler (for free-form conversations)
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handlers.handle_message
        ))

        # Register callback query handler (for inline keyboard buttons)
        application.add_handler(CallbackQueryHandler(handlers.handle_callback_query))

        # Register error handler
        application.add_error_handler(handlers.error_handler)

        # Start bot
        logger.info("Bot started successfully! Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
