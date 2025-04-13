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
        Initialize RiskAssessor with loaded configuration.

        Args:
            config (dict): Configuration dictionary with risk rules.
        """
        self.config = config

    def calculate_risk_score(self, wallet_analysis: Dict[str, Any], patterns: List[Dict[str, Any]]) -> float:
        """
        Calculate a risk score from analysis data.

        Args:
            wallet_analysis (dict): Wallet analysis result from WalletScanner.
            patterns (list): List of detected pattern dictionaries.

        Returns:
            float: Final risk score between 0.0 and 10.0
        """

        logger.info(f"Calculating risk score for wallet {wallet_analysis.get('wallet')}")

        score = 0.0  # Initial base score

        # Fetch weights from config safely
        activity_weights = self.config.get("risk_weights", {}).get("activity", {})
        pattern_weight = self.config.get("risk_weights", {}).get("pattern", 1.5)
        whale_threshold = self.config.get("risk_weights", {}).get("whale_token_threshold", 20)

        # Determine wallet activity type
        activity_type = wallet_analysis.get("activity_type", "")

        # Add activity type score (if defined in config)
        activity_score = activity_weights.get(activity_type, 1.0)
        score += activity_score

        logger.debug(f"Activity type: {activity_type} → +{activity_score}")

        # Add score for number of detected patterns
        pattern_score = len(patterns) * pattern_weight
        score += pattern_score

        logger.debug(f"Patterns detected: {len(patterns)} → +{pattern_score}")

        # Bonus score for whale wallets (high token holding)
        tokens_held = wallet_analysis.get("tokens_held", 0)
        if tokens_held >= whale_threshold:
            score += 2.5
            logger.debug(f"Whale threshold exceeded: {tokens_held} tokens → +2.5")

        # Extra rule → penalty if wallet is completely empty
        if tokens_held == 0 and wallet_analysis.get("transaction_count", 0) == 0:
            score = max(score - 1.0, 0.0)
            logger.debug(f"Empty wallet detected → -1.0 penalty")

        # Round final score and limit max to 10
        final_score = min(round(score, 2), 10.0)

        logger.info(f"Final risk score for wallet {wallet_analysis.get('wallet')}: {final_score}")
        return final_score
