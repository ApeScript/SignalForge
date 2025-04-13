import os
import logging
from typing import Dict, Any, List

import openai

# Initialize logger
logger = logging.getLogger("signalforge")


class AIEngine:
    """
    AIEngine integrates OpenAI GPT to generate short, human-readable comments
    based on wallet analysis and detected patterns.
    """

    def __init__(self, api_key: str):
        """
        Initialize AIEngine with OpenAI API Key.

        Args:
            api_key (str): OpenAI API key for authentication.
        """
        self.api_key = api_key
        openai.api_key = api_key

    def generate_comment(self, wallet_analysis: Dict[str, Any], patterns: List[Dict[str, Any]]) -> str:
        """
        Generate an AI comment based on wallet analysis and patterns.

        Args:
            wallet_analysis (dict): Result of wallet analysis.
            patterns (list): List of detected patterns.

        Returns:
            str: AI-generated comment or fallback message.
        """
        try:
            # Build prompt for GPT
            prompt = self._build_prompt(wallet_analysis, patterns)

            # Call OpenAI ChatCompletion API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert crypto trading analyst. Keep responses short, clear, and realistic."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,  # Low creativity for consistency
                max_tokens=200,   # Limit output length
                request_timeout=15  # Prevent long hangs
            )

            # Extract result
            comment = response.choices[0].message.content.strip()

            logger.info("AI comment generated successfully.")
            return comment

        except Exception as e:
            logger.error(f"Failed to generate AI comment: {e}")
            return "AI comment unavailable."

    def _build_prompt(self, wallet_analysis: Dict[str, Any], patterns: List[Dict[str, Any]]) -> str:
        """
        Build the prompt for GPT based on analysis data.

        Args:
            wallet_analysis (dict): Analyzed wallet data.
            patterns (list): Patterns detected during analysis.

        Returns:
            str: The final prompt text for GPT.
        """

        # Extract pattern names or provide fallback text
        if patterns:
            pattern_names = [p.get("name", "Unknown Pattern") for p in patterns]
            patterns_text = ', '.join(pattern_names)
        else:
            patterns_text = "No patterns detected"

        # Build prompt string
        prompt = (
            f"Analyze the following wallet behavior:\n"
            f"Wallet Address: {wallet_analysis.get('wallet', 'N/A')}\n"
            f"Tokens Held: {wallet_analysis.get('tokens_held', 0)}\n"
            f"Transaction Count: {wallet_analysis.get('transaction_count', 0)}\n"
            f"Detected Patterns: {patterns_text}\n"
            f"Provide a short and realistic comment about this trading behavior."
        )

        logger.debug(f"AI Prompt built: {prompt}")
        return prompt
