"""
Command and message handlers for ChicoIA Telegram bot
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.gemini_service import GeminiService
from bot.database import DatabaseManager
from bot.onboarding import OnboardingManager

logger = logging.getLogger(__name__)


class BotHandlers:
    """Handlers for bot commands and messages"""

    def __init__(
        self,
        gemini_service: GeminiService,
        db_manager: DatabaseManager,
        onboarding_manager: OnboardingManager
    ):
        """
        Initialize bot handlers

        Args:
            gemini_service: Gemini AI service
            db_manager: Database manager
            onboarding_manager: Onboarding manager
        """
        self.gemini = gemini_service
        self.db = db_manager
        self.onboarding = onboarding_manager

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command

        Args:
            update: Telegram update
            context: Callback context
        """
        await self.onboarding.send_welcome_message(update, context)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /ajuda command

        Args:
            update: Telegram update
            context: Callback context
        """
        help_text = """🤖 *Comandos disponíveis:*

/start - Começar conversa com o Chico
/ajuda - Ver esta mensagem de ajuda
/analisar [time1] vs [time2] - Analisar jogo específico
/palpites - Ver sugestões de apostas do dia
/meusdados - Ver suas estatísticas e histórico
/premium - Conhecer ChicoIA Premium

💬 *Conversação livre:*
Você também pode conversar comigo normalmente! É só me mandar uma mensagem perguntando sobre qualquer jogo ou aspecto de apostas esportivas.

Exemplos:
• "Quero analisar Flamengo x Palmeiras"
• "Como funciona over/under?"
• "Dicas de gestão de banca"

Tô aqui pra te ajudar! 🎯"""

        await update.message.reply_text(help_text, parse_mode='Markdown')
        logger.info(f"Help command used by user {update.effective_user.id}")

    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /analisar command

        Args:
            update: Telegram update
            context: Callback context
        """
        try:
            user_id = update.effective_user.id

            # Get match info from command args
            if context.args:
                match_info = " ".join(context.args)
            else:
                await update.message.reply_text(
                    "Me diz qual jogo você quer analisar!\n\n"
                    "Exemplo: /analisar Flamengo vs Palmeiras"
                )
                return

            # Send typing action
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

            # Get analysis from Gemini
            analysis = await self.gemini.analyze_match(match_info)

            # Save conversation
            self.db.save_conversation(user_id, "user", f"/analisar {match_info}")
            self.db.save_conversation(user_id, "assistant", analysis)

            # Send analysis
            await update.message.reply_text(analysis)

            logger.info(f"Match analysis for '{match_info}' sent to user {user_id}")

        except Exception as e:
            logger.error(f"Error in analyze command: {e}")
            await update.message.reply_text(
                "Ops, tive um probleminha ao analisar esse jogo. Pode tentar de novo? 🤔"
            )

    async def tips_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /palpites command

        Args:
            update: Telegram update
            context: Callback context
        """
        try:
            user_id = update.effective_user.id

            # Send typing action
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

            # Get daily tips from Gemini
            tips = await self.gemini.get_daily_tips()

            # Save conversation
            self.db.save_conversation(user_id, "user", "/palpites")
            self.db.save_conversation(user_id, "assistant", tips)

            # Send tips
            await update.message.reply_text(tips)

            logger.info(f"Daily tips sent to user {user_id}")

        except Exception as e:
            logger.error(f"Error in tips command: {e}")
            await update.message.reply_text(
                "Ops, tive um problema ao buscar os palpites. Tenta de novo em alguns segundos? 😅"
            )

    async def mydata_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /meusdados command

        Args:
            update: Telegram update
            context: Callback context
        """
        try:
            user_id = update.effective_user.id
            user = self.db.get_user(user_id)

            if not user:
                await update.message.reply_text(
                    "Ops, não encontrei seus dados. Use /start para começar!"
                )
                return

            # Get conversation count
            history = self.db.get_conversation_history(user_id, limit=1000)
            conversation_count = len(history) // 2  # Divide by 2 for message pairs

            user_data_text = f"""📊 *Seus Dados na ChicoIA*

👤 Nome: {user.first_name or 'Não informado'}
📅 Membro desde: {user.joined_at.strftime('%d/%m/%Y')}
💬 Conversas: {conversation_count} análises
{'🌟 Status: Premium' if user.is_premium else '⚡ Status: Free'}
{'🔔 Alertas: Ativados' if user.opted_in_alerts else '🔕 Alertas: Desativados'}

{'' if user.is_premium else '💡 *Dica:* Usuários Premium têm acesso a análises avançadas e alertas em tempo real! Use /premium para conhecer.'}
"""

            keyboard = []
            if not user.is_premium:
                keyboard.append([InlineKeyboardButton("🌟 Conhecer Premium", callback_data="premium_info")])

            if not user.opted_in_alerts:
                keyboard.append([InlineKeyboardButton("🔔 Ativar Alertas", callback_data="optin_alerts")])

            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

            await update.message.reply_text(
                user_data_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )

            logger.info(f"User data displayed for user {user_id}")

        except Exception as e:
            logger.error(f"Error in mydata command: {e}")
            await update.message.reply_text(
                "Ops, tive um problema ao buscar seus dados. Tenta de novo? 🤔"
            )

    async def premium_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /premium command

        Args:
            update: Telegram update
            context: Callback context
        """
        await self.onboarding.handle_premium_info(update, context)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle regular text messages

        Args:
            update: Telegram update
            context: Callback context
        """
        try:
            user_id = update.effective_user.id
            user_message = update.message.text

            # Update user interaction time
            self.db.create_user(
                telegram_id=user_id,
                username=update.effective_user.username,
                first_name=update.effective_user.first_name
            )

            # Send typing action
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

            # Get conversation history
            history = self.db.get_conversation_history(user_id, limit=10)

            # Get response from Gemini
            response = await self.gemini.get_response(user_message, history)

            # Save conversation
            self.db.save_conversation(user_id, "user", user_message)
            self.db.save_conversation(user_id, "assistant", response)

            # Send response
            await update.message.reply_text(response)

            logger.info(f"Message handled for user {user_id}")

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "Desculpa, tive um problema aqui. Pode tentar de novo? 🙏"
            )

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle callback queries from inline keyboards

        Args:
            update: Telegram update
            context: Callback context
        """
        query = update.callback_query
        data = query.data

        try:
            if data == "optin_alerts":
                await self.onboarding.handle_alert_optin(update, context)

            elif data == "premium_info":
                await self.onboarding.handle_premium_info(update, context)

            elif data == "premium_questions":
                await self.onboarding.handle_premium_questions(update, context)

            elif data == "daily_tips":
                await query.answer()
                user_id = query.from_user.id

                # Send typing action
                await context.bot.send_chat_action(chat_id=query.message.chat_id, action="typing")

                # Get daily tips
                tips = await self.gemini.get_daily_tips()

                # Save conversation
                self.db.save_conversation(user_id, "user", "Ver palpites do dia")
                self.db.save_conversation(user_id, "assistant", tips)

                # Send tips
                await query.message.reply_text(tips)

            else:
                await query.answer("Opção não reconhecida")

        except Exception as e:
            logger.error(f"Error handling callback query: {e}")
            await query.answer("Ops, tive um problema. Tenta de novo?")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle errors

        Args:
            update: Telegram update
            context: Callback context
        """
        logger.error(f"Update {update} caused error {context.error}")

        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Desculpa, aconteceu um erro inesperado. Tenta de novo em alguns segundos? 🙏"
            )
