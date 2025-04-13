import os
import json
import logging
from typing import Dict, Any, List

# Initialize logger
logger = logging.getLogger("signalforge")


class ModelTrainer:
    """
    ModelTrainer allows users to create, store, retrieve 
    and manage custom pattern rules for SignalForge.
    Patterns are stored locally in a JSON file.
    """

    def __init__(self, storage_path: str = "assets/pattern_memory.json"):
        """
        Initialize ModelTrainer.

        Args:
            storage_path (str): Path to pattern storage JSON file.
        """
        self.storage_path = storage_path

        # Auto-create assets folder if missing
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)

        # Load existing memory or start empty
        self.memory = self._load_memory()

    def _load_memory(self) -> List[Dict[str, Any]]:
        """
        Load pattern memory from local JSON file.

        Returns:
            list: List of stored pattern dicts.
        """
        if not os.path.isfile(self.storage_path):
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

    def _save_memory(self) -> None:
        """
        Save current memory to local JSON file.
        """
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.memory, f, indent=4)
            logger.info("Pattern memory saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save pattern memory: {e}")

    def add_pattern(self, pattern_name: str, description: str, conditions: Dict[str, Any]) -> None:
        """
        Add a new pattern to memory.

        Args:
            pattern_name (str): Name of the new pattern.
            description (str): Explanation of the pattern.
            conditions (dict): Detection conditions of the pattern.
        """
        # Prevent duplicate pattern names
        if any(p["name"].lower() == pattern_name.lower() for p in self.memory):
            logger.warning(f"Pattern with name '{pattern_name}' already exists. Skipping add.")
            return

        new_pattern = {
            "name": pattern_name,
            "description": description,
            "conditions": conditions
        }

        self.memory.append(new_pattern)
        self._save_memory()
        logger.info(f"Added new pattern: {pattern_name}")

    def get_patterns(self) -> List[Dict[str, Any]]:
        """
        Retrieve all stored patterns.

        Returns:
            list: List of all patterns in memory.
        """
        return self.memory

    def delete_pattern(self, pattern_name: str) -> None:
        """
        Delete a specific pattern by name.

        Args:
            pattern_name (str): Name of the pattern to delete.
        """
        original_len = len(self.memory)
        self.memory = [p for p in self.memory if p["name"].lower() != pattern_name.lower()]

        if len(self.memory) < original_len:
            self._save_memory()
            logger.info(f"Deleted pattern: {pattern_name}")
        else:
            logger.warning(f"No pattern found with name: {pattern_name}")

    def clear_memory(self) -> None:
        """
        Delete all patterns from memory.
        """
        self.memory = []
        self._save_memory()
        logger.info("All patterns deleted. Pattern memory cleared.")
