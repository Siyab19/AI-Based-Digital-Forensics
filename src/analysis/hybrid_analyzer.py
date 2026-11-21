
import json
import pickle

from src.config import (
    SEQUENCE_MODEL_FILE,
    CORRELATIONS_FILE,
    SEQUENCE_FEATURES_FILE,
    HYBRID_ANALYSIS_FILE
)


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
    with open(filename, "r", encoding="utf-8") as file:
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
    """Generate the ML prediction and suspicious-class score."""

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
    """Find all correlations associated with a sequence's source IP."""

    source_ip = sequence.get("source_ip")

    if not source_ip:
        return []

    return [
        correlation
        for correlation in correlations
        if source_ip in (
            correlation.get("earlier_event", {}).get("source_ip"),
            correlation.get("later_event", {}).get("source_ip")
        )
    ]


def build_rule_findings(correlations):
    """Build unique human-readable explanations without losing evidence."""

    findings = []
    seen_findings = set()

    for correlation in correlations:
        reason = correlation.get("reason")

        if reason and reason not in seen_findings:
            findings.append(reason)
            seen_findings.add(reason)

    return findings


def build_correlated_events(correlations):
    """
    Preserve every correlated event relationship.

    Each record retains its original earlier and later event details.
    """

    correlated_events = []

    for correlation in correlations:
        correlated_events.append({
            "rule": correlation.get("rule"),
            "time_difference_seconds": (
                correlation.get("time_difference_seconds")
            ),
            "earlier_event": correlation.get("earlier_event", {}),
            "later_event": correlation.get("later_event", {}),
            "reason": correlation.get("reason")
        })

    return correlated_events


def determine_assessment(rule_findings, ml_prediction):
    """
    Produce a cautious investigation assessment.

    These assessments are investigative indicators,
    not definitive attack verdicts.
    """

    if (
        rule_findings
        and ml_prediction["prediction"] == "suspicious"
    ):
        return "requires_investigation"

    if rule_findings:
        return "correlated_activity_observed"

    if ml_prediction["prediction"] == "suspicious":
        return "ml_based_finding"

    return "no_significant_finding"


def analyze_sequences(sequences, correlations, model):
    """Build hybrid analysis for every evidence sequence."""

    results = []

    for sequence in sequences:

        sequence_correlations = find_sequence_correlations(
            sequence,
            correlations
        )

        rule_findings = build_rule_findings(
            sequence_correlations
        )

        correlated_events = build_correlated_events(
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
            "correlated_events": correlated_events,
            "ml_prediction": ml_prediction["prediction"],
            "ml_suspicious_probability": (
                ml_prediction["suspicious_probability"]
            ),
            "assessment": assessment
        })

    return results


def save_results(results, filename):
    """Save hybrid analysis results."""
    filename.parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)


def main():
    sequences = load_json(SEQUENCE_FEATURES_FILE)
    correlations = load_json(CORRELATIONS_FILE)
    model = load_model(SEQUENCE_MODEL_FILE)

    results = analyze_sequences(
        sequences,
        correlations,
        model
    )

    save_results(results, HYBRID_ANALYSIS_FILE)

    print(f"Sequences analyzed: {len(results)}")
    print(f"Hybrid analysis saved to {HYBRID_ANALYSIS_FILE}")


if __name__ == "__main__":
    main()
