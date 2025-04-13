import os
import logging
import uvicorn
from fastapi import FastAPI

from app.outputs.logger import setup_logger
from app.core.config_loader import ConfigLoader
from app.db.database import Database
from app.api.routes import register_routes

logger = logging.getLogger("signalforge")

# Initialize Logger
setup_logger("INFO")

logger.info("Starting SignalForge API...")

# Initialize App
app = FastAPI(
    title="SignalForge API",
    description="AI Driven Crypto Signal Framework",
    version="1.0.0"
)

# Base Path Detection → wichtig für Docker & Local
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load Config
config_loader = ConfigLoader(
    base_config_path=os.path.join(BASE_DIR, "config", "base_config.yaml"),
    strategy_config_path=os.path.join(BASE_DIR, "config", "strategy_aggressive.yaml")
)

config = config_loader.load_configs()

if not config:
    logger.error("Failed to load configuration. Exiting.")
    exit(1)

# Init DB
db = Database()

# Register API Routes
register_routes(app, config, db)

# For local & docker run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
