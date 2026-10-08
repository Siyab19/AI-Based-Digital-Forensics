import json
import pickle


MODEL_FILE = "sequence_forensic_model.pkl"
CORRELATIONS_FILE = "correlations.json"
SEQUENCE_FEATURES_FILE = "sequence_features.json"
OUTPUT_FILE = "hybrid_analysis.json"

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


def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, "r") as file:
        return json.load(file)


def load_model(filename):
    """Load the trained sequence-level ML model."""
    with open(filename, "rb") as file:
        return pickle.load(file)


def build_feature_vector(sequence):
    """Convert sequence features into model input format."""
    return [
        sequence[feature]
        for feature in FEATURES
    ]


def get_ml_prediction(model, sequence):
    """Generate the ML prediction and suspicious-class probability."""

    feature_vector = [
        build_feature_vector(sequence)
    ]

    prediction = model.predict(feature_vector)[0]
    probabilities = model.predict_proba(feature_vector)[0]

    return {
        "prediction": (
            "suspicious"
            if prediction == 1
            else "normal"
        ),
        "suspicious_probability": round(
            float(probabilities[1]),
            4
        )
    }


def find_sequence_correlations(sequence, correlations):
    source_ip = sequence.get("source_ip")
    return [
        correlation
        for correlation in correlations
        if source_ip in (
            correlation.get("earlier_event", {}).get("source_ip"),
            correlation.get("later_event", {}).get("source_ip")
        )
    ]


def build_rule_findings(correlations):
    """Convert deterministic correlations into explainable findings."""

    findings = []

    for correlation in correlations:
        reason = correlation.get("reason")

        if reason:
            findings.append(reason)

    return findings


def determine_assessment(rule_findings, ml_prediction):
    """
    Produce a cautious investigation assessment.

    This is NOT an attack verdict.
    """

    if rule_findings and ml_prediction["prediction"] == "suspicious":
        return "requires_investigation"

    if rule_findings:
        return "rule_based_finding"

    if ml_prediction["prediction"] == "suspicious":
        return "ml_based_finding"

    return "no_significant_finding"


def analyze_sequences(sequences, correlations, model):
    """Build hybrid analysis for every sequence."""

    results = []

    for sequence in sequences:

        sequence_correlations = find_sequence_correlations(
            sequence,
            correlations
        )

        rule_findings = build_rule_findings(
            sequence_correlations
        )

        ml_prediction = get_ml_prediction(
            model,
            sequence
        )

        assessment = determine_assessment(
            rule_findings,
            ml_prediction
        )

        results.append({
            "sequence_id": sequence["sequence_id"],
            "source_ip": sequence["source_ip"],
            "rule_findings": rule_findings,
            "ml_prediction": ml_prediction["prediction"],
            "ml_suspicious_probability": (
                ml_prediction["suspicious_probability"]
            ),
            "assessment": assessment
        })

    return results


def save_results(results, filename):
    """Save hybrid analysis results."""
    with open(filename, "w") as file:
        json.dump(results, file, indent=4)


def main():
    sequences = load_json(SEQUENCE_FEATURES_FILE)
    correlations = load_json(CORRELATIONS_FILE)
    model = load_model(MODEL_FILE)

    results = analyze_sequences(
        sequences,
        correlations,
        model
    )

    save_results(results, OUTPUT_FILE)

    print(
        f"Sequences analyzed: {len(results)}"
    )

    print(
        f"Hybrid analysis saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()