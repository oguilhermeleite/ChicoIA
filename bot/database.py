"""
Database connection and operations for ChicoIA Telegram bot
"""

import os
import logging
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy import create_engine, Column, BigInteger, String, Integer, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import asyncpg

logger = logging.getLogger(__name__)

Base = declarative_base()


class TelegramUser(Base):
    """Telegram user model"""
    __tablename__ = 'telegram_users'

    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)
    onboarding_day = Column(Integer, default=1)
    is_premium = Column(Boolean, default=False)
    opted_in_alerts = Column(Boolean, default=False)


class Conversation(Base):
    """Conversation history model"""
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Database manager for ChicoIA bot"""

    def __init__(self, database_url: str):
        """
        Initialize database manager

        Args:
            database_url: PostgreSQL connection URL
        """
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None

        try:
            self.engine = create_engine(database_url)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def init_db(self):
        """Initialize database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error creating database tables: {e}")
            raise

    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()

    def create_user(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None
    ) -> TelegramUser:
        """
        Create or update user

        Args:
            telegram_id: Telegram user ID
            username: Telegram username
            first_name: User's first name

        Returns:
            TelegramUser object
        """
        session = self.get_session()
        try:
            user = session.query(TelegramUser).filter_by(telegram_id=telegram_id).first()

            if user:
                # Update existing user
                user.username = username
                user.first_name = first_name
                user.last_interaction = datetime.utcnow()
            else:
                # Create new user
                user = TelegramUser(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name
                )
                session.add(user)

            session.commit()
            session.refresh(user)
            logger.info(f"User {telegram_id} created/updated")
            return user

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error creating/updating user: {e}")
            raise
        finally:
            session.close()

    def get_user(self, telegram_id: int) -> Optional[TelegramUser]:
        """
        Get user by telegram ID

        Args:
            telegram_id: Telegram user ID

        Returns:
            TelegramUser object or None
        """
        session = self.get_session()
        try:
            user = session.query(TelegramUser).filter_by(telegram_id=telegram_id).first()
            return user
        except SQLAlchemyError as e:
            logger.error(f"Error getting user: {e}")
            return None
        finally:
            session.close()

    def update_onboarding_day(self, telegram_id: int, day: int):
        """
        Update user's onboarding day

        Args:
            telegram_id: Telegram user ID
            day: Onboarding day number
        """
        session = self.get_session()
        try:
            user = session.query(TelegramUser).filter_by(telegram_id=telegram_id).first()
            if user:
                user.onboarding_day = day
                session.commit()
                logger.info(f"Updated onboarding day for user {telegram_id} to {day}")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error updating onboarding day: {e}")
        finally:
            session.close()

    def set_alert_preference(self, telegram_id: int, opted_in: bool):
        """
        Set user's alert preference

        Args:
            telegram_id: Telegram user ID
            opted_in: Whether user opted in for alerts
        """
        session = self.get_session()
        try:
            user = session.query(TelegramUser).filter_by(telegram_id=telegram_id).first()
            if user:
                user.opted_in_alerts = opted_in
                session.commit()
                logger.info(f"Alert preference for user {telegram_id} set to {opted_in}")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error setting alert preference: {e}")
        finally:
            session.close()

    def save_conversation(self, telegram_id: int, role: str, message: str):
        """
        Save conversation message

        Args:
            telegram_id: Telegram user ID
            role: Message role ('user' or 'assistant')
            message: Message content
        """
        session = self.get_session()
        try:
            conversation = Conversation(
                telegram_id=telegram_id,
                role=role,
                message=message
            )
            session.add(conversation)
            session.commit()
            logger.debug(f"Saved {role} message for user {telegram_id}")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error saving conversation: {e}")
        finally:
            session.close()

    def get_conversation_history(
        self,
        telegram_id: int,
        limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Get conversation history for user

        Args:
            telegram_id: Telegram user ID
            limit: Maximum number of messages to retrieve

        Returns:
            List of conversation messages
        """
        session = self.get_session()
        try:
            conversations = (
                session.query(Conversation)
                .filter_by(telegram_id=telegram_id)
                .order_by(Conversation.created_at.desc())
                .limit(limit)
                .all()
            )

            # Reverse to get chronological order
            history = [
                {"role": conv.role, "content": conv.message}
                for conv in reversed(conversations)
            ]

            return history

        except SQLAlchemyError as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
        finally:
            session.close()

    def get_users_for_onboarding(self, day: int) -> List[int]:
        """
        Get users who should receive onboarding message for specific day

        Args:
            day: Onboarding day number

        Returns:
            List of telegram IDs
        """
        session = self.get_session()
        try:
            users = (
                session.query(TelegramUser.telegram_id)
                .filter_by(onboarding_day=day)
                .all()
            )
            return [user[0] for user in users]
        except SQLAlchemyError as e:
            logger.error(f"Error getting users for onboarding: {e}")
            return []
        finally:
            session.close()

    def get_opted_in_users(self) -> List[int]:
        """
        Get users who opted in for alerts

        Returns:
            List of telegram IDs
        """
        session = self.get_session()
        try:
            users = (
                session.query(TelegramUser.telegram_id)
                .filter_by(opted_in_alerts=True)
                .all()
            )
            return [user[0] for user in users]
        except SQLAlchemyError as e:
            logger.error(f"Error getting opted-in users: {e}")
            return []
        finally:
            session.close()
