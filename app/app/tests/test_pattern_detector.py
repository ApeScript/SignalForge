from app.core.pattern_detector import PatternDetector


def test_detect_patterns():
    config = {
        "pattern_rules": {
            "whale_tokens": 10,
            "dormant_threshold": 3
        }
    }

    detector = PatternDetector(config)

    dummy_wallet = {
        "tokens_held": 12,
        "transaction_count": 1,
        "activity_type": "Low Activity",
        "wallet": "abc"
    }

    patterns = detector.detect_patterns(dummy_wallet)
    assert isinstance(patterns, list)
