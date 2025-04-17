from app.core.data_collector import DataCollector


def test_fetch_token_price():
    """
    Test fetch_token_price() method.

    Verifies that the method returns a non-negative price for a known token.
    This ensures that the external API is reachable and returns valid data.
    """
    collector = DataCollector(
        coingecko_api="https://api.coingecko.com/api/v3",
        rpc_url="https://api.mainnet-beta.solana.com"
    )

    price = collector.fetch_token_price("solana")

    # Assert that price is a valid number and >= 0
    assert isinstance(price, (int, float)), "Token price should be numeric"
    assert price >= 0, "Token price should not be negative"


def test_fetch_wallet_balance():
    """
    Test fetch_wallet_balance() method.

    Verifies that the method returns a dictionary structure for any input wallet.
    Use a placeholder wallet for structure testing only.
    """
    collector = DataCollector(
        coingecko_api="https://api.coingecko.com/api/v3",
        rpc_url="https://api.mainnet-beta.solana.com"
    )

    # Use a dummy or devnet wallet; this test checks structure, not real values
    dummy_wallet = "Enter_Real_Wallet_Or_Devnet"
    result = collector.fetch_wallet_balance(dummy_wallet)

    # Assert structure
    assert isinstance(result, dict), "Wallet balance should return a dictionary"
    assert "wallet" in result or "value" in result, "Expected keys missing in wallet balance response"
