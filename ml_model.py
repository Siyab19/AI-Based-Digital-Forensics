import json
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


INPUT_FILE = "training_features.json"
MODEL_FILE = "forensic_model.pkl"


# ------------------------------------------------
# Load training data
# ------------------------------------------------

def load_training_data(file_path):

    with open(file_path, "r") as file:
        data = json.load(file)

    return data


# ------------------------------------------------
# Prepare features and labels
# ------------------------------------------------

def prepare_data(data):

    X = []
    y = []

    for record in data:

        X.append([
            record["features"]["time_difference_seconds"],
            record["features"]["authentication_failed"],
            record["features"]["authentication_success"],
            record["features"]["firewall_activity"],
            record["features"]["firewall_denied"],
            record["features"]["browser_activity"],
            record["features"]["same_user"],
            record["features"]["same_source_ip"],
            record["features"]["same_device"],
            record["features"]["different_sources"]
        ])

        y.append(record["label"])

    return X, y


# ------------------------------------------------
# Train Random Forest
# ------------------------------------------------

def train_model(X_train, y_train):

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    return model


# ------------------------------------------------
# Save trained model
# ------------------------------------------------

def save_model(model, file_path):

    with open(file_path, "wb") as file:
        pickle.dump(
            model,
            file
        )


# ------------------------------------------------
# Main program
# ------------------------------------------------

data = load_training_data(
    INPUT_FILE
)

X, y = prepare_data(
    data
)

# Split dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(
    f"\nTraining records: {len(X_train)}"
)

print(
    f"Testing records: {len(X_test)}"
)

# Train model
model = train_model(
    X_train,
    y_train
)

# Test model
predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"\nModel accuracy: {accuracy:.2%}"
)

print(
    "\nClassification Report:"
)

print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "Normal",
            "Suspicious"
        ]
    )
)

# Display feature importance
feature_names = [
    "time_difference_seconds",
    "authentication_failed",
    "authentication_success",
    "firewall_activity",
    "firewall_denied",
    "browser_activity",
    "same_user",
    "same_source_ip",
    "same_device",
    "different_sources"
]

print(
    "\nFeature Importance:"
)

for name, importance in zip(
    feature_names,
    model.feature_importances_
):

    print(
        f"{name}: {importance:.4f}"
    )

# Save model
save_model(
    model,
    MODEL_FILE
)

print(
    f"\nTrained model saved to {MODEL_FILE}"
)