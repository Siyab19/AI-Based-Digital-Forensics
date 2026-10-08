import json
import random


NUMBER_OF_RECORDS = 2000


def create_sequence_features(
    failed_logins,
    successful_logins,
    successful_after_failure,
    firewall_activity,
    firewall_denials,
    browser_activity,
    authentication_events,
    duration
):
    total_events = (
        authentication_events
        + firewall_activity
        + browser_activity
    )

    evidence_sources = sum([
        authentication_events > 0,
        firewall_activity > 0,
        browser_activity > 0
    ])

    return {
        "failed_login_count": failed_logins,
        "successful_login_count": successful_logins,
        "successful_login_after_failure": successful_after_failure,
        "firewall_activity_count": firewall_activity,
        "firewall_denial_count": firewall_denials,
        "browser_activity_count": browser_activity,
        "authentication_event_count": authentication_events,
        "total_event_count": total_events,
        "number_of_evidence_sources": evidence_sources,
        "sequence_duration_seconds": duration
    }


def generate_base_behaviour():
    """
    Generate a random combination of authentication,
    firewall and browser behaviour.
    """

    failed_logins = random.choices(
        [0, 1, 2, 3],
        weights=[45, 35, 15, 5]
    )[0]

    successful_logins = random.choices(
        [0, 1, 2],
        weights=[20, 60, 20]
    )[0]

    firewall_activity = random.randint(0, 3)

    firewall_denials = random.randint(
        0,
        firewall_activity
    )

    browser_activity = random.randint(0, 3)

    authentication_events = (
        failed_logins + successful_logins
    )

    successful_after_failure = 0

    if failed_logins > 0 and successful_logins > 0:
        successful_after_failure = 1

    duration = random.randint(30, 900)

    return create_sequence_features(
        failed_logins,
        successful_logins,
        successful_after_failure,
        firewall_activity,
        firewall_denials,
        browser_activity,
        authentication_events,
        duration
    )


def calculate_suspicion_score(features):
    """
    Calculate a behavioural suspicion score.

    The score is intentionally based on combinations
    of behaviours rather than a single feature.
    """

    score = 0

    failed = features["failed_login_count"]
    successful_after_failure = features[
        "successful_login_after_failure"
    ]
    firewall_denials = features[
        "firewall_denial_count"
    ]
    browser = features["browser_activity_count"]
    firewall = features["firewall_activity_count"]
    sources = features["number_of_evidence_sources"]

    # Repeated authentication failures
    if failed >= 2:
        score += 2

    # Successful authentication after failures
    if successful_after_failure:
        score += 2

    # Multiple denied network connections
    if firewall_denials >= 2:
        score += 2

    # Authentication followed by network activity
    if features["authentication_event_count"] > 0 and firewall > 0:
        score += 1

    # Authentication followed by browser activity
    if features["authentication_event_count"] > 0 and browser > 0:
        score += 1

    # Activity across multiple evidence sources
    if sources >= 3:
        score += 1

    return score


def generate_record():
    """Generate one sequence and assign its behavioural label."""

    features = generate_base_behaviour()

    suspicion_score = calculate_suspicion_score(features)

    # Add some ambiguity around the classification boundary.
    if suspicion_score >= 5:
        label = 1
    elif suspicion_score <= 2:
        label = 0
    else:
        # Borderline sequences can belong to either class.
        label = random.choice([0, 1])

    features["label"] = label

    return features


def generate_training_data():
    """Generate the complete synthetic training dataset."""

    training_data = [
        generate_record()
        for _ in range(NUMBER_OF_RECORDS)
    ]

    random.shuffle(training_data)

    return training_data


def main():
    training_data = generate_training_data()

    with open(
        "sequence_training_features.json",
        "w"
    ) as file:
        json.dump(
            training_data,
            file,
            indent=4
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
        f"Training records generated: "
        f"{len(training_data)}"
    )

    print(
        f"Normal records: {normal_count}"
    )

    print(
        f"Suspicious records: {suspicious_count}"
    )

    print(
        "Training data saved to "
        "sequence_training_features.json"
    )


if __name__ == "__main__":
    main()