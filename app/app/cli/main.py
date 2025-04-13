import argparse
import sys
import logging

from app.outputs.logger import setup_logger
from app.core.config_loader import ConfigLoader
from app.db.database import Database
from app.cli import commands


def main():
    """
    Main entry point for SignalForge CLI.
    """
    parser = argparse.ArgumentParser(
        description="SignalForge - AI Driven Crypto Signal Framework"
    )

    parser.add_argument(
        "command",
        help="Command to execute (scan, train, signal, help)"
    )

    parser.add_argument(
        "--wallet",
        help="Wallet address to analyze"
    )

    parser.add_argument(
        "--strategy",
        help="Strategy config file (default: strategy_aggressive.yaml)",
        default="config/strategy_aggressive.yaml"
    )

    args = parser.parse_args()

    # Initialize Logger
    setup_logger("INFO")

    logger = logging.getLogger("signalforge")
    logger.info("Starting SignalForge CLI...")

    # Load Config
    config_loader = ConfigLoader(
        base_config_path="config/base_config.yaml",
        strategy_config_path=args.strategy
    )

    config = config_loader.load_configs()

    if not config:
        logger.error("Failed to load configuration. Exiting.")
        sys.exit(1)

    # Init DB
    db = Database()

    # Dispatch Command
    commands.dispatch(args.command, args, config, db)


if __name__ == "__main__":
    main()
