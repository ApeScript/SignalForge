from app.core.data_collector import DataCollector


def test_fetch_token_price():
    collector = DataCollector(
        coingecko_api="https://api.coingecko.com/api/v3",
        rpc_url="https://api.mainnet-beta.solana.com"
    )
    price = collector.fetch_token_price("solana")
    assert price >= 0


def test_fetch_wallet_balance():
    collector = DataCollector(
        coingecko_api="https://api.coingecko.com/api/v3",
        rpc_url="https://api.mainnet-beta.solana.com"
    )
    result = collector.fetch_wallet_balance("Enter_Real_Wallet_Or_Devnet")
    assert isinstance(result, dict)
