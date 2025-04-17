from app.core.pattern_detector import PatternDetector


def test_detect_patterns():
    """
    Test detect_patterns() method from PatternDetector.

    Verifies that the method returns a list of pattern dictionaries based on 
    wallet activity, token count, and configured thresholds.
    """
    # Minimal config with pattern detection thresholds
    config = {
        "pattern_rules": {
            "whale_tokens": 10,          # Flag wallet as whale if tokens_held >= 10
            "dormant_threshold": 3       # Used for detecting awakened dormant wallets
        }
    }

    # Dummy wallet data that should match at least one rule (whale)
    dummy_wallet = {
        "tokens_held": 12,              # Exceeds whale threshold
        "transaction_count": 1,         # Low transaction count
        "activity_type": "Low Activity",
        "wallet": "abc"
    }

    # Instantiate pattern detector with mock config
    detector = PatternDetector(config)

    # Run pattern detection
    patterns = detector.detect_patterns(dummy_wallet)

    # Assert return is a list
    assert isinstance(patterns, list), "Output should be a list"

    # Optional: check structure of detected pattern
    if patterns:
        assert "name" in patterns[0], "Each pattern should have a 'name'"
        assert "description" in patterns[0], "Each pattern should have a 'description'"
