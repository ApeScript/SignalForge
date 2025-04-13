import logging
from typing import Dict, Any, List

from app.core.data_collector import DataCollector

logger = logging.getLogger("signalforge")


class WalletScanner:
    """
    WalletScanner analyzes a wallet's behavior
    based on its holdings and recent transaction activity.
    """

    def __init__(self, data_collector: DataCollector):
        """
        Initialize the WalletScanner.

        Args:
            data_collector (DataCollector): Instance of DataCollector.
        """
        self.data_collector = data_collector

    def analyze_wallet(self, wallet_address: str) -> Dict[str, Any]:
        """
        Analyze a wallet and return behavioral insights.

        Args:
            wallet_address (str): Blockchain wallet address.

        Returns:
            dict: Wallet analysis result.
        """
        logger.info(f"Analyzing wallet {wallet_address}...")

        balance_data = self.data_collector.fetch_wallet_balance(wallet_address)
        transactions = self.data_collector.fetch_recent_transactions(wallet_address, limit=20)

        token_count = len(balance_data.get('value', []))
        transaction_count = len(transactions)

        if transaction_count == 0:
            activity_type = "Dormant Wallet"
        elif transaction_count <= 5:
            activity_type = "Low Activity"
        elif transaction_count <= 20:
            activity_type = "Moderate Activity"
        else:
            activity_type = "High Activity"

        behavior_type = "Holder" if transaction_count < 5 and token_count >= 2 else "Active Trader"

        analysis = {
            "wallet": wallet_address,
            "tokens_held": token_count,
            "transaction_count": transaction_count,
            "activity_type": activity_type,
            "behavior_type": behavior_type
        }

        logger.info(f"Wallet Analysis Complete: {analysis}")
        return analysis
