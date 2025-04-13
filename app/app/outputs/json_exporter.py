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
    Automatically organizes signals in daily folders.
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
        Generate a unique but short hash from wallet address
        for cleaner filenames and privacy-friendly storage.

        Args:
            wallet_address (str): Wallet address.

        Returns:
            str: First 12 chars of SHA256 hash.
        """
        return hashlib.sha256(wallet_address.encode()).hexdigest()[:12]

    def _get_output_path(self, wallet_address: str) -> str:
        """
        Build the full output path for the signal file.

        Args:
            wallet_address (str): Wallet address.

        Returns:
            str: Full file path to save signal.
        """
        # Folder name = UTC date
        today = datetime.utcnow().strftime("%Y-%m-%d")

        # Subfolder per day
        dir_path = os.path.join(self.base_dir, today)

        # Auto-create if missing
        os.makedirs(dir_path, exist_ok=True)

        # Final filename = wallet hash
        wallet_hash = self._generate_wallet_hash(wallet_address)
        filename = f"{wallet_hash}.json"

        return os.path.join(dir_path, filename)

    def save_signal(self, signal: Dict[str, Any]) -> None:
        """
        Save the given signal to a local JSON file.

        Args:
            signal (dict): The signal data to save.
        """
        # Determine wallet address (fallback if missing)
        wallet_address = signal.get("wallet", "unknown")

        # Generate clean file path
        file_path = self._get_output_path(wallet_address)

        try:
            # Write to file
            with open(file_path, "w") as f:
                json.dump(signal, f, indent=4)

            logger.info(f"Signal saved successfully: {file_path}")

        except Exception as e:
            logger.error(f"Failed to save signal to {file_path}: {e}")
