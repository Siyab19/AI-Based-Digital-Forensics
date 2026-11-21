
import json
from datetime import datetime

from src.config import (
    EVIDENCE_FILE,
    NORMALIZED_EVIDENCE_FILE
)


def normalize_timestamp(timestamp):
    try:
        date_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return date_time.isoformat()
    except ValueError:
        return timestamp


def normalize_evidence(record):
    normalized = record.copy()

    # Normalize timestamp
    normalized["timestamp"] = normalize_timestamp(
        normalized["timestamp"]
    )

    # Normalize text fields
    text_fields = [
        "source",
        "event_type",
        "action",
        "status"
    ]

    for field in text_fields:
        if field in normalized and normalized[field] is not None:
            normalized[field] = normalized[field].lower()

    # Normalize protocol inside details
    if "protocol" in normalized["details"]:
        normalized["details"]["protocol"] = (
            normalized["details"]["protocol"].lower()
        )

    return normalized


def main():
    # Read evidence
    with open(EVIDENCE_FILE, "r") as file:
        evidence = json.load(file)

    # Normalize every evidence record
    normalized_evidence = []

    for record in evidence:
        normalized_record = normalize_evidence(record)
        normalized_evidence.append(normalized_record)

    # Save normalized evidence
    NORMALIZED_EVIDENCE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(NORMALIZED_EVIDENCE_FILE, "w") as file:
        json.dump(normalized_evidence, file, indent=4)

    print(
        f"Successfully normalized {len(normalized_evidence)} evidence records."
    )
    print(f"Normalized evidence saved to {NORMALIZED_EVIDENCE_FILE}")


if __name__ == "__main__":
    main()
