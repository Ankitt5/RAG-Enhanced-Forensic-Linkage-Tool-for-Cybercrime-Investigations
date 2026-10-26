import os
import re
from datetime import datetime, timezone
from typing import List, Dict, Any


def parse_chat_logs(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse chat export files into the standardized evidence JSON schema.
    Supports messages with optional channel information.
    """
    parsed_records = []

    if not os.path.exists(file_path):
        print(f"[!] Warning: Chat log file not found at {file_path}")
        return parsed_records

    chat_pattern = re.compile(
        r"^\[(?P<timestamp>[^\]]+)\]\s+"
        r"(?:\[CHANNEL:\s*(?P<channel>[^\]]+)\]\s+)?"
        r"@?(?P<sender>[\w#-]+):\s+"
        r"(?P<message>.+)$"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            match = chat_pattern.match(line)

            if match:
                data = match.groupdict()
                timestamp = data["timestamp"].strip()

                # Validate and normalize the original timestamp.
                try:
                    parsed_timestamp = datetime.fromisoformat(
                        timestamp.replace("Z", "+00:00")
                    )

                    if parsed_timestamp.tzinfo is None:
                        parsed_timestamp = parsed_timestamp.replace(
                            tzinfo=timezone.utc
                        )

                    timestamp = parsed_timestamp.isoformat()

                except ValueError:
                    print(
                        f"[!] Invalid timestamp at chat line {idx}; "
                        "preserving the original line as raw text."
                    )
                    parsed_records.append({
                        "evidence_id": f"EV-CHAT-{idx:04d}",
                        "source_type": "chat",
                        "source_format": "raw_text",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "raw_content": line,
                        "metadata": {
                            "sender": "unknown",
                            "platform": "generic",
                        },
                    })
                    continue

                sender = data["sender"]
                channel = data["channel"]
                platform = "discord" if channel and channel.startswith("#") else "generic"

                metadata = {
                    "sender": sender,
                    "message_body": data["message"],
                    "platform": platform,
                }

                if channel:
                    metadata["channel"] = channel

                record = {
                    "evidence_id": f"EV-CHAT-{idx:04d}",
                    "source_type": "chat",
                    "source_format": platform,
                    "timestamp": timestamp,
                    "raw_content": line,
                    "metadata": metadata,
                }

            else:
                record = {
                    "evidence_id": f"EV-CHAT-{idx:04d}",
                    "source_type": "chat",
                    "source_format": "raw_text",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "raw_content": line,
                    "metadata": {
                        "sender": "unknown",
                        "platform": "generic",
                    },
                }

            parsed_records.append(record)

    return parsed_records