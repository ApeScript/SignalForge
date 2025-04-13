import logging
import os
from datetime import datetime


def setup_logger(log_level: str = "INFO") -> None:
    """
    Initialize and configure the SignalForge logger.

    Creates both console and file logging outputs.
    Automatically creates the /logs directory if missing.

    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
    """

    # Define log directory and file name
    log_dir = "logs"
    log_file = os.path.join(log_dir, "signalforge.log")

    # Auto-create /logs folder if not exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Get SignalForge logger instance
    logger = logging.getLogger("signalforge")

    # Set log level dynamically (fallback to INFO if invalid)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Define common log format
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Setup file handler for persistent log storage
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Setup console handler for terminal output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Prevent adding multiple handlers if logger already configured
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.info("Logger initialized. Log level: %s", log_level)

