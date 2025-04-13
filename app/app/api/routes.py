# Import standard libraries
import logging

# Import FastAPI framework components
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Import core modules from SignalForge
from app.core.data_collector import DataCollector
from app.core.wallet_scanner import WalletScanner
from app.core.pattern_detector import PatternDetector
from app.core.signal_generator import SignalGenerator
from app.core.risk_assessor import RiskAssessor
from app.core.model_trainer import ModelTrainer

# Initialize logger for SignalForge
logger = logging.getLogger("signalforge")

# Request model for wallet-based API calls
class WalletRequest(BaseModel):
    wallet: str

# Request model for training new custom patterns
class TrainRequest(BaseModel):
    name: str
    description: str
    conditions: Dict[str, Any]

def register_routes(app: FastAPI, config: Dict[str, Any], db) -> None:
    """
    Register all available API routes for SignalForge.

    Args:
        app (FastAPI): FastAPI instance
        config (dict): Loaded configuration dictionary
        db (Database): Database instance
    """

    @app.get("/status")
    def status():
        """
        API Health Check Route.

        Returns:
            dict: API running status message
        """
        return {"status": "SignalForge API is running."}

    @app.post("/scan")
    def scan_wallet(req: WalletRequest):
        """
        Scan a wallet without generating a signal.
        Pure analysis only.

        Args:
            req (WalletRequest): Wallet address input from user

        Returns:
            dict: Wallet analysis results
        """
        # Initialize DataCollector and WalletScanner
        collector = DataCollector(
            coingecko_api=config["coingecko_api"],
            rpc_url=config["rpc_url"]
        )
        scanner = WalletScanner(collector)

        # Perform wallet analysis
        result = scanner.analyze_wallet(req.wallet)

        return result

    @app.post("/signal")
    def generate_signal(req: WalletRequest):
        """
        Generate a full signal for a wallet.
        Includes analysis, pattern detection, signal building, and risk score.

        Args:
            req (WalletRequest): Wallet address input from user

        Returns:
            dict: Final signal object with risk score
        """
        # Initialize required core modules
        collector = DataCollector(
            coingecko_api=config["coingecko_api"],
            rpc_url=config["rpc_url"]
        )
        scanner = WalletScanner(collector)
        detector = PatternDetector(config)
        generator = SignalGenerator()
        assessor = RiskAssessor(config)

        # Analyze wallet
        wallet_analysis = scanner.analyze_wallet(req.wallet)

        # Detect patterns based on strategy rules
        patterns = detector.detect_patterns(wallet_analysis)

        # Generate signal object
        signal = generator.generate_signal(wallet_analysis, patterns)

        # Calculate risk score and attach to signal
        risk_score = assessor.calculate_risk_score(wallet_analysis, patterns)
        signal["risk_score"] = risk_score

        return signal

    @app.post("/train")
    def train_pattern(req: TrainRequest):
        """
        Add a new user-defined pattern to the system.

        Args:
            req (TrainRequest): Pattern name, description, and conditions provided by user

        Returns:
            dict: Confirmation message
        """
        trainer = ModelTrainer()

        # Save pattern to database
        trainer.add_pattern(req.name, req.description, req.conditions)

        return {"message": "Pattern saved successfully."}
