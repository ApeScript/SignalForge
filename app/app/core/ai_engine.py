import os
import logging
from typing import Dict, Any, List

import openai

logger = logging.getLogger("signalforge")


class AIEngine:
    """
    AIEngine integrates OpenAI GPT for generating
    human-readable comments on detected trading patterns.
    """

    def __init__(self, api_key: str):
        """
        Initialize AIEngine.

        Args:
            api_key (str): OpenAI API key.
        """
        self.api_key = api_key
        openai.api_key = api_key

    def generate_comment(self, wallet_analysis: Dict[str, Any], patterns: List[Dict[str, Any]]) -> str:
        """
        Generate an AI-powered comment based on wallet data and patterns.

        Args:
            wallet_analysis (dict): Wallet analysis result.
            patterns (list): List of detected patterns.

        Returns:
            str: AI-generated comment.
        """
        try:
            prompt = self._build_prompt(wallet_analysis, patterns)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert crypto trading analyst. Keep responses short and realistic."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6
            )

            comment = response.choices[0].message.content.strip()
            logger.info("AI comment generated successfully.")
            return comment

        except Exception as e:
            logger.error(f"Failed to generate AI comment: {e}")
            return "AI comment unavailable."

    def _build_prompt(self, wallet_analysis: Dict[str, Any], patterns: List[Dict[str, Any]]) -> str:
        """
        Build prompt for AI generation.

        Args:
            wallet_analysis (dict): Wallet analysis data.
            patterns (list): Detected patterns.

        Returns:
            str: Prompt text.
        """
        pattern_names = [p["name"] for p in patterns]
        prompt = (
            f"Analyze the following wallet behavior:\n"
            f"Wallet Address: {wallet_analysis.get('wallet')}\n"
            f"Tokens Held: {wallet_analysis.get('tokens_held')}\n"
            f"Transaction Count: {wallet_analysis.get('transaction_count')}\n"
            f"Detected Patterns: {', '.join(pattern_names)}\n"
            f"Provide a short comment about the trading behavior."
        )
        return prompt
