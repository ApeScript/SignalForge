import logging
import random
from typing import Dict, Any, List, Optional

from app.core.ai_engine import AIEngine

logger = logging.getLogger("signalforge")


class SignalGenerator:
    """
    SignalGenerator creates a trading signal object
    based on wallet analysis and detected patterns.
    """

    def __init__(self, ai_engine: Optional[AIEngine] = None):
        """
        Initialize SignalGenerator.

        Args:
            ai_engine (AIEngine, optional): AI Engine instance for comment generation.
        """
        self.ai_engine = ai_engine

    def generate_signal(self, wallet_analysis: Dict[str, Any], patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a trading signal based on provided wallet analysis and detected patterns.

        Args:
            wallet_analysis (dict): Analysis result for a wallet.
            patterns (list): List of detected patterns.

        Returns:
            dict: Final trading signal object with all data.
        """

        logger.info(f"Generating trading signal for wallet {wallet_analysis.get('wallet')}")

        # Default values
        signal_type = "HOLD"
        confidence = 0.3
        reason = "No significant patterns detected."

        # Basic rule: If patterns detected → BUY signal
        if patterns:
            signal_type = "BUY"
            confidence = min(0.5 + (len(patterns) * 0.1), 0.95)
            reason = f"{len(patterns)} pattern(s) detected: {', '.join([p['name'] for p in patterns])}"

        # Additional rule: If empty wallet → suggest AVOID instead of HOLD
        if wallet_analysis.get("tokens_held", 0) == 0 and wallet_analysis.get("transaction_count", 0) == 0:
            signal_type = "AVOID"
            confidence = 0.1
            reason = "Empty wallet detected. No holdings or activity."

        # Optional AI generated comment
        ai_comment = None
        if self.ai_engine:
            ai_comment = self.ai_engine.generate_comment(wallet_analysis, patterns)
            logger.info("AI comment generated.")

        # Build final signal dictionary
        signal = {
            "wallet": wallet_analysis.get("wallet"),
            "signal": signal_type,  # BUY / HOLD / AVOID
            "confidence": round(confidence, 2),  # Confidence between 0.1 - 0.95
            "reason": reason,  # Explanation why signal was generated
            "ai_comment": ai_comment or "No AI comment available."  # AI explanation or fallback text
        }

        logger.info(f"Signal generated successfully: {signal}")

        return signal
