import os
import re
from datetime import datetime, timezone
from typing import List, Dict, Any


def parse_chat_logs(file_path: str) -> List[Dict[str, Any]]:
    """
    Anshuman's Module: Parses unstructured Telegram and Discord chat export files
    into the standardized evidence JSON schema.
    """
    parsed_records = []
    if not os.path.exists(file_path):
        print(f"[!] Warning: Chat log file not found at {file_path}")
        return parsed_records

    # Regex pattern to match timestamp, sender, and message content
    chat_pattern = re.compile(
        r"^\[(?P<timestamp>[\d\-:\s]+)\]\s+@?(?P<sender>[\w#]+):\s+(?P<message>.+)$"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            match = chat_pattern.match(line)
            if match:
                data = match.groupdict()
                sender = data["sender"]
                platform = "discord" if "#" in sender else "telegram"

                record = {
                    "evidence_id": f"EV-CHAT-{idx:04d}",
                    "source_type": "chat",
                    "source_format": platform,
                    "timestamp": data["timestamp"].replace(" ", "T") + "Z",
                    "raw_content": line,
                    "metadata": {
                        "sender": sender,
                        "message_body": data["message"],
                        "platform": platform,
                    },
                }
            else:
                record = {
                    "evidence_id": f"EV-CHAT-{idx:04d}",
                    "source_type": "chat",
                    "source_format": "raw_text",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "raw_content": line,
                    "metadata": {"sender": "unknown", "platform": "generic"},
                }
            parsed_records.append(record)

    return parsed_records