import logging
from typing import Dict, List, Any

# Initialize logger
logger = logging.getLogger("signalforge")


class PatternDetector:
    """
    PatternDetector analyzes wallet data and detects 
    specific trading patterns based on dynamic config rules.
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
        Detect patterns from wallet analysis result.

        Args:
            wallet_analysis (dict): Result data from WalletScanner.

        Returns:
            list: List of detected pattern dictionaries.
        """
        patterns = []

        # Extract relevant wallet metrics
        tokens_held = wallet_analysis.get("tokens_held", 0)
        transaction_count = wallet_analysis.get("transaction_count", 0)
        activity_type = wallet_analysis.get("activity_type", "")
        wallet_address = wallet_analysis.get("wallet", "unknown")

        # Load pattern rules from config with safe defaults
        pattern_rules = self.config.get("pattern_rules", {})
        whale_tokens_threshold = pattern_rules.get("whale_tokens", 20)
        dormant_threshold = pattern_rules.get("dormant_threshold", 5)

        # Pattern 1: Empty Wallet
        if tokens_held == 0 and transaction_count == 0:
            patterns.append({
                "name": "Empty Wallet",
                "description": "Wallet holds no tokens and has no transactions."
            })

        # Pattern 2: Whale Wallet
        if tokens_held >= whale_tokens_threshold:
            patterns.append({
                "name": "Whale Wallet",
                "description": f"Wallet holds at least {whale_tokens_threshold} tokens."
            })

        # Pattern 3: Dormant Awakening
        if activity_type == "High Activity" and transaction_count < dormant_threshold:
            patterns.append({
                "name": "Dormant Awakening",
                "description": "Previously inactive wallet is now highly active."
            })

        # Pattern 4: Accumulation Behavior
        if tokens_held >= 3 and transaction_count <= 5:
            patterns.append({
                "name": "Accumulation Behavior",
                "description": "Wallet is accumulating tokens quietly."
            })

        logger.info(f"Detected {len(patterns)} pattern(s) for wallet {wallet_address}")

        return patterns
