import os
from app.core.ai_engine import AIEngine


def test_generate_comment():
    """
    Unit test for AIEngine.generate_comment().
    This test checks if the AI comment generation returns a string.
    The test will be skipped if no API key is found in the environment.
    """

    # Load OpenAI API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")

    # Skip test if no API key is available
    if not api_key:
        print("Skipping AIEngine test: OPENAI_API_KEY not found in environment.")
        return

    # Initialize the AI engine
    engine = AIEngine(api_key)

    # Dummy input data for testing
    dummy_wallet = {
        "wallet": "abc",
        "tokens_held": 8,
        "transaction_count": 3
    }

    dummy_patterns = [
        {"name": "Whale Wallet"}
    ]

    # Generate AI comment using dummy input
    comment = engine.generate_comment(dummy_wallet, dummy_patterns)

    # Assert the output is a string
    assert isinstance(comment, str), "Generated comment should be a string"

    # Optional: Print the comment during manual testing
    print("AI Comment:", comment)
