import json
from datetime import datetime

SEQUENCE_WINDOW_MINUTES = 5


def load_evidence(filename):
    """Load normalized evidence from a JSON file."""
    with open(filename, "r") as file:
        return json.load(file)


def parse_timestamp(timestamp):
    """Convert ISO timestamp string into a datetime object."""
    return datetime.fromisoformat(timestamp)


def get_sequence_key(event):
    """
    Return the key used to group related events.

    For now, source IP is the primary sequence identifier.
    """
    return event.get("source_ip")


def build_sequences(evidence):
    """
    Build chronological evidence sequences.

    Events belonging to the same source IP are grouped together
    when consecutive events occur within the configured time window.
    """

    # Sort all evidence chronologically
    sorted_evidence = sorted(
        evidence,
        key=lambda event: parse_timestamp(event["timestamp"])
    )

    sequences = []
    current_sequences = {}

    window_seconds = SEQUENCE_WINDOW_MINUTES * 60

    for event in sorted_evidence:
        sequence_key = get_sequence_key(event)

        # Ignore events without a source IP for now
        if sequence_key is None:
            continue

        event_time = parse_timestamp(event["timestamp"])

        if sequence_key not in current_sequences:
            sequence = {
                "sequence_id": len(sequences) + 1,
                "source_ip": sequence_key,
                "start_time": event["timestamp"],
                "end_time": event["timestamp"],
                "events": [event]
            }

            sequences.append(sequence)
            current_sequences[sequence_key] = sequence

        else:
            sequence = current_sequences[sequence_key]

            last_event = sequence["events"][-1]
            last_event_time = parse_timestamp(last_event["timestamp"])

            time_difference = (
                event_time - last_event_time
            ).total_seconds()

            if time_difference <= window_seconds:
                sequence["events"].append(event)
                sequence["end_time"] = event["timestamp"]

            else:
                new_sequence = {
                    "sequence_id": len(sequences) + 1,
                    "source_ip": sequence_key,
                    "start_time": event["timestamp"],
                    "end_time": event["timestamp"],
                    "events": [event]
                }

                sequences.append(new_sequence)
                current_sequences[sequence_key] = new_sequence

    return sequences


def save_sequences(sequences, filename):
    """Save generated sequences to JSON."""
    with open(filename, "w") as file:
        json.dump(sequences, file, indent=4)


def main():
    input_file = "normalized_evidence.json"
    output_file = "sequences.json"

    evidence = load_evidence(input_file)

    sequences = build_sequences(evidence)

    save_sequences(sequences, output_file)

    print(f"Evidence events: {len(evidence)}")
    print(f"Sequences generated: {len(sequences)}")
    print(f"Sequences saved to {output_file}")


if __name__ == "__main__":
    main()