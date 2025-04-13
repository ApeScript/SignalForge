from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SignalModel:
    """
    SignalModel defines the structure for a trading signal.
    """
    wallet: str
    signal_type: str
    confidence: float
    reason: str
    ai_comment: Optional[str] = None


@dataclass
class LogModel:
    """
    LogModel defines the structure for internal log messages.
    """
    level: str
    message: str


@dataclass
class PatternModel:
    """
    PatternModel defines the structure for user-defined patterns.
    """
    name: str
    description: str
    conditions: Dict[str, Any]
