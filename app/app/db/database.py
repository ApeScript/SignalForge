import sqlite3
import os
import logging

logger = logging.getLogger("signalforge")


class Database:
    """
    Database class handles SQLite connection and
    initializes required tables for SignalForge.
    """

    def __init__(self, db_path: str = None):
        """
        Initialize Database.

        Args:
            db_path (str): Path to SQLite database file.
        """
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(base_dir, "signalforge.db")
        else:
            self.db_path = db_path

        self.connection = None
        self._connect()
        self._create_tables()

    def _connect(self) -> None:
        """
        Establish connection to the database.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            logger.info(f"Connected to SQLite database at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")

    def _create_tables(self) -> None:
        """
        Create necessary tables if not exists.
        """
        try:
            cursor = self.connection.cursor()

            # Table for Signals
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wallet TEXT NOT NULL,
                    signal_type TEXT NOT NULL,
                    confidence REAL,
                    reason TEXT,
                    ai_comment TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table for Logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table for User-Defined Patterns
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT,
                    conditions TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.connection.commit()
            logger.info("Database tables created successfully.")

        except sqlite3.Error as e:
            logger.error(f"Failed to create tables: {e}")

    def get_connection(self):
        """
        Get active SQLite connection.

        Returns:
            sqlite3.Connection: Active database connection.
        """
        return self.connection
