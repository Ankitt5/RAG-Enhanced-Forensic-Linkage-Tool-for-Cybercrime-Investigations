import os
import json
from typing import List, Dict, Any

from chat_parser import parse_chat_logs
from telegram_parser import parse_telegram_export

try:
    from network_parser import parse_network_telemetry
except ImportError:
    parse_network_telemetry = None

try:
    from crypto_parser import parse_crypto_transactions
except ImportError:
    parse_crypto_transactions = None

try:
    from pcap_parser import parse_pcap
except ImportError:
    parse_pcap = None


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "parsed_evidence.json")


def run_parser_pipeline() -> List[Dict[str, Any]]:
    """Combine evidence from all available evidence parsers."""

    all_parsed = []

    # 1. Discord-style chat export
    chat_file = os.path.join(DATA_DIR, "chat_export.txt")
    chat_records = parse_chat_logs(chat_file)
    all_parsed.extend(chat_records)
    print(f"[+] Chat parser: {len(chat_records)} records")

    # 2. Telegram JSON export
    telegram_file = os.path.join(DATA_DIR, "telegram_export.json")
    telegram_records = parse_telegram_export(telegram_file)
    all_parsed.extend(telegram_records)
    print(f"[+] Telegram parser: {len(telegram_records)} records")

    # 3. Network telemetry / NetFlow-like CSV
    net_file = os.path.join(DATA_DIR, "network_telemetry.csv")

    if parse_network_telemetry:
        net_records = parse_network_telemetry(net_file)
        all_parsed.extend(net_records)
        print(f"[+] Network parser: {len(net_records)} records")
    else:
        print("[!] Network parser is unavailable.")

    # 4. PCAP packet capture
    pcap_file = os.path.join(DATA_DIR, "test_traffic.pcap")

    if parse_pcap:
        if os.path.exists(pcap_file):
            pcap_records = parse_pcap(pcap_file)
            all_parsed.extend(pcap_records)
            print(f"[+] PCAP parser: {len(pcap_records)} records")
        else:
            print(f"[!] PCAP file not found: {pcap_file}")
    else:
        print("[!] PCAP parser is unavailable.")


    # Save the combined standardized evidence records
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_parsed, file, indent=2, ensure_ascii=False)

    print(f"\n[PASS] Pipeline complete: {len(all_parsed)} total records")
    print(f"[PASS] Standardized evidence saved to: {OUTPUT_FILE}")

    return all_parsed


if __name__ == "__main__":
    run_parser_pipeline()