# Import standard logging module
import logging

# Import core modules from SignalForge
from app.core.data_collector import DataCollector
from app.core.wallet_scanner import WalletScanner
from app.core.pattern_detector import PatternDetector
from app.core.signal_generator import SignalGenerator
from app.core.risk_assessor import RiskAssessor
from app.core.model_trainer import ModelTrainer

# Import output/export modules
from app.outputs.json_exporter import JSONExporter
from app.outputs.webhook_sender import WebhookSender
from app.outputs.report_writer import ReportWriter

# Initialize logger instance for CLI
logger = logging.getLogger("signalforge")


def dispatch(command, args, config, db):
    """
    Dispatch CLI commands based on user input.

    Args:
        command (str): CLI command provided by user.
        args (argparse.Namespace): CLI arguments provided by user.
        config (dict): Loaded and merged configuration settings.
        db (Database): Database connection instance.
    """

    if command == "scan":
        run_scan(args, config)

    elif command == "signal":
        run_signal(args, config)

    elif command == "train":
        run_train(config)

    elif command == "help":
        print_help()

    else:
        logger.error(f"Unknown command: {command}")
        print_help()


def run_scan(args, config):
    """
    Execute wallet scanning (without signal generation).

    Args:
        args (argparse.Namespace): CLI arguments provided by user.
        config (dict): Loaded configuration settings.
    """

    # Wallet address is mandatory for scan command
    if not args.wallet:
        logger.error("Wallet address required for scan command.")
        return

    # Initialize data collector with Coingecko API & RPC URL
    collector = DataCollector(
        coingecko_api=config["coingecko_api"],
        rpc_url=config["rpc_url"]
    )

    # Initialize wallet scanner
    scanner = WalletScanner(collector)

    # Analyze provided wallet
    result = scanner.analyze_wallet(args.wallet)

    # Log scan result to console and logs
    logger.info(f"Scan Result: {result}")


def run_signal(args, config):
    """
    Execute full signal generation workflow for a wallet.

    Args:
        args (argparse.Namespace): CLI arguments provided by user.
        config (dict): Loaded configuration settings.
    """

    # Wallet address is mandatory for signal command
    if not args.wallet:
        logger.error("Wallet address required for signal command.")
        return

    # Initialize all required modules for signal generation
    collector = DataCollector(
        coingecko_api=config["coingecko_api"],
        rpc_url=config["rpc_url"]
    )

    scanner = WalletScanner(collector)
    detector = PatternDetector(config)
    generator = SignalGenerator()
    assessor = RiskAssessor(config)
    exporter = JSONExporter()
    sender = WebhookSender(config)
    writer = ReportWriter()

    # Step 1: Analyze wallet
    wallet_analysis = scanner.analyze_wallet(args.wallet)

    # Step 2: Detect patterns based on analysis
    patterns = detector.detect_patterns(wallet_analysis)

    # Step 3: Generate signal structure
    signal = generator.generate_signal(wallet_analysis, patterns)

    # Step 4: Calculate risk score for the signal
    risk_score = assessor.calculate_risk_score(wallet_analysis, patterns)
    signal["risk_score"] = risk_score

    # Log final signal structure
    logger.info(f"Final Signal: {signal}")

    # Step 5: Export signal to JSON file
    exporter.save_signal(signal)

    # Step 6: Export signal as Markdown report
    writer.save_report(signal)

    # Step 7: Send signal to webhooks (Discord / Telegram)
    sender.send_signal(signal)


def run_train(config):
    """
    Execute interactive CLI pattern creation.

    Args:
        config (dict): Loaded configuration settings.
    """

    # Initialize pattern trainer
    trainer = ModelTrainer()

    # Interactive user input for pattern creation
    name = input("Enter pattern name: ")
    description = input("Enter pattern description: ")

    print("Enter conditions as key=value pairs. Type 'done' when finished.")

    conditions = {}

    # Loop until user types 'done'
    while True:
        user_input = input("> ")
        if user_input.lower() == "done":
            break
        try:
            key, value = user_input.split("=")
            conditions[key.strip()] = value.strip()
        except ValueError:
            print("Invalid format. Use key=value")

    # Add new pattern to strategy
    trainer.add_pattern(name, description, conditions)

    print("Pattern saved successfully.")


def print_help():
    """
    Print all available CLI commands and usage instructions.
    """

    print("Available Commands:")
    print("scan --wallet <address>       : Analyze a wallet")
    print("signal --wallet <address>     : Generate a full trading signal")
    print("train                         : Add a new custom pattern")
    print("help                          : Show this help message")
