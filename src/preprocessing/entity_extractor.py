
import json

from src.config import (
    NORMALIZED_EVIDENCE_FILE,
    EXTRACTED_ENTITIES_FILE
)


def extract_entities(record):
    entities = {
        "users": [],
        "ip_addresses": {
            "source": [],
            "destination": []
        },
        "devices": [],
        "resources": []
    }

    # Extract user
    if record.get("user") is not None:
        entities["users"].append(record["user"])

    # Extract source IP
    if record.get("source_ip") is not None:
        entities["ip_addresses"]["source"].append(
            record["source_ip"]
        )

    # Extract destination IP
    if record.get("destination_ip") is not None:
        entities["ip_addresses"]["destination"].append(
            record["destination_ip"]
        )

    # Extract device
    if record.get("device") is not None:
        entities["devices"].append(record["device"])

    # Extract resource
    if record.get("resource") is not None:
        entities["resources"].append(record["resource"])

    return entities


def main():
    # Read normalized evidence
    with open(NORMALIZED_EVIDENCE_FILE, "r") as file:
        evidence = json.load(file)

    # Extract entities from every evidence record
    extracted_evidence = []

    for record in evidence:
        entities = extract_entities(record)

        extracted_record = {
            "timestamp": record["timestamp"],
            "source": record["source"],
            "event_type": record["event_type"],
            "action": record["action"],
            "status": record["status"],
            "entities": entities
        }

        extracted_evidence.append(extracted_record)

    # Save extracted entities
    EXTRACTED_ENTITIES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(EXTRACTED_ENTITIES_FILE, "w") as file:
        json.dump(extracted_evidence, file, indent=4)

    print(
        f"Successfully extracted entities from {len(extracted_evidence)} evidence records."
    )
    print(f"Extracted entities saved to {EXTRACTED_ENTITIES_FILE}")


if __name__ == "__main__":
    main()
