import requests
import json
import time
import logging

logger = logging.getLogger("signalforge")

class DataCollector:
    """
    DataCollector fetches price and on-chain data
    for tokens and wallets.
    """

    def __init__(self, coingecko_api: str, rpc_url: str):
        """
        Initialize the DataCollector.

        Args:
            coingecko_api (str): Base URL for CoinGecko API.
            rpc_url (str): RPC endpoint for blockchain queries.
        """
        self.coingecko_api = coingecko_api
        self.rpc_url = rpc_url

    def fetch_token_price(self, token_id: str) -> float:
        """
        Fetch the current price of a token from CoinGecko.

        Args:
            token_id (str): CoinGecko token id (e.g. 'solana')

        Returns:
            float: Current price in USD or 0.0 on failure.
        """
        url = f"{self.coingecko_api}/simple/price?ids={token_id}&vs_currencies=usd"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = data.get(token_id, {}).get('usd', 0.0)
            logger.info(f"Fetched price for {token_id}: ${price}")
            return price
        except Exception as e:
            logger.error(f"Failed to fetch price for {token_id}: {e}")
            return 0.0

    def fetch_wallet_balance(self, wallet_address: str) -> dict:
        """
        Fetch token balances of a wallet using RPC.

        Args:
            wallet_address (str): Blockchain wallet address.

        Returns:
            dict: Token balances or empty dict on failure.
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [
                wallet_address,
                {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
                {"encoding": "jsonParsed"}
            ]
        }
        try:
            response = requests.post(self.rpc_url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json().get("result", {})
            logger.info(f"Fetched wallet balance for {wallet_address}")
            return result
        except Exception as e:
            logger.error(f"Failed to fetch wallet balance for {wallet_address}: {e}")
            return {}

    def fetch_recent_transactions(self, wallet_address: str, limit: int = 10) -> list:
        """
        Fetch recent transactions of a wallet.

        Args:
            wallet_address (str): Wallet address.
            limit (int): Number of transactions to fetch.

        Returns:
            list: List of transactions.
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                wallet_address,
                {"limit": limit}
            ]
        }
        try:
            response = requests.post(self.rpc_url, json=payload, timeout=10)
            response.raise_for_status()
            transactions = response.json().get("result", [])
            logger.info(f"Fetched {len(transactions)} transactions for {wallet_address}")
            return transactions
        except Exception as e:
            logger.error(f"Failed to fetch transactions for {wallet_address}: {e}")
            return []

