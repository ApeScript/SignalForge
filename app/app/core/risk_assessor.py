import logging
from typing import Dict, Any, List

logger = logging.getLogger("signalforge")


class RiskAssessor:
    """
    RiskAssessor calculates a risk score
    based on wallet analysis and detected patterns.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize RiskAssessor.

        Args:
            config (dict): Configuration rules.
        """
        self.config = config

    def calculate_risk_score(self, wallet_analysis: Dict[str, Any], patterns: List[Dict[str, Any]]) -> float:
        """
        Calculate a risk score from analysis data.

        Args:
            wallet_analysis (dict): Wallet analysis result.
            patterns (list): Detected patterns.

        Returns:
            float: Risk score between 0.0 and 10.0
        """
        logger.info(f"Calculating risk score for wallet {wallet_analysis.get('wallet')}")

        score = 0.0

        # Base score for activity type
        activity_type = wallet_analysis.get("activity_type", "")

        activity_weights = self.config.get("risk_weights", {}).get("activity", {})
        score += activity_weights.get(activity_type, 1.0)

        # Add weight per detected pattern
        pattern_weight = self.config.get("risk_weights", {}).get("pattern", 1.5)
        score += len(patterns) * pattern_weight

        # Bonus for whale behavior
        if wallet_analysis.get("tokens_held", 0) >= self.config.get("risk_weights", {}).get("whale_token_threshold", 20):
            score += 2.5

        # Ensure score stays in 0-10 range
        final_score = min(round(score, 2), 10.0)

        logger.info(f"Final risk score: {final_score}")
        return final_score
