from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class SignalModel:
    """
    SignalModel defines the structure of a generated trading signal.

    Attributes:
        wallet (str): Wallet address the signal belongs to.
        signal_type (str): The type of signal (e.g., BUY, HOLD, SELL).
        confidence (float): Confidence score of the signal (0.0 - 1.0).
        reason (str): Human-readable reason for the signal decision.
        ai_comment (Optional[str]): Optional AI-generated comment for extra context.
    """
    wallet: str
    signal_type: str
    confidence: float
    reason: str
    ai_comment: Optional[str] = None


@dataclass
class LogModel:
    """
    LogModel defines the structure of internal log records.

    Attributes:
        level (str): Log severity level (INFO, WARNING, ERROR).
        message (str): Log message content.
    """
    level: str
    message: str


@dataclass
class PatternModel:
    """
    PatternModel defines the structure of a user-defined trading pattern.

    Attributes:
        name (str): Pattern name (identifier).
        description (str): Short explanation of what this pattern does.
        conditions (Dict[str, Any]): Dict with pattern conditions (rule logic).
    """
    name: str
    description: str
    conditions: Dict[str, Any] = field(default_factory=dict)  # Ensures empty dict as default if not provided
