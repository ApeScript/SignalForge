import logging
from app.core.data_collector import DataCollector
from app.core.wallet_scanner import WalletScanner
from app.core.pattern_detector import PatternDetector
from app.core.signal_generator import SignalGenerator
from app.core.risk_assessor import RiskAssessor
from app.core.model_trainer import ModelTrainer
from app.outputs.json_exporter import JSONExporter
from app.outputs.webhook_sender import WebhookSender
from app.outputs.report_writer import ReportWriter

logger = logging.getLogger("signalforge")


def dispatch(command, args, config, db):
    """
    Dispatch CLI commands.

    Args:
        command (str): CLI command name.
        args (argparse.Namespace): CLI arguments.
        config (dict): Loaded config.
        db (Database): Database instance.
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
    Run wallet analysis.

    Args:
        args (argparse.Namespace): CLI arguments.
        config (dict): Loaded config.
    """
    if not args.wallet:
        logger.error("Wallet address required for scan command.")
        return

    collector = DataCollector(
        coingecko_api=config["coingecko_api"],
        rpc_url=config["rpc_url"]
    )

    scanner = WalletScanner(collector)
    result = scanner.analyze_wallet(args.wallet)

    logger.info(f"Scan Result: {result}")


def run_signal(args, config):
    """
    Run full signal generation.

    Args:
        args (argparse.Namespace): CLI arguments.
        config (dict): Loaded config.
    """
    if not args.wallet:
        logger.error("Wallet address required for signal command.")
        return

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

    wallet_analysis = scanner.analyze_wallet(args.wallet)
    patterns = detector.detect_patterns(wallet_analysis)
    signal = generator.generate_signal(wallet_analysis, patterns)
    risk_score = assessor.calculate_risk_score(wallet_analysis, patterns)

    signal["risk_score"] = risk_score

    logger.info(f"Final Signal: {signal}")

    # Export
    exporter.save_signal(signal)
    writer.save_report(signal)
    sender.send_signal(signal)


def run_train(config):
    """
    Run pattern trainer.

    Args:
        config (dict): Loaded config.
    """
    trainer = ModelTrainer()

    name = input("Enter pattern name: ")
    description = input("Enter pattern description: ")

    print("Enter conditions as key=value pairs. Type 'done' when finished.")
    conditions = {}

    while True:
        user_input = input("> ")
        if user_input.lower() == "done":
            break
        try:
            key, value = user_input.split("=")
            conditions[key.strip()] = value.strip()
        except ValueError:
            print("Invalid format. Use key=value")

    trainer.add_pattern(name, description, conditions)
    print("Pattern saved successfully.")


def print_help():
    """
    Print available commands.
    """
    print("Available Commands:")
    print("scan --wallet <address>       : Analyze a wallet")
    print("signal --wallet <address>     : Generate a full trading signal")
    print("train                         : Add a new custom pattern")
    print("help                          : Show this help message")
