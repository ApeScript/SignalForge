import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.core.data_collector import DataCollector
from app.core.wallet_scanner import WalletScanner
from app.core.pattern_detector import PatternDetector
from app.core.signal_generator import SignalGenerator
from app.core.risk_assessor import RiskAssessor
from app.core.model_trainer import ModelTrainer

logger = logging.getLogger("signalforge")


class WalletRequest(BaseModel):
    wallet: str


class TrainRequest(BaseModel):
    name: str
    description: str
    conditions: Dict[str, Any]


def register_routes(app: FastAPI, config: Dict[str, Any], db) -> None:
    """
    Register all API routes.

    Args:
        app (FastAPI): FastAPI instance.
        config (dict): Loaded config.
        db (Database): Database instance.
    """

    @app.get("/status")
    def status():
        return {"status": "SignalForge API is running."}

    @app.post("/scan")
    def scan_wallet(req: WalletRequest):
        collector = DataCollector(
            coingecko_api=config["coingecko_api"],
            rpc_url=config["rpc_url"]
        )
        scanner = WalletScanner(collector)
        result = scanner.analyze_wallet(req.wallet)
        return result

    @app.post("/signal")
    def generate_signal(req: WalletRequest):
        collector = DataCollector(
            coingecko_api=config["coingecko_api"],
            rpc_url=config["rpc_url"]
        )
        scanner = WalletScanner(collector)
        detector = PatternDetector(config)
        generator = SignalGenerator()
        assessor = RiskAssessor(config)

        wallet_analysis = scanner.analyze_wallet(req.wallet)
        patterns = detector.detect_patterns(wallet_analysis)
        signal = generator.generate_signal(wallet_analysis, patterns)
        risk_score = assessor.calculate_risk_score(wallet_analysis, patterns)
        signal["risk_score"] = risk_score

        return signal

    @app.post("/train")
    def train_pattern(req: TrainRequest):
        trainer = ModelTrainer()
        trainer.add_pattern(req.name, req.description, req.conditions)
        return {"message": "Pattern saved successfully."}
