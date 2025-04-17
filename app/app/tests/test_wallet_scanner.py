# Import WalletScanner and DataCollector from core modules
from app.core.wallet_scanner import WalletScanner
from app.core.data_collector import DataCollector


def test_analyze_wallet():
    """
    Unit test for WalletScanner.analyze_wallet().
    This test checks whether the returned result contains
    required fields like 'tokens_held' and 'activity_type'.
    """

    # Initialize the DataCollector with public APIs (can be replaced with mocks if needed)
    collector = DataCollector(
        coingecko_api="https://api.coingecko.com/api/v3",         # Coingecko API for token prices
        rpc_url="https://api.mainnet-beta.solana.com"             # Solana RPC endpoint for wallet data
    )

    # Initialize the WalletScanner using the collector
    scanner = WalletScanner(collector)

    # NOTE: Replace this with a real wallet or devnet address when testing
    wallet_address = "Enter_Real_Wallet_Or_Devnet"

    # Run the wallet analysis
    result = scanner.analyze_wallet(wallet_address)

    # Basic assertions to verify expected keys exist in result
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "tokens_held" in result, "'tokens_held' key missing in result"
    assert "activity_type" in result, "'activity_type' key missing in result"

    # Optional: You could also add extra validations like expected data types
    assert isinstance(result["tokens_held"], int), "'tokens_held' should be an integer"
    assert isinstance(result["activity_type"], str), "'activity_type' should be a string"
