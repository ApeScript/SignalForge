# Import standard libraries
import os
import logging

# Import third-party libraries
import uvicorn
from fastapi import FastAPI

# Import local modules from SignalForge
from app.outputs.logger import setup_logger
from app.core.config_loader import ConfigLoader
from app.db.database import Database
from app.api.routes import register_routes

# Initialize logger instance for SignalForge
logger = logging.getLogger("signalforge")

# Setup logging configuration with log level INFO
setup_logger("INFO")

logger.info("Starting SignalForge API...")

# Initialize FastAPI app with metadata
app = FastAPI(
    title="SignalForge API",
    description="AI Driven Crypto Signal Framework",
    version="1.0.0"
)

# Dynamically detect base project directory
# This ensures correct path handling for both local & Docker environments
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load configuration files (base config + strategy config)
config_loader = ConfigLoader(
    base_config_path=os.path.join(BASE_DIR, "config", "base_config.yaml"),
    strategy_config_path=os.path.join(BASE_DIR, "config", "strategy_aggressive.yaml")
)

# Merge and load final configuration dictionary
config = config_loader.load_configs()

# If config loading failed → exit the app safely
if not config:
    logger.error("Failed to load configuration. Exiting.")
    exit(1)

# Initialize SQLite Database connection and tables
db = Database()

# Register all available API routes to FastAPI
register_routes(app, config, db)

# Entry point for local or Docker execution
# This runs the Uvicorn server on all network interfaces (0.0.0.0)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
