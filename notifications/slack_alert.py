import requests


def send_slack_message(message, webhook_url):
    """
    Sends a Slack notification.
    """

    payload = {"text": message}

    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except Exception as e:
        print(f"Slack Error: {e}")