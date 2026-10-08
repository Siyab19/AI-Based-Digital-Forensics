import json
import pickle


FEATURES = [
    "failed_login_count",
    "successful_login_count",
    "successful_login_after_failure",
    "firewall_activity_count",
    "firewall_denial_count",
    "browser_activity_count",
    "authentication_event_count",
    "total_event_count",
    "number_of_evidence_sources",
    "sequence_duration_seconds"
]

MODEL_FILE = "sequence_forensic_model.pkl"
FEATURE_FILE = "sequence_features.json"


def load_model(filename):
    """Load the trained sequence-level model."""
    with open(filename, "rb") as file:
        return pickle.load(file)


def load_features(filename):
    """Load real sequence features."""
    with open(filename, "r") as file:
        return json.load(file)


def prepare_features(sequence):
    """Convert one sequence into the model input format."""
    return [
        sequence[feature]
        for feature in FEATURES
    ]


def predict_sequences(model, sequences):
    """Generate predictions and probabilities for all sequences."""

    results = []

    for sequence in sequences:
        feature_vector = [
            prepare_features(sequence)
        ]

        prediction = model.predict(feature_vector)[0]
        probabilities = model.predict_proba(feature_vector)[0]

        suspicious_probability = probabilities[1]

        results.append({
            "sequence_id": sequence["sequence_id"],
            "source_ip": sequence["source_ip"],
            "prediction": (
                "suspicious"
                if prediction == 1
                else "normal"
            ),
            "suspicious_probability": round(
                float(suspicious_probability),
                4
            )
        })

    return results


def main():
    model = load_model(MODEL_FILE)
    sequences = load_features(FEATURE_FILE)

    results = predict_sequences(
        model,
        sequences
    )

    print("Sequence Predictions:")
    print()

    for result in results:
        print(
            f"Sequence {result['sequence_id']} "
            f"({result['source_ip']}): "
            f"{result['prediction']} "
            f"(suspicious probability: "
            f"{result['suspicious_probability']:.2f})"
        )


if __name__ == "__main__":
    main()