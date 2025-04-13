import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Any, Dict, Optional, Union

logger = logging.getLogger("signalforge")


def get_wallet_hash(wallet_address: str) -> str:
    """
    Generate a short hash for a wallet address for anonymized identification.

    Args:
        wallet_address (str): Blockchain wallet address.

    Returns:
        str: Shortened SHA-256 hash (first 12 characters).
    """
    return hashlib.sha256(wallet_address.encode()).hexdigest()[:12]


def get_utc_timestamp() -> str:
    """
    Get current UTC timestamp in formatted string.

    Returns:
        str: Timestamp in format YYYY-MM-DD HH:MM:SS
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def safe_load_json(path: str) -> Optional[Union[Dict[str, Any], list]]:
    """
    Safely load JSON data from a given file path.

    Args:
        path (str): Absolute or relative file path.

    Returns:
        dict or list or None: Loaded JSON data if available, else None.
    """
    if not os.path.exists(path):
        logger.warning(f"File not found: {path}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Successfully loaded JSON from {path}")
            return data
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in file: {path}")
        return None
    except Exception as e:
        logger.error(f"Failed to load JSON from {path}: {e}")
        return None


def safe_save_json(path: str, data: Union[Dict[str, Any], list]) -> None:
    """
    Safely save dictionary or list data to a JSON file.

    Args:
        path (str): Absolute or relative file path.
        data (dict or list): Data to save as JSON.

    Notes:
        Auto-creates parent folders if missing.
    """
    try:
        # Auto-create directories if missing
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        logger.info(f"Data successfully saved to {path}")

    except Exception as e:
        logger.error(f"Failed to save JSON to {path}: {e}")
