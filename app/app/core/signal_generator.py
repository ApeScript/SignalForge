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
            ai_engine (AIEngine, optional): AI Engine instance for comments.
        """
        self.ai_engine = ai_engine

    def generate_signal(self, wallet_analysis: Dict[str, Any], patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a trading signal from analysis data.

        Args:
            wallet_analysis (dict): Wallet analysis result.
            patterns (list): Detected patterns list.

        Returns:
            dict: Trading signal object.
        """
        logger.info(f"Generating trading signal for wallet {wallet_analysis.get('wallet')}")

        if not patterns:
            signal_type = "HOLD"
            confidence = 0.3
            reason = "No significant patterns detected."
        else:
            signal_type = "BUY"
            confidence = min(0.5 + (len(patterns) * 0.1), 0.95)
            reason = f"{len(patterns)} pattern(s) detected: {', '.join([p['name'] for p in patterns])}"

        ai_comment = None
        if self.ai_engine:
            ai_comment = self.ai_engine.generate_comment(wallet_analysis, patterns)
            logger.info("AI comment generated.")

        signal = {
            "wallet": wallet_analysis.get("wallet"),
            "signal": signal_type,
            "confidence": round(confidence, 2),
            "reason": reason,
            "ai_comment": ai_comment or "No AI comment available."
        }

        logger.info(f"Signal generated: {signal}")
        return signal
