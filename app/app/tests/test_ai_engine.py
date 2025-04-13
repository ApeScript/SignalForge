import os
from app.core.ai_engine import AIEngine


def test_generate_comment():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return

    engine = AIEngine(api_key)
    comment = engine.generate_comment(
        {"wallet": "abc", "tokens_held": 8, "transaction_count": 3},
        [{"name": "Whale Wallet"}]
    )
    assert isinstance(comment, str)
