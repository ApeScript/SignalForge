import os
import yaml
import logging

logger = logging.getLogger("signalforge")


class ConfigLoader:
    """
    ConfigLoader loads and validates YAML-based configurations
    for SignalForge.
    """

    def __init__(self, base_config_path: str, strategy_config_path: str):
        """
        Initialize ConfigLoader.

        Args:
            base_config_path (str): Path to base config YAML file.
            strategy_config_path (str): Path to strategy-specific config YAML.
        """
        self.base_config_path = base_config_path
        self.strategy_config_path = strategy_config_path
        self.config = {}

    def load_configs(self) -> dict:
        """
        Load and merge base config with strategy config.

        Returns:
            dict: Merged config dictionary.
        """
        base_config = self._load_yaml(self.base_config_path)
        strategy_config = self._load_yaml(self.strategy_config_path)

        if not base_config:
            logger.error(f"Base config not found at {self.base_config_path}")
            return {}

        # Merge configs (strategy overrides base)
        merged_config = base_config.copy()
        merged_config.update(strategy_config or {})

        self.config = merged_config
        logger.info("Configuration successfully loaded and merged.")
        return self.config

    def _load_yaml(self, path: str) -> dict:
        """
        Load a YAML file.

        Args:
            path (str): Path to YAML file.

        Returns:
            dict: Loaded data or empty dict.
        """
        if not os.path.exists(path):
            logger.warning(f"Config file not found: {path}")
            return {}

        try:
            with open(path, "r") as file:
                return yaml.safe_load(file) or {}
        except Exception as e:
            logger.error(f"Failed to load YAML from {path}: {e}")
            return {}
