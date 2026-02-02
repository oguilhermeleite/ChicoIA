"""
Helper utility functions for ChicoIA Telegram bot
"""

import re
import logging
from typing import Tuple, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def parse_match_teams(match_str: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse team names from match string

    Args:
        match_str: Match string like "Flamengo vs Palmeiras" or "Flamengo x Palmeiras"

    Returns:
        Tuple of (team1, team2) or (None, None) if parsing fails
    """
    # Remove extra whitespace
    match_str = " ".join(match_str.split())

    # Try different separators
    separators = [' vs ', ' x ', ' VS ', ' X ']

    for sep in separators:
        if sep in match_str:
            teams = match_str.split(sep, 1)
            if len(teams) == 2:
                return teams[0].strip(), teams[1].strip()

    return None, None


def sanitize_message(message: str) -> str:
    """
    Sanitize user message for safe storage and processing

    Args:
        message: Raw user message

    Returns:
        Sanitized message
    """
    # Remove excessive whitespace
    message = " ".join(message.split())

    # Limit message length
    max_length = 1000
    if len(message) > max_length:
        message = message[:max_length] + "..."

    return message


def format_odds(odds: float) -> str:
    """
    Format odds for display

    Args:
        odds: Decimal odds value

    Returns:
        Formatted odds string
    """
    return f"{odds:.2f}"


def calculate_implied_probability(odds: float) -> float:
    """
    Calculate implied probability from decimal odds

    Args:
        odds: Decimal odds

    Returns:
        Implied probability as percentage
    """
    if odds <= 0:
        return 0.0

    return (1 / odds) * 100


def format_percentage(value: float) -> str:
    """
    Format percentage for display

    Args:
        value: Percentage value

    Returns:
        Formatted percentage string
    """
    return f"{value:.1f}%"


def is_valid_telegram_id(telegram_id: int) -> bool:
    """
    Validate Telegram user ID

    Args:
        telegram_id: Telegram user ID

    Returns:
        True if valid, False otherwise
    """
    # Telegram IDs are positive integers
    return isinstance(telegram_id, int) and telegram_id > 0


def extract_command_args(text: str, command: str) -> str:
    """
    Extract arguments from command text

    Args:
        text: Full message text
        command: Command name (without /)

    Returns:
        Command arguments
    """
    # Remove command prefix
    pattern = f"^/{command}\\s*"
    args = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return args.strip()


def format_datetime(dt: datetime) -> str:
    """
    Format datetime for display in Portuguese

    Args:
        dt: Datetime object

    Returns:
        Formatted datetime string
    """
    if dt is None:
        return "Não disponível"

    # Check if today
    now = datetime.now()
    if dt.date() == now.date():
        return f"Hoje às {dt.strftime('%H:%M')}"

    # Check if yesterday
    yesterday = now - timedelta(days=1)
    if dt.date() == yesterday.date():
        return f"Ontem às {dt.strftime('%H:%M')}"

    # Otherwise show full date
    return dt.strftime("%d/%m/%Y às %H:%M")


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def escape_markdown(text: str) -> str:
    """
    Escape special characters for Telegram MarkdownV2

    Args:
        text: Text to escape

    Returns:
        Escaped text
    """
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

    for char in special_chars:
        text = text.replace(char, f'\\{char}')

    return text


def is_brazilian_team(team_name: str) -> bool:
    """
    Check if team name is likely Brazilian

    Args:
        team_name: Team name

    Returns:
        True if likely Brazilian team
    """
    brazilian_teams = [
        'flamengo', 'palmeiras', 'corinthians', 'são paulo', 'santos',
        'grêmio', 'internacional', 'atlético', 'cruzeiro', 'botafogo',
        'vasco', 'fluminense', 'bahia', 'sport', 'fortaleza', 'ceará',
        'athletico', 'coritiba', 'goiás', 'atlético-mg', 'atlético-pr'
    ]

    team_lower = team_name.lower()

    return any(brazilian in team_lower for brazilian in brazilian_teams)


def get_greeting() -> str:
    """
    Get time-appropriate greeting in Portuguese

    Returns:
        Greeting string
    """
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Bom dia"
    elif 12 <= hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"


def validate_percentage(value: float) -> bool:
    """
    Validate if value is a valid percentage (0-100)

    Args:
        value: Value to validate

    Returns:
        True if valid percentage
    """
    return 0 <= value <= 100


def calculate_stake(bankroll: float, percentage: float) -> float:
    """
    Calculate stake based on bankroll and percentage

    Args:
        bankroll: Total bankroll
        percentage: Percentage of bankroll to stake

    Returns:
        Stake amount
    """
    if bankroll <= 0 or not validate_percentage(percentage):
        return 0.0

    return bankroll * (percentage / 100)


def format_currency(amount: float, currency: str = "R$") -> str:
    """
    Format amount as currency

    Args:
        amount: Amount to format
        currency: Currency symbol

    Returns:
        Formatted currency string
    """
    return f"{currency} {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
