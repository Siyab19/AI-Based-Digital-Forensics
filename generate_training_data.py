import json
import random


OUTPUT_FILE = "training_features.json"

NUMBER_OF_RECORDS = 2000


# ------------------------------------------------
# NORMAL BEHAVIOUR
# ------------------------------------------------

def normal_successful_login_browser():
    """
    Successful authentication followed by normal browser activity.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(30, 300),

            "authentication_failed": 0,
            "authentication_success": 1,

            "firewall_activity": 0,
            "firewall_denied": 0,

            "browser_activity": 1,

            "same_user": 1,
            "same_source_ip": 1,
            "same_device": 1,

            "different_sources": 1
        },
        "label": 0
    }


def normal_failed_login_then_success():
    """
    A user mistypes a password and subsequently logs in successfully.
    This should NOT automatically be considered malicious.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(30, 180),

            "authentication_failed": 1,
            "authentication_success": 1,

            "firewall_activity": 0,
            "firewall_denied": 0,

            "browser_activity": 1,

            "same_user": 1,
            "same_source_ip": 1,
            "same_device": 1,

            "different_sources": 1
        },
        "label": 0
    }


def normal_allowed_network_activity():
    """
    Successful authentication followed by allowed network activity.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(30, 300),

            "authentication_failed": 0,
            "authentication_success": 1,

            "firewall_activity": 1,
            "firewall_denied": 0,

            "browser_activity": 0,

            "same_user": 0,
            "same_source_ip": 1,
            "same_device": 0,

            "different_sources": 1
        },
        "label": 0
    }


def normal_firewall_denial():
    """
    A legitimate connection is blocked by the firewall.
    Firewall denial alone should not mean malicious activity.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(30, 300),

            "authentication_failed": 0,
            "authentication_success": 1,

            "firewall_activity": 1,
            "firewall_denied": 1,

            "browser_activity": 0,

            "same_user": 0,
            "same_source_ip": 1,
            "same_device": 0,

            "different_sources": 1
        },
        "label": 0
    }


def normal_browser_activity():
    """
    Normal browser activity following successful authentication.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(60, 300),

            "authentication_failed": 0,
            "authentication_success": 1,

            "firewall_activity": 0,
            "firewall_denied": 0,

            "browser_activity": 1,

            "same_user": 1,
            "same_source_ip": 1,
            "same_device": 1,

            "different_sources": 1
        },
        "label": 0
    }


# ------------------------------------------------
# SUSPICIOUS BEHAVIOUR
# ------------------------------------------------

def suspicious_failed_login_firewall():
    """
    Failed authentication followed by denied network activity.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(20, 300),

            "authentication_failed": 1,
            "authentication_success": 0,

            "firewall_activity": 1,
            "firewall_denied": 1,

            "browser_activity": 0,

            "same_user": 0,
            "same_source_ip": 1,
            "same_device": 0,

            "different_sources": 1
        },
        "label": 1
    }


def suspicious_multiple_authentication_activity():
    """
    Authentication failure combined with additional activity.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(20, 120),

            "authentication_failed": 1,
            "authentication_success": 0,

            "firewall_activity": 1,
            "firewall_denied": random.choice([0, 1]),

            "browser_activity": random.choice([0, 1]),

            "same_user": random.choice([0, 1]),
            "same_source_ip": 1,
            "same_device": random.choice([0, 1]),

            "different_sources": 1
        },
        "label": 1
    }


def suspicious_failed_login_browser():
    """
    Failed authentication followed by browser activity.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(20, 180),

            "authentication_failed": 1,
            "authentication_success": 0,

            "firewall_activity": 0,
            "firewall_denied": 0,

            "browser_activity": 1,

            "same_user": 1,
            "same_source_ip": 1,
            "same_device": 1,

            "different_sources": 1
        },
        "label": 1
    }


def suspicious_successful_login_network():
    """
    Successful authentication followed by suspicious network activity.
    This prevents the model from assuming successful authentication is
    always normal.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(10, 120),

            "authentication_failed": 0,
            "authentication_success": 1,

            "firewall_activity": 1,
            "firewall_denied": 1,

            "browser_activity": 0,

            "same_user": 0,
            "same_source_ip": 1,
            "same_device": 0,

            "different_sources": 1
        },
        "label": 1
    }


def suspicious_successful_login_browser():
    """
    Successful authentication followed by potentially suspicious
    browser activity.
    """

    return {
        "features": {
            "time_difference_seconds": random.randint(10, 120),

            "authentication_failed": 0,
            "authentication_success": 1,

            "firewall_activity": 0,
            "firewall_denied": 0,

            "browser_activity": 1,

            "same_user": 0,
            "same_source_ip": 1,
            "same_device": 0,

            "different_sources": 1
        },
        "label": 1
    }


# ------------------------------------------------
# DATASET GENERATION
# ------------------------------------------------

def generate_training_data():

    records = []

    normal_patterns = [
        normal_successful_login_browser,
        normal_failed_login_then_success,
        normal_allowed_network_activity,
        normal_firewall_denial,
        normal_browser_activity
    ]

    suspicious_patterns = [
        suspicious_failed_login_firewall,
        suspicious_multiple_authentication_activity,
        suspicious_failed_login_browser,
        suspicious_successful_login_network,
        suspicious_successful_login_browser
    ]

    for _ in range(NUMBER_OF_RECORDS):

        # Approximately 70% normal
        # Approximately 30% suspicious

        if random.random() < 0.7:

            pattern = random.choice(
                normal_patterns
            )

        else:

            pattern = random.choice(
                suspicious_patterns
            )

        records.append(
            pattern()
        )

    return records


# ------------------------------------------------
# SAVE DATASET
# ------------------------------------------------

def save_training_data(records):

    with open(OUTPUT_FILE, "w") as file:

        json.dump(
            records,
            file,
            indent=4
        )


# ------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------

training_data = generate_training_data()

save_training_data(
    training_data
)

normal_count = sum(
    record["label"] == 0
    for record in training_data
)

suspicious_count = sum(
    record["label"] == 1
    for record in training_data
)

print(
    f"\nTraining records generated: "
    f"{len(training_data)}"
)

print(
    f"Normal records: {normal_count}"
)

print(
    f"Suspicious records: {suspicious_count}"
)

print(
    f"Training data saved to {OUTPUT_FILE}"
)