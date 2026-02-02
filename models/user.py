"""
User model for ChicoIA Telegram bot
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User data model"""

    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    joined_at: datetime = None
    last_interaction: datetime = None
    onboarding_day: int = 1
    is_premium: bool = False
    opted_in_alerts: bool = False

    def __post_init__(self):
        """Initialize timestamps if not provided"""
        if self.joined_at is None:
            self.joined_at = datetime.utcnow()
        if self.last_interaction is None:
            self.last_interaction = datetime.utcnow()

    @property
    def display_name(self) -> str:
        """Get user's display name"""
        if self.first_name:
            return self.first_name
        elif self.username:
            return self.username
        else:
            return f"User {self.telegram_id}"

    def should_receive_onboarding(self) -> bool:
        """Check if user should receive onboarding messages"""
        return self.onboarding_day <= 7

    def advance_onboarding(self):
        """Move user to next onboarding day"""
        if self.onboarding_day < 7:
            self.onboarding_day += 1
        else:
            self.onboarding_day = 8  # Mark as completed

    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None,
            'onboarding_day': self.onboarding_day,
            'is_premium': self.is_premium,
            'opted_in_alerts': self.opted_in_alerts,
        }
