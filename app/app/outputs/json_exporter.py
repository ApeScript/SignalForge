import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger("signalforge")


class JSONExporter:
    """
    JSONExporter saves generated signals
    to local JSON files for history and further processing.
    """

    def __init__(self, base_dir: str = "signals"):
        """
        Initialize JSONExporter.

        Args:
            base_dir (str): Base directory for signal storage.
        """
        self.base_dir = base_dir

    def _generate_wallet_hash(self, wallet_address: str) -> str:
        """
        Generate a hash for wallet filename.

        Args:
            wallet_address (str): Wallet address.

        Returns:
            str: Hashed string.
        """
        return hashlib.sha256(wallet_address.encode()).hexdigest()[:12]

    def save_signal(self, signal: Dict[str, Any]) -> None:
        """
        Save the given signal to a JSON file.

        Args:
            signal (dict): The signal data to save.
        """
        today = datetime.utcnow().strftime("%Y-%m-%d")
        wallet_hash = self._generate_wallet_hash(signal.get("wallet", "unknown"))

        dir_path = os.path.join(self.base_dir, today)
        os.makedirs(dir_path, exist_ok=True)

        file_path = os.path.join(dir_path, f"{wallet_hash}.json")

        try:
            with open(file_path, "w") as f:
                json.dump(signal, f, indent=4)

            logger.info(f"Signal saved to {file_path}")

        except Exception as e:
            logger.error(f"Failed to save signal to {file_path}: {e}")
