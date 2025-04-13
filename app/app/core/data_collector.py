import requests
import json
import time
import logging

# Initialize logger
logger = logging.getLogger("signalforge")


class DataCollector:
    """
    DataCollector is responsible for fetching blockchain 
    data and token prices from external APIs (RPC & CoinGecko).
    """

    def __init__(self, coingecko_api: str, rpc_url: str):
        """
        Initialize the DataCollector with API endpoints.

        Args:
            coingecko_api (str): CoinGecko API base URL.
            rpc_url (str): RPC URL for blockchain data.
        """
        self.coingecko_api = coingecko_api
        self.rpc_url = rpc_url

    def fetch_token_price(self, token_id: str) -> float:
        """
        Fetch real-time token price in USD from CoinGecko.

        Args:
            token_id (str): Token identifier for CoinGecko API.

        Returns:
            float: Token price or 0.0 on failure.
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
        Fetch token balances of a wallet using blockchain RPC.

        Args:
            wallet_address (str): Blockchain wallet address.

        Returns:
            dict: Token balances result with "empty" flag if no holdings found.
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

            # Extra flag for empty wallets
            if not result.get("value"):
                result["empty"] = True
                logger.info(f"Wallet {wallet_address} is empty.")
            else:
                result["empty"] = False
                logger.info(f"Fetched wallet balance for {wallet_address}")

            return result

        except Exception as e:
            logger.error(f"Failed to fetch wallet balance for {wallet_address}: {e}")
            return {"empty": True}

    def fetch_recent_transactions(self, wallet_address: str, limit: int = 10) -> list:
        """
        Fetch recent transaction signatures for a given wallet.

        Args:
            wallet_address (str): Blockchain wallet address.
            limit (int): Max number of transactions to fetch.

        Returns:
            list: List of transaction signatures or empty list on failure.
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

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            try:
                response = requests.post(self.rpc_url, json=payload, timeout=10)
                response.raise_for_status()
                transactions = response.json().get("result", [])

                logger.info(f"Fetched {len(transactions)} transactions for {wallet_address}")
                return transactions

            except Exception as e:
                attempts += 1
                logger.warning(f"Attempt {attempts}/{max_attempts} failed to fetch transactions for {wallet_address}: {e}")
                time.sleep(1)

        logger.error(f"Failed to fetch transactions for {wallet_address} after {max_attempts} attempts.")
        return []
