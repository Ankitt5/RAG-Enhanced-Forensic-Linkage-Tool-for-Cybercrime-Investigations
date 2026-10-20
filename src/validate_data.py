import os

def validate_corpus():
    required_files = {
        "data/chat_export.txt": ["@DarkKni9ht", "203.0.113.88"],
        "data/network_telemetry.csv": ["timestamp", "source_ip", "destination_ip", "flag"],
        "data/crypto_transactions.csv": ["tx_hash", "from_address", "to_address", "amount_crypto"]
    }
    
    print("--- Starting Dataset Compatibility Validation ---")
    for filepath, required_keys in required_files.items():
        if not os.path.exists(filepath):
            print(f"[FAIL] Missing required file: {filepath}")
            return False
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            for key in required_keys:
                if key not in content:
                    print(f"[FAIL] Key identifier '{key}' missing in {filepath}")
                    return False
        print(f"[PASS] {filepath} validated successfully.")
        
    print("--- All Dataset Formats Compatible & Verified ---")
    return True

if __name__ == "__main__":
    validate_corpus()