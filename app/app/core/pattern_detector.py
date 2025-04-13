import logging
from typing import Dict, List, Any

logger = logging.getLogger("signalforge")


class PatternDetector:
    """
    PatternDetector analyzes data and detects
    trading patterns based on configurable rules.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize PatternDetector.

        Args:
            config (dict): Loaded configuration rules.
        """
        self.config = config

    def detect_patterns(self, wallet_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect patterns from wallet analysis data.

        Args:
            wallet_analysis (dict): Result from WalletScanner.

        Returns:
            list: List of detected pattern dicts.
        """
        patterns = []

        tokens_held = wallet_analysis.get("tokens_held", 0)
        transaction_count = wallet_analysis.get("transaction_count", 0)

        # Rule: Whale Wallet
        if tokens_held >= self.config.get("pattern_rules", {}).get("whale_tokens", 20):
            patterns.append({
                "name": "Whale Wallet",
                "description": "Wallet holds a large number of tokens."
            })

        # Rule: Dormant Wallet suddenly active
        if wallet_analysis.get("activity_type") == "High Activity" and transaction_count < self.config.get("pattern_rules", {}).get("dormant_threshold", 5):
            patterns.append({
                "name": "Dormant Awakening",
                "description": "Previously inactive wallet is now highly active."
            })

        # Rule: Accumulation Pattern
        if tokens_held >= 3 and transaction_count <= 5:
            patterns.append({
                "name": "Accumulation Behavior",
                "description": "Wallet is accumulating tokens quietly."
            })

        logger.info(f"Detected {len(patterns)} patterns for wallet {wallet_analysis.get('wallet')}")
        return patterns
