import json
from datetime import datetime


def load_sequences(filename):
    """Load sequences from a JSON file."""
    with open(filename, "r") as file:
        return json.load(file)


def parse_timestamp(timestamp):
    """Convert an ISO timestamp into a datetime object."""
    return datetime.fromisoformat(timestamp)


def extract_features(sequence):
    """
    Extract behavioural features from a single evidence sequence.
    """

    events = sequence["events"]

    failed_login_count = 0
    successful_login_count = 0
    successful_login_after_failure = 0

    firewall_activity_count = 0
    firewall_denial_count = 0
    browser_activity_count = 0
    authentication_event_count = 0

    evidence_sources = set()

    failure_seen = False

    for event in events:

        source = event.get("source")
        status = event.get("status")
        action = event.get("action")
        event_type = event.get("event_type")

        if source:
            evidence_sources.add(source)

        # Authentication activity
        if source == "authentication":
            authentication_event_count += 1

            if status == "failed":
                failed_login_count += 1
                failure_seen = True

            elif status == "success":
                successful_login_count += 1

                if failure_seen:
                    successful_login_after_failure += 1

        # Firewall activity
        elif source == "firewall":
            firewall_activity_count += 1

            if action == "deny":
                firewall_denial_count += 1

        # Browser activity
        elif source == "browser_history":
            browser_activity_count += 1

    # Sequence duration
    start_time = parse_timestamp(sequence["start_time"])
    end_time = parse_timestamp(sequence["end_time"])

    sequence_duration_seconds = (
        end_time - start_time
    ).total_seconds()

    return {
        "sequence_id": sequence["sequence_id"],
        "source_ip": sequence["source_ip"],
        "failed_login_count": failed_login_count,
        "successful_login_count": successful_login_count,
        "successful_login_after_failure": successful_login_after_failure,
        "firewall_activity_count": firewall_activity_count,
        "firewall_denial_count": firewall_denial_count,
        "browser_activity_count": browser_activity_count,
        "authentication_event_count": authentication_event_count,
        "total_event_count": len(events),
        "number_of_evidence_sources": len(evidence_sources),
        "sequence_duration_seconds": sequence_duration_seconds
    }


def extract_sequence_features(sequences):
    """Extract features for all sequences."""
    return [
        extract_features(sequence)
        for sequence in sequences
    ]


def save_features(features, filename):
    """Save extracted features to JSON."""
    with open(filename, "w") as file:
        json.dump(features, file, indent=4)


def main():
    input_file = "sequences.json"
    output_file = "sequence_features.json"

    sequences = load_sequences(input_file)

    features = extract_sequence_features(sequences)

    save_features(features, output_file)

    print(f"Sequences processed: {len(sequences)}")
    print(f"Feature records generated: {len(features)}")
    print(f"Features saved to {output_file}")


if __name__ == "__main__":
    main()