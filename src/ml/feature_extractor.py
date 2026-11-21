import json


def load_correlations(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def extract_features(correlation):

    earlier = correlation["earlier_event"]
    later = correlation["later_event"]

    features = {}

    # ------------------------------------------------
    # Temporal feature
    # ------------------------------------------------

    features["time_difference_seconds"] = (
        correlation["time_difference_seconds"]
    )

    # ------------------------------------------------
    # Authentication features
    # ------------------------------------------------

    features["authentication_failed"] = int(
        earlier["source"] == "authentication"
        and earlier["status"] == "failed"
    )

    features["authentication_success"] = int(
        earlier["source"] == "authentication"
        and earlier["status"] == "success"
    )

    # ------------------------------------------------
    # Firewall features
    # ------------------------------------------------

    features["firewall_activity"] = int(
        later["source"] == "firewall"
    )

    features["firewall_denied"] = int(
        later["source"] == "firewall"
        and later["action"] == "deny"
    )

    # ------------------------------------------------
    # Browser features
    # ------------------------------------------------

    features["browser_activity"] = int(
        later["source"] == "browser_history"
    )

    # ------------------------------------------------
    # Entity relationship features
    # ------------------------------------------------

    features["same_user"] = int(
        earlier["user"] is not None
        and later["user"] is not None
        and earlier["user"] == later["user"]
    )

    features["same_source_ip"] = int(
        earlier["source_ip"] is not None
        and later["source_ip"] is not None
        and earlier["source_ip"] == later["source_ip"]
    )

    features["same_device"] = int(
        earlier["device"] is not None
        and later["device"] is not None
        and earlier["device"] == later["device"]
    )

    # ------------------------------------------------
    # Evidence source feature
    # ------------------------------------------------

    features["different_sources"] = int(
        earlier["source"] != later["source"]
    )

    return features


def extract_all_features(correlations):

    feature_records = []

    for correlation in correlations:

        features = extract_features(
            correlation
        )

        feature_records.append({
            "rule": correlation["rule"],
            "features": features
        })

    return feature_records


def save_features(features, file_path):

    with open(file_path, "w") as file:
        json.dump(
            features,
            file,
            indent=4
        )


# ------------------------------------------------
# Main program
# ------------------------------------------------

correlations = load_correlations(
    "correlations.json"
)

features = extract_all_features(
    correlations
)

save_features(
    features,
    "features.json"
)

print(
    f"\nFeatures extracted for {len(features)} correlations."
)

print(
    "Features saved to features.json"
)