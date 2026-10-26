import os
import json
from typing import List, Dict, Any

# Import Anshuman's module
from chat_parser import parse_chat_logs

# Gracefully attempt to import Ankit's modules when present
try:
    from network_parser import parse_network_telemetry
except ImportError:
    parse_network_telemetry = None

try:
    from crypto_parser import parse_crypto_transactions
except ImportError:
    parse_crypto_transactions = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "parsed_evidence.json")


def run_parser_pipeline() -> List[Dict[str, Any]]:
    """
    Master Ingestion Pipeline: Combines outputs from chat, network, and crypto modules.
    """
    chat_file = os.path.join(DATA_DIR, "chat_export.txt")
    net_file = os.path.join(DATA_DIR, "network_telemetry.csv")
    crypto_file = os.path.join(DATA_DIR, "crypto_transactions.csv")

    all_parsed = []

    # 1. Run Anshuman's Chat Parser
    chat_records = parse_chat_logs(chat_file)
    all_parsed.extend(chat_records)
    print(f"[+] Anshuman (Chat Parser): Processed {len(chat_records)} chat records.")

    # 2. Run Ankit's Network Telemetry Parser (if merged)
    if parse_network_telemetry:
        net_records = parse_network_telemetry(net_file)
        all_parsed.extend(net_records)
        print(f"[+] Ankit (Network Parser): Processed {len(net_records)} network records.")
    else:
        print("[!] Ankit's network_parser module is not yet merged.")

    # 3. Run Ankit's Crypto Ledger Parser (if merged)
    if parse_crypto_transactions:
        crypto_records = parse_crypto_transactions(crypto_file)
        all_parsed.extend(crypto_records)
        print(f"[+] Ankit (Crypto Parser): Processed {len(crypto_records)} crypto records.")
    else:
        print("[!] Ankit's crypto_parser module is not yet merged.")

    # Save output to standardized evidence JSON schema
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_parsed, f, indent=2)

    print(f"[PASS] Pipeline complete. Total evidence records in output: {len(all_parsed)}")
    print(f"[PASS] Standardized evidence saved to: {OUTPUT_FILE}")
    return all_parsed


if __name__ == "__main__":
    run_parser_pipeline()