import requests

from logforge.logger import setup_logger
from logforge.utils import truncate

logger = setup_logger("notifier")


class Notifier:
    def __init__(self, channels_config):
        self.channels_config = channels_config if channels_config else []

    def _send_telegram(self, config, message, title):
        full_message = f"{title}\n\n{message}"
        full_message = truncate(full_message, 4096, preserve_newlines=True, suffix="\n[TRUNCATED]")
        payload = {"chat_id": config["chat_id"], "text": full_message}
        api_url = f"https://api.telegram.org/bot{config['token']}/sendMessage"
        try:
            response = requests.post(api_url, data=payload, timeout=10)
            response.raise_for_status()
            if not response.json().get("ok"):
                logger.error(
                    f"telegram api error for {config.get('name', 'telegram')}: {response.json().get('description')}"
                )
                return
            logger.info(f"successfully sent telegram message for {config.get('name', 'telegram')}")
        except requests.exceptions.RequestException as e:
            logger.error(f"failed to send telegram message for {config.get('name', 'telegram')}: {e}")
        except Exception as ex:
            logger.error(f"non-request error sending telegram message for {config.get('name', 'telegram')}: {ex}")

    def _send_slack(self, config, message, title):
        full_message = f"*{title}*\n\n{message}"
        full_message = truncate(full_message, 4000, preserve_newlines=True, suffix="\n[TRUNCATED]")
        payload = {"text": full_message}
        try:
            response = requests.post(config["webhook_id"], json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"successfully sent slack message for {config.get('name', 'slack')}")
        except requests.exceptions.RequestException as e:
            logger.error(
                f"failed to send slack message for {config.get('name', 'slack')}: {e} (make sure webhook url is correct"
                " and active)"
            )

    def _send_discord(self, config, message, title):
        full_message = f"**{title}**\n\n{message}"
        full_message = truncate(full_message, 2000, preserve_newlines=True, suffix="\n[TRUNCATED]")
        payload = {"content": full_message}
        try:
            response = requests.post(config["webhook_id"], json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"successfully sent discord message for {config.get('name', 'discord')}")
        except requests.exceptions.RequestException as e:
            logger.error(
                f"failed to send discord message for {config.get('name', 'discord')}: {e} (make sure webhook url is"
                " correct and active)"
            )

    def _send_gotify(self, config, message, title):
        message = truncate(message, 32768, preserve_newlines=True, suffix="\n[TRUNCATED]")
        target_url = f"{config['server_url'].rstrip('/')}/message?token={config['token']}"
        payload = {"title": title, "message": message, "priority": config.get("priority", 5)}
        try:
            response = requests.post(target_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"successfully sent gotify message for {config.get('name', 'gotify')}")
        except requests.exceptions.RequestException as e:
            logger.error(f"failed to send gotify message for {config.get('name', 'gotify')}: {e}")

    def send_message(self, message_body, title="LogForge notification"):
        if not self.channels_config:
            logger.warning("no notification channels configured")
            return
        for channel_conf_wrapper in self.channels_config:
            if not channel_conf_wrapper.get("enabled", False):
                logger.debug(f"skipping disabled channel: {channel_conf_wrapper.get('name', 'unnamed channel')}")
                continue
            channel_type = channel_conf_wrapper.get("type")
            specific_config = channel_conf_wrapper.get("config", {})
            specific_config["name"] = channel_conf_wrapper.get("name", f"unnamed {channel_type}")
            if not specific_config:
                logger.warning(f"channel {channel_conf_wrapper.get('name')} is enabled but has no specific config")
                continue
            try:
                if channel_type == "telegram":
                    if "token" in specific_config and "chat_id" in specific_config:
                        self._send_telegram(specific_config, message_body, title)
                    else:
                        logger.error(f"telegram channel {specific_config['name']} missing token or chat_id")
                elif channel_type == "slack":
                    if "webhook_id" in specific_config:
                        self._send_slack(specific_config, message_body, title)
                    else:
                        logger.error(f"slack channel {specific_config['name']} missing webhook_id")
                elif channel_type == "discord":
                    if "webhook_id" in specific_config:
                        self._send_discord(specific_config, message_body, title)
                    else:
                        logger.error(f"discord channel {specific_config['name']} missing webhook_id")
                elif channel_type == "gotify":
                    if "server_url" in specific_config and "token" in specific_config:
                        self._send_gotify(specific_config, message_body, title)
                    else:
                        logger.error(f"gotify channel {specific_config['name']} missing server_url or token")
                else:
                    logger.warning(
                        f"unsupported notification channel type: {channel_type} for {specific_config['name']}"
                    )
            except Exception as e:
                logger.error(f"unhandled error processing channel {specific_config['name']} ({channel_type}): {e}")
