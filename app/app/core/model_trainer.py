import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("signalforge")


class ModelTrainer:
    """
    ModelTrainer allows users to define and train
    custom pattern rules for SignalForge.
    """

    def __init__(self, storage_path: str = "assets/pattern_memory.json"):
        """
        Initialize ModelTrainer.

        Args:
            storage_path (str): Path to pattern storage file.
        """
        self.storage_path = storage_path
        self.memory = self._load_memory()

    def _load_memory(self) -> List[Dict[str, Any]]:
        """
        Load pattern memory from JSON file.

        Returns:
            list: Stored patterns.
        """
        if not os.path.exists(self.storage_path):
            logger.warning(f"Pattern memory not found at {self.storage_path}. Starting empty.")
            return []

        try:
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                logger.info("Pattern memory loaded successfully.")
                return data
        except Exception as e:
            logger.error(f"Failed to load pattern memory: {e}")
            return []

    def add_pattern(self, pattern_name: str, description: str, conditions: Dict[str, Any]) -> None:
        """
        Add a new pattern to memory.

        Args:
            pattern_name (str): Name of the pattern.
            description (str): Description of the pattern.
            conditions (dict): Conditions for detection.
        """
        new_pattern = {
            "name": pattern_name,
            "description": description,
            "conditions": conditions
        }
        self.memory.append(new_pattern)
        self._save_memory()
        logger.info(f"Added new pattern: {pattern_name}")

    def _save_memory(self) -> None:
        """
        Save pattern memory to JSON file.
        """
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.memory, f, indent=4)
            logger.info("Pattern memory saved.")
        except Exception as e:
            logger.error(f"Failed to save pattern memory: {e}")

    def get_patterns(self) -> List[Dict[str, Any]]:
        """
        Get all stored patterns.

        Returns:
            list: Stored patterns.
        """
        return self.memory
