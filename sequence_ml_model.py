import json
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


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

TRAINING_FILE = "sequence_training_features.json"
MODEL_FILE = "sequence_forensic_model.pkl"


def load_training_data(filename):
    """Load sequence-level training data."""
    with open(filename, "r") as file:
        return json.load(file)


def prepare_data(training_data):
    """Separate features and labels."""
    X = [
        [record[feature] for feature in FEATURES]
        for record in training_data
    ]

    y = [
        record["label"]
        for record in training_data
    ]

    return X, y


def train_model(X_train, y_train):
    """Train the Random Forest classifier."""
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model


def save_model(model, filename):
    """Save the trained model."""
    with open(filename, "wb") as file:
        pickle.dump(model, file)


def main():
    training_data = load_training_data(TRAINING_FILE)

    X, y = prepare_data(training_data)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = train_model(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"Training records: {len(X_train)}")
    print(f"Testing records: {len(X_test)}")
    print()
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    print()
    print("Classification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["Normal", "Suspicious"]
        )
    )

    print("Feature Importance:")

    for feature, importance in zip(
        FEATURES,
        model.feature_importances_
    ):
        print(f"{feature}: {importance:.4f}")

    save_model(model, MODEL_FILE)

    print()
    print(f"Model saved to {MODEL_FILE}")


if __name__ == "__main__":
    main()