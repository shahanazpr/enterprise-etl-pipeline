import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_slack_message(message):
    webhook = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook or webhook == "YOUR_SLACK_WEBHOOK_URL":
        print("⚠ Slack webhook not configured.")
        return

    payload = {"text": message}

    try:
        response = requests.post(webhook, json=payload, timeout=10)
        response.raise_for_status()

        print("✅ Slack notification sent.")

    except Exception as e:
        print(f"❌ Slack notification failed: {e}")