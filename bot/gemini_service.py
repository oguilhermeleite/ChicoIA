"""
Google Gemini API integration for conversational AI
"""

import os
import logging
from typing import List, Dict, Optional
import google.generativeai as genai
from bot.prompts import CHICO_SYSTEM_PROMPT, MATCH_ANALYSIS_PROMPT, DAILY_TIPS_PROMPT

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API"""

    def __init__(self, api_key: str):
        """
        Initialize Gemini service

        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)

        # Configure model
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )

        logger.info("Gemini service initialized successfully")

    async def get_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Get conversational response from Gemini

        Args:
            user_message: User's message
            conversation_history: Previous conversation context

        Returns:
            AI-generated response
        """
        try:
            # Build conversation context
            messages = [{"role": "user", "parts": [CHICO_SYSTEM_PROMPT]}]

            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    messages.append({
                        "role": msg["role"],
                        "parts": [msg["content"]]
                    })

            # Add current user message
            messages.append({
                "role": "user",
                "parts": [user_message]
            })

            # Start chat and get response
            chat = self.model.start_chat(history=[])

            # Send full context
            full_prompt = f"{CHICO_SYSTEM_PROMPT}\n\n"
            if conversation_history:
                for msg in conversation_history[-10:]:
                    role = "Usuário" if msg["role"] == "user" else "Chico"
                    full_prompt += f"{role}: {msg['content']}\n"
            full_prompt += f"Usuário: {user_message}\nChico:"

            response = chat.send_message(full_prompt)

            logger.info(f"Generated response for message: {user_message[:50]}...")
            return response.text

        except Exception as e:
            logger.error(f"Error getting Gemini response: {e}")
            return self._get_fallback_response(user_message)

    async def analyze_match(self, match_info: str) -> str:
        """
        Analyze a specific match

        Args:
            match_info: Match information (e.g., "Flamengo vs Palmeiras")

        Returns:
            Match analysis
        """
        try:
            prompt = MATCH_ANALYSIS_PROMPT.format(match=match_info)
            full_prompt = f"{CHICO_SYSTEM_PROMPT}\n\n{prompt}"

            response = self.model.generate_content(full_prompt)
            logger.info(f"Generated match analysis for: {match_info}")
            return response.text

        except Exception as e:
            logger.error(f"Error analyzing match: {e}")
            return "Desculpa, tive um problema ao analisar esse jogo. Pode tentar de novo? 🤔"

    async def get_daily_tips(self) -> str:
        """
        Get daily betting tips

        Returns:
            Daily tips and suggestions
        """
        try:
            full_prompt = f"{CHICO_SYSTEM_PROMPT}\n\n{DAILY_TIPS_PROMPT}"

            response = self.model.generate_content(full_prompt)
            logger.info("Generated daily tips")
            return response.text

        except Exception as e:
            logger.error(f"Error getting daily tips: {e}")
            return "Ops, tive um problema ao buscar os palpites de hoje. Tenta de novo em alguns segundos? 😅"

    def _get_fallback_response(self, user_message: str) -> str:
        """
        Fallback response when API fails

        Args:
            user_message: User's message

        Returns:
            Simple fallback response
        """
        fallback_responses = {
            "oi": "Opa! Tô com um probleminha técnico aqui, mas já já volto. Enquanto isso, usa /ajuda pra ver os comandos disponíveis! 😊",
            "olá": "Fala! Tô tendo uma dificuldade técnica momentânea. Tenta de novo em alguns segundos? 🙏",
            "ajuda": "Use os comandos:\n/start - Começar\n/palpites - Sugestões do dia\n/analisar - Analisar jogo\n/ajuda - Ver comandos",
            "default": "Opa, tô com uma instabilidade aqui. Pode tentar de novo? Se persistir, usa /ajuda pra ver outras opções! 😊"
        }

        user_message_lower = user_message.lower().strip()

        for key in fallback_responses:
            if key in user_message_lower:
                return fallback_responses[key]

        return fallback_responses["default"]
