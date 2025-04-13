from app.core.wallet_scanner import WalletScanner
from app.core.data_collector import DataCollector


def test_analyze_wallet():
    collector = DataCollector(
        coingecko_api="https://api.coingecko.com/api/v3",
        rpc_url="https://api.mainnet-beta.solana.com"
    )
    scanner = WalletScanner(collector)
    result = scanner.analyze_wallet("Enter_Real_Wallet_Or_Devnet")
    assert "tokens_held" in result
    assert "activity_type" in result
