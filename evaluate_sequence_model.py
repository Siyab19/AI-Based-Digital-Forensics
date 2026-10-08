import json
import pickle

from sklearn.metrics import accuracy_score, classification_report


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
VALIDATION_FILE = "sequence_validation_features.json"


def load_validation_data(filename):
    with open(filename, "r") as file:
        return json.load(file)


def load_model(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


def prepare_data(data):
    X = [
        [record[feature] for feature in FEATURES]
        for record in data
    ]

    y = [
        record["label"]
        for record in data
    ]

    return X, y


def main():
    validation_data = load_validation_data(VALIDATION_FILE)
    model = load_model(MODEL_FILE)

    X_validation, y_validation = prepare_data(validation_data)

    predictions = model.predict(X_validation)

    accuracy = accuracy_score(
        y_validation,
        predictions
    )

    print(f"Validation records: {len(X_validation)}")
    print()
    print(
        f"Independent validation accuracy: "
        f"{accuracy * 100:.2f}%"
    )
    print()
    print("Classification Report:")

    print(
        classification_report(
            y_validation,
            predictions,
            target_names=["Normal", "Suspicious"]
        )
    )


if __name__ == "__main__":
    main()