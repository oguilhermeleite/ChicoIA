"""
Onboarding flow for ChicoIA Telegram bot
"""

import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.prompts import ONBOARDING_MESSAGES
from bot.database import DatabaseManager

logger = logging.getLogger(__name__)


class OnboardingManager:
    """Manages user onboarding flow"""

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize onboarding manager

        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager

    async def send_welcome_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Send welcome message with lead magnet

        Args:
            update: Telegram update
            context: Callback context
        """
        try:
            user = update.effective_user

            # Create or update user in database
            self.db.create_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name
            )

            # Send welcome message
            welcome_text = ONBOARDING_MESSAGES[1]

            # Add lead magnet
            lead_magnet_text = "\n\n🎁 *Quer receber alertas gratuitos de value bets toda vez que identifico?*"

            keyboard = [
                [
                    InlineKeyboardButton("✅ Sim, quero alertas!", callback_data="optin_alerts"),
                    InlineKeyboardButton("🌐 Ver plataforma", url="https://chicoia.com.br")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                welcome_text + lead_magnet_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )

            logger.info(f"Welcome message sent to user {user.id}")

        except Exception as e:
            logger.error(f"Error sending welcome message: {e}")
            await update.message.reply_text(
                "Opa! Bem-vindo à ChicoIA! Tô aqui pra te ajudar com apostas esportivas. "
                "Use /ajuda pra ver o que posso fazer por você! 😊"
            )

    async def handle_alert_optin(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Handle user opting in for alerts

        Args:
            update: Telegram update
            context: Callback context
        """
        query = update.callback_query
        await query.answer()

        try:
            user_id = query.from_user.id
            self.db.set_alert_preference(user_id, True)

            await query.edit_message_text(
                "🎉 *Perfeito!*\n\n"
                "Você vai receber alertas sempre que eu identificar value bets interessantes!\n\n"
                "Enquanto isso, me conta: tem algum jogo que você quer analisar hoje? "
                "É só me falar o nome dos times ou usar /palpites pra ver minhas sugestões!",
                parse_mode='Markdown'
            )

            logger.info(f"User {user_id} opted in for alerts")

        except Exception as e:
            logger.error(f"Error handling alert opt-in: {e}")
            await query.edit_message_text(
                "Pronto! Você vai receber meus alertas de value bets! 🎯"
            )

    async def send_onboarding_message(
        self,
        telegram_id: int,
        day: int,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Send onboarding message for specific day

        Args:
            telegram_id: Telegram user ID
            day: Onboarding day (1-7)
            context: Callback context
        """
        try:
            if day not in ONBOARDING_MESSAGES:
                logger.warning(f"No onboarding message for day {day}")
                return

            message = ONBOARDING_MESSAGES[day]

            # Add special buttons for certain days
            reply_markup = None

            if day == 7:  # Premium promotion
                keyboard = [
                    [InlineKeyboardButton("🌟 Conhecer Premium", callback_data="premium_info")],
                    [InlineKeyboardButton("📊 Ver palpites", callback_data="daily_tips")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=telegram_id,
                text=message,
                reply_markup=reply_markup
            )

            # Update onboarding day in database
            self.db.update_onboarding_day(telegram_id, day + 1)

            logger.info(f"Onboarding day {day} message sent to user {telegram_id}")

        except Exception as e:
            logger.error(f"Error sending onboarding message: {e}")

    async def handle_premium_info(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Handle premium info request

        Args:
            update: Telegram update
            context: Callback context
        """
        query = update.callback_query
        await query.answer()

        premium_text = """🌟 *ChicoIA Premium* 🌟

Com o Premium você leva suas apostas para o próximo nível:

✨ *Alertas em Tempo Real*
Receba notificações instantâneas de value bets identificadas

📊 *Análises Profundas*
Estatísticas avançadas, histórico completo e padrões de jogo

💰 *Gestão Automática de Banca*
Ferramentas para gerenciar seu bankroll de forma profissional

📈 *Histórico Completo*
Acompanhe todas suas apostas e analise seu desempenho

🎯 *Suporte Prioritário*
Tire dúvidas diretamente com analistas especializados

*Usuários Premium têm 34% mais lucro em média!*

💳 *A partir de R$ 49,90/mês*

Quer conhecer? Acesse: https://chicoia.com.br/premium

Alguma dúvida? É só perguntar! 😊"""

        keyboard = [
            [InlineKeyboardButton("🚀 Assinar Premium", url="https://chicoia.com.br/premium")],
            [InlineKeyboardButton("❓ Tenho dúvidas", callback_data="premium_questions")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            premium_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    async def handle_premium_questions(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Handle premium questions

        Args:
            update: Telegram update
            context: Callback context
        """
        query = update.callback_query
        await query.answer()

        await query.edit_message_text(
            "Pode perguntar o que quiser sobre o Premium! Tô aqui pra te ajudar. 😊\n\n"
            "Me manda tua dúvida que eu explico tudo direitinho!"
        )
