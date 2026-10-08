import json


def parse_firewall_log(line):
    parts = line.strip().split()

    if len(parts) != 8:
        return None

    try:
        timestamp = parts[0] + " " + parts[1]
        action = parts[2]
        source_ip = parts[3]
        destination_ip = parts[4]
        source_port = int(parts[5])
        destination_port = int(parts[6])
        protocol = parts[7]

        return {
            "timestamp": timestamp,
            "source": "firewall",
            "event_type": "network_connection",

            "user": None,
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "device": None,

            "action": action,
            "status": None,
            "resource": None,

            "details": {
                "source_port": source_port,
                "destination_port": destination_port,
                "protocol": protocol
            }
        }

    except ValueError:
        return None

def parse_authentication_log(line):
    parts = line.strip().split()

    if len(parts) != 7:
        return None

    try:
        timestamp = parts[0] + " " + parts[1]
        action = parts[2]
        user = parts[3]
        source_ip = parts[4]
        device = parts[5]
        status = parts[6]

        return {
            "timestamp": timestamp,
            "source": "authentication",
            "event_type": "login",

            "user": user,
            "source_ip": source_ip,
            "destination_ip": None,
            "device": device,

            "action": action,
            "status": status,
            "resource": None,

            "details": {}
        }

    except ValueError:
        return None

def parse_browser_history_log(line):
    parts = line.strip().split()

    if len(parts) != 6:
        return None

    try:
        timestamp = parts[0] + " " + parts[1]
        user = parts[2]
        source_ip = parts[3]
        device = parts[4]
        url = parts[5]

        return {
            "timestamp": timestamp,
            "source": "browser_history",
            "event_type": "web_access",

            "user": user,
            "source_ip": source_ip,
            "destination_ip": None,
            "device": device,

            "action": "access",
            "status": None,
            "resource": url,

            "details": {}
        }

    except ValueError:
        return None


def read_log_file(file_path, parser):
    evidence = []

    with open(file_path, "r") as file:
        for line in file:
            if not line.strip():
                continue

            record = parser(line)

            if record is not None:
                evidence.append(record)
            else:
                print("Warning: Could not parse log entry:", line.strip())

    return evidence


def save_evidence(evidence, output_file):
    with open(output_file, "w") as file:
        json.dump(evidence, file, indent=4)


# Main program
firewall_evidence = read_log_file(
    "firewall.log",
    parse_firewall_log
)

authentication_evidence = read_log_file(
    "authentication.log",
    parse_authentication_log
)

browser_evidence = read_log_file(
    "browser_history.log",
    parse_browser_history_log
)

evidence = (
    firewall_evidence
    + authentication_evidence
    + browser_evidence
)

save_evidence(evidence, "evidence.json")

print(f"\nSuccessfully processed {len(evidence)} evidence records.")
print("Structured evidence saved to evidence.json")