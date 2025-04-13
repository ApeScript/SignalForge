import os
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger("signalforge")


class WebhookSender:
    """
    WebhookSender sends signals to various endpoints like
    Discord, Telegram, or custom webhooks.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize WebhookSender.

        Args:
            config (dict): Configuration with webhook URLs.
        """
        # Webhook URLs from config
        self.discord_url = config.get("webhooks", {}).get("discord")
        self.telegram_token = config.get("webhooks", {}).get("telegram_token")
        self.telegram_chat_id = config.get("webhooks", {}).get("telegram_chat_id")
        self.custom_url = config.get("webhooks", {}).get("custom")

    def send_signal(self, signal: Dict[str, Any]) -> None:
        """
        Send signal to all configured webhook endpoints.

        Args:
            signal (dict): Signal to send.
        """
        # Send to Discord if URL provided
        if self.discord_url:
            self._send_discord(signal)

        # Send to Telegram if token & chat_id provided
        if self.telegram_token and self.telegram_chat_id:
            self._send_telegram(signal)

        # Send to custom endpoint if URL provided
        if self.custom_url:
            self._send_custom(signal)

    def _send_discord(self, signal: Dict[str, Any]) -> None:
        """
        Send signal to Discord webhook.

        Args:
            signal (dict): Signal to send.
        """
        # Build message content for Discord
        content = (
            f"New Signal: `{signal.get('signal')}`\n"
            f"Wallet: `{signal.get('wallet')}`\n"
            f"Reason: {signal.get('reason')}\n"
            f"Confidence: {signal.get('confidence')}"
        )

        payload = {"content": content}

        try:
            response = requests.post(self.discord_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Signal sent to Discord webhook.")
        except Exception as e:
            logger.error(f"Failed to send signal to Discord: {e}")

    def _send_telegram(self, signal: Dict[str, Any]) -> None:
        """
        Send signal to Telegram chat.

        Args:
            signal (dict): Signal to send.
        """
        # Build message content for Telegram
        content = (
            f"📈 *New Signal: {signal.get('signal')}*\n"
            f"Wallet: `{signal.get('wallet')}`\n"
            f"Reason: {signal.get('reason')}\n"
            f"Confidence: {signal.get('confidence')}"
        )

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"

        payload = {
            "chat_id": self.telegram_chat_id,
            "text": content,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Signal sent to Telegram.")
        except Exception as e:
            logger.error(f"Failed to send signal to Telegram: {e}")

    def _send_custom(self, signal: Dict[str, Any]) -> None:
        """
        Send signal to a custom webhook endpoint.

        Args:
            signal (dict): Signal to send.
        """
        try:
            response = requests.post(self.custom_url, json=signal, timeout=10)
            response.raise_for_status()
            logger.info("Signal sent to custom webhook.")
        except Exception as e:
            logger.error(f"Failed to send signal to custom webhook: {e}")
