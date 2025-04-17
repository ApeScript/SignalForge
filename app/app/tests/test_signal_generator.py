from app.core.signal_generator import SignalGenerator


def test_generate_signal():
    """
    Test generate_signal() method from SignalGenerator.

    Ensures the generated signal contains expected keys and valid types
    based on dummy wallet analysis and detected patterns.
    """
    # Instantiate the signal generator without AI (default fallback mode)
    generator = SignalGenerator()

    # Dummy wallet data input
    dummy_wallet = {
        "wallet": "abc",
        "tokens_held": 8,
        "transaction_count": 3,
        "activity_type": "Low Activity"
    }

    # Simulated pattern detection results
    patterns = [
        {"name": "Whale Wallet", "description": "Big holder"}
    ]

    # Generate the signal
    signal = generator.generate_signal(dummy_wallet, patterns)

    # Core structure checks
    assert isinstance(signal, dict), "Signal output should be a dictionary"
    assert "signal" in signal, "'signal' field should be present"
    assert "confidence" in signal, "'confidence' field should be present"
    assert "wallet" in signal, "'wallet' field should be present"
    assert "reason" in signal, "'reason' field should be present"
    assert "ai_comment" in signal, "'ai_comment' field should be present"

    # Value type checks
    assert isinstance(signal["signal"], str), "Signal type must be a string"
    assert isinstance(signal["confidence"], float), "Confidence must be a float"
    assert 0.0 <= signal["confidence"] <= 1.0, "Confidence must be between 0.0 and 1.0"
