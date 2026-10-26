import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any


def parse_telegram_export(file_path: str) -> List[Dict[str, Any]]:
    """Parse a Telegram JSON export into standardized evidence records."""

    records = []

    if not os.path.exists(file_path):
        print(f"[!] Telegram export not found: {file_path}")
        return records

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            export_data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"[!] Could not read Telegram export: {error}")
        return records

    messages = export_data.get("messages", [])

    for message in messages:
        if message.get("type") != "message":
            continue

        message_id = message.get("id", len(records) + 1)
        timestamp = message.get("date")

        if timestamp:
            try:
                parsed_date = datetime.fromisoformat(
                    timestamp.replace("Z", "+00:00")
                )

                if parsed_date.tzinfo is None:
                    parsed_date = parsed_date.replace(tzinfo=timezone.utc)

                timestamp = parsed_date.isoformat()

            except ValueError:
                timestamp = datetime.now(timezone.utc).isoformat()
        else:
            timestamp = datetime.now(timezone.utc).isoformat()

        text = message.get("text", "")

        # Telegram exports may contain strings or lists of text objects.
        if isinstance(text, list):
            text = "".join(
                item if isinstance(item, str)
                else str(item.get("text", ""))
                for item in text
            )

        sender = message.get("from", "unknown")

        record = {
            "evidence_id": f"EV-TELEGRAM-{message_id}",
            "source_type": "chat",
            "source_format": "telegram",
            "timestamp": timestamp,
            "raw_content": str(text),
            "metadata": {
                "sender": sender,
                "platform": "telegram",
                "chat_name": export_data.get("name", "unknown"),
                "message_id": message_id
            }
        }

        records.append(record)

    return records