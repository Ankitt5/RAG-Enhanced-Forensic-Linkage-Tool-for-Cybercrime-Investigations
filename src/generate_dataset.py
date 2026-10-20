import os
import csv

def generate_evidence_corpus():
    """Programmatically generates multi-source synthetic forensic evidence 
    with consistent cross-source entity identifiers (IPs, Crypto Wallets, Handles).
    """
    os.makedirs("data", exist_ok=True)
    
    # 1. Telegram/Discord Chat Export (.txt)
    chat_logs = (
        "[2026-03-10T14:15:22Z] [CHANNEL: #syndicate-ops] @DarkKni9ht: Target environment exfiltration complete. Sent 100MB archive to 203.0.113.88 over HTTPS.\n"
        "[2026-03-10T14:18:05Z] [CHANNEL: #syndicate-ops] @Viper_Sec: Understood. C2 command staging server running at 198.51.100.45:8443. Send victim decryption keys to viper_dev@protonmail.com.\n"
        "[2026-03-10T14:22:40Z] [CHANNEL: #syndicate-ops] @DarkKni9ht: Demanding 2.5 BTC ransom payment to primary vault 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.\n"
        "[2026-03-10T14:30:12Z] [CHANNEL: #syndicate-ops] @Phantom_X: Once victim pays BTC, auto-split 40% to cashout mixer wallet bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh immediately.\n"
        "[2026-03-10T14:35:50Z] [CHANNEL: #syndicate-ops] @DarkKni9ht: Backup ETH wallet active at 0x71C7656EC7ab88b098defB751B7401B5f6d8976F. Darknet portal mirror live at c2.shadow-vault.tech.\n"
        "[2026-03-10T14:40:01Z] [CHANNEL: #syndicate-ops] @Viper_Sec: Hey team, grabbing coffee, back in 10 mins."
    )
    with open("data/chat_export.txt", "w", encoding="utf-8") as f:
        f.write(chat_logs)

    # 2. NetFlow Network Telemetry (.csv)
    network_headers = ["timestamp", "source_ip", "source_port", "destination_ip", "destination_port", "protocol", "bytes_sent", "flag"]
    network_rows = [
        ["2026-03-10T14:12:00Z", "10.0.4.112", "49152", "203.0.113.88", "443", "TCP", "104857600", "EXFILTRATION"],
        ["2026-03-10T14:16:30Z", "10.0.4.112", "49158", "198.51.100.45", "8443", "TCP", "4096", "C2_BEACON"],
        ["2026-03-10T14:20:00Z", "198.51.100.45", "8443", "10.0.4.112", "49160", "TCP", "2048", "C2_COMMAND"],
        ["2026-03-10T14:40:15Z", "198.51.100.45", "53", "8.8.8.8", "53", "UDP", "512", "DNS_QUERY"]
    ]
    with open("data/network_telemetry.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(network_headers)
        writer.writerows(network_rows)

    # 3. Cryptocurrency Transaction Ledger (.csv)
    crypto_headers = ["tx_hash", "timestamp", "from_address", "to_address", "amount_crypto", "asset", "fee"]
    crypto_rows = [
        ["8f3a2c4e1b9d0e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f", "2026-03-10T15:00:00Z", "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "2.5000", "BTC", "0.00015"],
        ["1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b", "2026-03-10T15:15:30Z", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", "1.0000", "BTC", "0.00010"],
        ["7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f", "2026-03-10T15:30:10Z", "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE", "0x71C7656EC7ab88b098defB751B7401B5f6d8976F", "15.5000", "ETH", "0.00210"]
    ]
    with open("data/crypto_transactions.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(crypto_headers)
        writer.writerows(crypto_rows)

    print("[+] Synthetic evidence generated successfully inside 'data/'.")

if __name__ == "__main__":
    generate_evidence_corpus()