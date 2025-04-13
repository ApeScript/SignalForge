import os
import yaml
import logging

# Initialize logger
logger = logging.getLogger("signalforge")


class ConfigLoader:
    """
    ConfigLoader handles loading, merging, and validating 
    YAML configuration files for SignalForge.
    """

    def __init__(self, base_config_path: str, strategy_config_path: str):
        """
        Initialize the ConfigLoader with file paths.

        Args:
            base_config_path (str): Path to base config YAML file.
            strategy_config_path (str): Path to strategy-specific config YAML.
        """
        self.base_config_path = base_config_path
        self.strategy_config_path = strategy_config_path
        self.config = {}

    def load_configs(self) -> dict:
        """
        Load both base and strategy configuration files.
        Merge them together, with strategy config overriding base config.

        Returns:
            dict: Final merged configuration dictionary.
        """
        # Load YAML files
        base_config = self._load_yaml(self.base_config_path)
        strategy_config = self._load_yaml(self.strategy_config_path)

        # Error handling if both configs missing
        if not base_config and not strategy_config:
            logger.error("No configuration could be loaded. Exiting.")
            return {}

        if not base_config:
            logger.warning(f"Base config missing → using strategy config only.")

        # Merge strategy config over base config
        merged_config = base_config.copy()
        merged_config.update(strategy_config or {})

        self.config = merged_config

        logger.info("Configuration loaded and merged successfully.")
        return self.config

    def _load_yaml(self, path: str) -> dict:
        """
        Load YAML content from a given file path.

        Args:
            path (str): Path to the YAML file.

        Returns:
            dict: Parsed YAML data or empty dictionary.
        """
        # Convert to absolute path for safety
        path = os.path.abspath(path)

        if not os.path.exists(path):
            logger.warning(f"Config file not found: {path}")
            return {}

        try:
            with open(path, "r") as file:
                data = yaml.safe_load(file) or {}
                logger.debug(f"Loaded YAML from: {path}")
                return data
        except Exception as e:
            logger.error(f"Failed to load YAML from {path}: {e}")
            return {}

    def get(self, key: str, default=None):
        """
        Safe access to configuration values.

        Args:
            key (str): The config key to retrieve.
            default (Any): Default value if key does not exist.

        Returns:
            Any: Config value or provided default.
        """
        return self.config.get(key, default)
