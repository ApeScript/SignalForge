from app.core.signal_generator import SignalGenerator


def test_generate_signal():
    generator = SignalGenerator()

    dummy_wallet = {
        "wallet": "abc",
        "tokens_held": 8,
        "transaction_count": 3,
        "activity_type": "Low Activity"
    }

    patterns = [{"name": "Whale Wallet", "description": "Big holder"}]

    signal = generator.generate_signal(dummy_wallet, patterns)
    assert "signal" in signal
    assert "confidence" in signal
