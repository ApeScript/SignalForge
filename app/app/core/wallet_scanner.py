import logging
from typing import Dict, Any

from app.core.data_collector import DataCollector

# Initialize logger for SignalForge
logger = logging.getLogger("signalforge")


class WalletScanner:
    """
    WalletScanner analyzes a wallet's behavior
    based on its holdings and recent transaction activity.
    """

    def __init__(self, data_collector: DataCollector):
        """
        Initialize the WalletScanner instance.

        Args:
            data_collector (DataCollector): Instance of DataCollector for fetching wallet data.
        """
        self.data_collector = data_collector

    def analyze_wallet(self, wallet_address: str) -> Dict[str, Any]:
        """
        Analyze a wallet address and return a behavior profile.

        Args:
            wallet_address (str): Blockchain wallet address to analyze.

        Returns:
            dict: Analysis result containing activity and behavior classification.
        """

        logger.info(f"Starting analysis for wallet: {wallet_address}")

        # Safe default values
        token_count = 0
        transaction_count = 0
        balance_data = {}
        transactions = []

        # Fetch balance
        try:
            balance_data = self.data_collector.fetch_wallet_balance(wallet_address)
            token_count = len(balance_data.get('value', []))
        except Exception as e:
            logger.warning(f"Failed to fetch wallet balance for {wallet_address}: {e}")

        # Fetch transactions
        try:
            transactions = self.data_collector.fetch_recent_transactions(wallet_address, limit=20)
            transaction_count = len(transactions)
        except Exception as e:
            logger.warning(f"Failed to fetch transactions for {wallet_address}: {e}")

        # Activity type classification
        if transaction_count == 0:
            activity_type = "Dormant Wallet"
        elif transaction_count <= 5:
            activity_type = "Low Activity"
        elif transaction_count <= 20:
            activity_type = "Moderate Activity"
        else:
            activity_type = "High Activity"

        # Behavior type classification
        behavior_type = "Holder" if transaction_count < 5 and token_count >= 2 else "Active Trader"

        # Quick Whale Detection (purely based on tokens held)
        is_whale = True if token_count >= 20 else False

        # Final Analysis Result
        analysis = {
            "wallet": wallet_address,
            "tokens_held": token_count,
            "transaction_count": transaction_count,
            "activity_type": activity_type,
            "behavior_type": behavior_type,
            "is_whale": is_whale,
            "top_tokens": balance_data.get('value', []),
            "recent_transactions": transactions
        }

        logger.info(f"Analysis completed for wallet {wallet_address}: "
                    f"Tokens Held: {token_count}, "
                    f"Tx Count: {transaction_count}, "
                    f"Activity: {activity_type}, "
                    f"Behavior: {behavior_type}, "
                    f"Whale: {is_whale}")

        return analysis
