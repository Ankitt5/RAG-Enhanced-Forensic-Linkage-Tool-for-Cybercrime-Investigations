from pathlib import Path
from scapy.all import Ether, IP, TCP, UDP, ICMP, DNS, DNSQR, wrpcap

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "test_traffic.pcap"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

packets = [
    # Synthetic TCP packet
    Ether() / IP(src="192.0.2.10", dst="198.51.100.20") /
    TCP(sport=49152, dport=443, flags="S"),

    # Synthetic UDP packet
    Ether() / IP(src="192.0.2.11", dst="198.51.100.53") /
    UDP(sport=53000, dport=53),

    # Synthetic ICMP packet
    Ether() / IP(src="192.0.2.12", dst="198.51.100.30") /
    ICMP(),

    # Synthetic DNS query
    Ether() / IP(src="192.0.2.13", dst="198.51.100.53") /
    UDP(sport=53001, dport=53) /
    DNS(rd=1, qd=DNSQR(qname="example.test"))
]

wrpcap(str(OUTPUT_FILE), packets)

print(f"[PASS] Generated {len(packets)} synthetic packets.")
print(f"[PASS] PCAP saved to: {OUTPUT_FILE}")