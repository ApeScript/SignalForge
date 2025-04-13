import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger("signalforge")


def get_wallet_hash(wallet_address: str) -> str:
    """
    Generate a short hash for a wallet address.

    Args:
        wallet_address (str): Wallet address.

    Returns:
        str: Short hash.
    """
    return hashlib.sha256(wallet_address.encode()).hexdigest()[:12]


def get_utc_timestamp() -> str:
    """
    Get current UTC timestamp.

    Returns:
        str: Timestamp string.
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def safe_load_json(path: str) -> Optional[Dict[str, Any]]:
    """
    Safely load JSON file.

    Args:
        path (str): File path.

    Returns:
        dict or None: Loaded data.
    """
    if not os.path.exists(path):
        logger.warning(f"File not found: {path}")
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON from {path}: {e}")
        return None


def safe_save_json(path: str, data: Dict[str, Any]) -> None:
    """
    Safely save data to JSON file.

    Args:
        path (str): File path.
        data (dict): Data to save.
    """
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Data saved to {path}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {path}: {e}")
