import logging
import os
from datetime import datetime


def setup_logger(log_level: str = "INFO") -> None:
    """
    Setup the logger for SignalForge.

    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "signalforge.log")

    logger = logging.getLogger("signalforge")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Formatter for console and file output
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.info("Logger initialized. Log level: %s", log_level)
