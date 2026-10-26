import csv
import ipaddress
from pathlib import Path


REQUIRED_COLUMNS = {
    "timestamp",
    "source_ip",
    "source_port",
    "destination_ip",
    "destination_port",
    "protocol",
    "bytes_sent",
    "flag",
}


def parse_network_telemetry(file_path):
    """Parse network telemetry CSV records into standardized evidence."""

    file_path = Path(file_path)
    evidence_records = []

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or missing its header.")

        reader.fieldnames = [
            name.strip() for name in reader.fieldnames
        ]

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

        for record_number, row in enumerate(reader, start=1):
            csv_row_number = record_number + 1

            try:
                source_ip = row["source_ip"].strip()
                destination_ip = row["destination_ip"].strip()
                timestamp = row["timestamp"].strip()
                protocol = row["protocol"].strip()
                flag = row["flag"].strip()

                source_port = int(row["source_port"])
                destination_port = int(row["destination_port"])
                bytes_sent = int(row["bytes_sent"])

                ipaddress.ip_address(source_ip)
                ipaddress.ip_address(destination_ip)

                if not 0 <= source_port <= 65535:
                    raise ValueError("Invalid source port.")

                if not 0 <= destination_port <= 65535:
                    raise ValueError("Invalid destination port.")

                if bytes_sent < 0:
                    raise ValueError("Bytes sent cannot be negative.")

                if not timestamp:
                    raise ValueError("Timestamp is missing.")

                if not protocol:
                    raise ValueError("Protocol is missing.")

                if not flag:
                    raise ValueError("Flag is missing.")

                evidence_records.append({
                    "evidence_id": f"EV-NET-{record_number:04d}",
                    "source_type": "network",
                    "source_format": "netflow_telemetry",
                    "source_file": file_path.name,
                    "source_row": csv_row_number,
                    "timestamp": timestamp,
                    "raw_content": (
                        f"{source_ip}:{source_port} -> "
                        f"{destination_ip}:{destination_port} "
                        f"({protocol})"
                    ),
                    "metadata": {
                        "src_ip": source_ip,
                        "dst_ip": destination_ip,
                        "src_port": source_port,
                        "dst_port": destination_port,
                        "protocol": protocol,
                        "bytes_transferred": bytes_sent,
                        "flag": flag,
                    },
                })

            except (ValueError, AttributeError, TypeError) as error:
                raise ValueError(
                    f"Invalid network record at CSV row "
                    f"{csv_row_number}: {error}"
                ) from error

    return evidence_records