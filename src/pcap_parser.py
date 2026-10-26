import json
from pathlib import Path
from datetime import datetime, timezone

from scapy.all import rdpcap, IP, IPv6, TCP, UDP, ICMP, DNS

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "test_traffic.pcap"
OUTPUT_FILE = BASE_DIR / "data" / "pcap_evidence.json"


def parse_pcap(file_path):
    # Accept either a string or a Path object.
    file_path = Path(file_path)

    packets = rdpcap(str(file_path))
    evidence_records = []

    for index, packet in enumerate(packets, start=1):
        timestamp = datetime.fromtimestamp(
            float(packet.time), tz=timezone.utc
        ).isoformat()

        src_ip = None
        dst_ip = None
        protocol = "OTHER"
        src_port = None
        dst_port = None

        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
        elif IPv6 in packet:
            src_ip = packet[IPv6].src
            dst_ip = packet[IPv6].dst

        if TCP in packet:
            protocol = "TCP"
            src_port = int(packet[TCP].sport)
            dst_port = int(packet[TCP].dport)
        elif UDP in packet:
            protocol = "UDP"
            src_port = int(packet[UDP].sport)
            dst_port = int(packet[UDP].dport)
        elif ICMP in packet:
            protocol = "ICMP"

        if DNS in packet:
            protocol = "DNS"

        evidence_records.append({
            "evidence_id": f"EV-PCAP-{index:04d}",
            "source_type": "network",
            "source_format": "pcap",
            "source_file": file_path.name,
            "source_row": index,
            "timestamp": timestamp,
            "raw_content": packet.summary(),
            "metadata": {
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "protocol": protocol,
                "packet_length": len(packet)
            }
        })

    return evidence_records


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"PCAP file not found: {INPUT_FILE}"
        )

    records = parse_pcap(INPUT_FILE)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)

    print(f"[PASS] PCAP packets processed: {len(records)}")
    print(f"[PASS] Evidence saved to: {OUTPUT_FILE}")

    for record in records:
        metadata = record["metadata"]
        print(
            f"[PACKET] {record['evidence_id']} | "
            f"{metadata['src_ip']} -> {metadata['dst_ip']} | "
            f"{metadata['protocol']}"
        )


if __name__ == "__main__":
    main()