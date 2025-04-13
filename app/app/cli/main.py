# Import required standard libraries
import argparse  # For parsing CLI arguments
import sys       # For system exit
import logging   # For logging messages

# Import custom modules from SignalForge
from app.outputs.logger import setup_logger
from app.core.config_loader import ConfigLoader
from app.db.database import Database
from app.cli import commands


def main():
    """
    Main entry point for SignalForge CLI.
    This function handles:
    - Argument parsing
    - Logger initialization
    - Config loading
    - Database initialization
    - Command dispatching
    """

    # Create argument parser for CLI usage
    parser = argparse.ArgumentParser(
        description="SignalForge - AI Driven Crypto Signal Framework"
    )

    # Required argument → which command to run
    parser.add_argument(
        "command",
        help="Command to execute (scan, train, signal, help)"
    )

    # Optional argument → Wallet address to analyze
    parser.add_argument(
        "--wallet",
        help="Wallet address to analyze"
    )

    # Optional argument → Strategy config to use
    parser.add_argument(
        "--strategy",
        help="Strategy config file (default: strategy_aggressive.yaml)",
        default="config/strategy_aggressive.yaml"
    )

    # Parse provided arguments
    args = parser.parse_args()

    # Initialize logging system for CLI
    setup_logger("INFO")

    logger = logging.getLogger("signalforge")
    logger.info("Starting SignalForge CLI...")

    # Load configuration (base + strategy merged)
    config_loader = ConfigLoader(
        base_config_path="config/base_config.yaml",
        strategy_config_path=args.strategy
    )

    config = config_loader.load_configs()

    # Exit if config loading failed
    if not config:
        logger.error("Failed to load configuration. Exiting.")
        sys.exit(1)

    # Initialize database (SQLite)
    db = Database()

    # Dispatch and execute the correct CLI command
    commands.dispatch(args.command, args, config, db)


# Required Python entry point for CLI execution
if __name__ == "__main__":
    main()
