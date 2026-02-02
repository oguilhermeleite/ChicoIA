"""
Basic tests for ChicoIA Telegram bot
"""

import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
from bot.gemini_service import GeminiService
from bot.database import DatabaseManager
from utils.helpers import (
    parse_match_teams,
    sanitize_message,
    format_odds,
    calculate_implied_probability,
    is_valid_telegram_id,
    format_currency
)


class TestHelpers:
    """Test helper functions"""

    def test_parse_match_teams(self):
        """Test match parsing"""
        team1, team2 = parse_match_teams("Flamengo vs Palmeiras")
        assert team1 == "Flamengo"
        assert team2 == "Palmeiras"

        team1, team2 = parse_match_teams("Corinthians x Santos")
        assert team1 == "Corinthians"
        assert team2 == "Santos"

    def test_sanitize_message(self):
        """Test message sanitization"""
        message = "  Teste   com   espaços  "
        assert sanitize_message(message) == "Teste com espaços"

        long_message = "a" * 2000
        sanitized = sanitize_message(long_message)
        assert len(sanitized) <= 1003  # 1000 + "..."

    def test_format_odds(self):
        """Test odds formatting"""
        assert format_odds(2.5) == "2.50"
        assert format_odds(1.75) == "1.75"

    def test_calculate_implied_probability(self):
        """Test implied probability calculation"""
        prob = calculate_implied_probability(2.0)
        assert prob == 50.0

        prob = calculate_implied_probability(4.0)
        assert prob == 25.0

    def test_is_valid_telegram_id(self):
        """Test Telegram ID validation"""
        assert is_valid_telegram_id(123456789) is True
        assert is_valid_telegram_id(-123) is False
        assert is_valid_telegram_id(0) is False

    def test_format_currency(self):
        """Test currency formatting"""
        assert format_currency(100.50) == "R$ 100,50"
        assert format_currency(1000.00) == "R$ 1.000,00"


class TestGeminiService:
    """Test Gemini service"""

    @pytest.fixture
    def gemini_service(self):
        """Create Gemini service instance"""
        # Use a dummy API key for testing
        return GeminiService("test_api_key")

    def test_initialization(self, gemini_service):
        """Test service initialization"""
        assert gemini_service.api_key == "test_api_key"
        assert gemini_service.model is not None

    def test_fallback_response(self, gemini_service):
        """Test fallback responses"""
        response = gemini_service._get_fallback_response("oi")
        assert "probleminha" in response.lower() or "técnico" in response.lower()


class TestDatabase:
    """Test database operations"""

    @pytest.fixture
    def mock_db(self):
        """Create mock database"""
        # For actual testing, you'd use a test database
        # This is just a structure example
        pass

    def test_user_creation(self):
        """Test user creation"""
        # Mock test - implement with actual test database
        pass

    def test_conversation_save(self):
        """Test conversation saving"""
        # Mock test - implement with actual test database
        pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
