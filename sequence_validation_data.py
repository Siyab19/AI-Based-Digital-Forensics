import json
import random


NUMBER_OF_RECORDS = 500


def create_record(
    failed,
    successful,
    successful_after_failure,
    firewall,
    firewall_denials,
    browser,
    authentication,
    duration,
    label
):
    total_events = authentication + firewall + browser

    number_of_sources = sum([
        authentication > 0,
        firewall > 0,
        browser > 0
    ])

    return {
        "failed_login_count": failed,
        "successful_login_count": successful,
        "successful_login_after_failure": successful_after_failure,
        "firewall_activity_count": firewall,
        "firewall_denial_count": firewall_denials,
        "browser_activity_count": browser,
        "authentication_event_count": authentication,
        "total_event_count": total_events,
        "number_of_evidence_sources": number_of_sources,
        "sequence_duration_seconds": duration,
        "label": label
    }


def generate_normal_sequence():
    """
    Generate normal behaviour using combinations that are
    different from the training generator.
    """

    pattern = random.choice([
        "single_failure_with_browser",
        "successful_login_with_denial",
        "normal_multiple_activity",
        "browser_then_network",
        "single_authentication"
    ])

    if pattern == "single_failure_with_browser":
        return create_record(
            failed=1,
            successful=0,
            successful_after_failure=0,
            firewall=0,
            firewall_denials=0,
            browser=random.randint(1, 2),
            authentication=1,
            duration=random.randint(100, 500),
            label=0
        )

    elif pattern == "successful_login_with_denial":
        return create_record(
            failed=0,
            successful=1,
            successful_after_failure=0,
            firewall=random.randint(1, 2),
            firewall_denials=1,
            browser=0,
            authentication=1,
            duration=random.randint(100, 500),
            label=0
        )

    elif pattern == "normal_multiple_activity":
        authentication = random.randint(1, 2)
        firewall = random.randint(1, 2)
        browser = random.randint(1, 2)

        return create_record(
            failed=0,
            successful=authentication,
            successful_after_failure=0,
            firewall=firewall,
            firewall_denials=random.choice([0, 1]),
            browser=browser,
            authentication=authentication,
            duration=random.randint(100, 600),
            label=0
        )

    elif pattern == "browser_then_network":
        return create_record(
            failed=0,
            successful=1,
            successful_after_failure=0,
            firewall=random.randint(1, 3),
            firewall_denials=random.choice([0, 1]),
            browser=random.randint(1, 2),
            authentication=1,
            duration=random.randint(100, 600),
            label=0
        )

    else:
        return create_record(
            failed=0,
            successful=1,
            successful_after_failure=0,
            firewall=0,
            firewall_denials=0,
            browser=0,
            authentication=1,
            duration=random.randint(0, 300),
            label=0
        )


def generate_suspicious_sequence():
    """
    Generate suspicious behaviour using combinations that differ
    from the original training patterns.
    """

    pattern = random.choice([
        "single_failure_multiple_denials",
        "failure_success_browser",
        "authentication_network_browser",
        "multiple_failures_browser",
        "success_after_failure_with_network"
    ])

    if pattern == "single_failure_multiple_denials":
        return create_record(
            failed=1,
            successful=0,
            successful_after_failure=0,
            firewall=random.randint(2, 4),
            firewall_denials=random.randint(2, 3),
            browser=0,
            authentication=1,
            duration=random.randint(100, 700),
            label=1
        )

    elif pattern == "failure_success_browser":
        return create_record(
            failed=1,
            successful=1,
            successful_after_failure=1,
            firewall=0,
            firewall_denials=0,
            browser=random.randint(1, 2),
            authentication=2,
            duration=random.randint(100, 700),
            label=1
        )

    elif pattern == "authentication_network_browser":
        return create_record(
            failed=random.choice([0, 1]),
            successful=random.randint(1, 2),
            successful_after_failure=random.choice([0, 1]),
            firewall=random.randint(2, 4),
            firewall_denials=random.randint(1, 2),
            browser=random.randint(1, 2),
            authentication=random.randint(2, 3),
            duration=random.randint(200, 900),
            label=1
        )

    elif pattern == "multiple_failures_browser":
        return create_record(
            failed=random.randint(2, 3),
            successful=0,
            successful_after_failure=0,
            firewall=0,
            firewall_denials=0,
            browser=random.randint(1, 2),
            authentication=random.randint(2, 3),
            duration=random.randint(100, 800),
            label=1
        )

    else:
        return create_record(
            failed=1,
            successful=1,
            successful_after_failure=1,
            firewall=random.randint(1, 3),
            firewall_denials=random.choice([0, 1, 2]),
            browser=0,
            authentication=2,
            duration=random.randint(100, 900),
            label=1
        )


def generate_validation_data():
    """Generate an independent validation dataset."""

    validation_data = []

    for _ in range(NUMBER_OF_RECORDS):
        if random.random() < 0.5:
            validation_data.append(generate_normal_sequence())
        else:
            validation_data.append(generate_suspicious_sequence())

    random.shuffle(validation_data)

    return validation_data


def main():
    validation_data = generate_validation_data()

    with open("sequence_validation_features.json", "w") as file:
        json.dump(validation_data, file, indent=4)

    normal_count = sum(
        record["label"] == 0
        for record in validation_data
    )

    suspicious_count = sum(
        record["label"] == 1
        for record in validation_data
    )

    print(f"Validation records generated: {len(validation_data)}")
    print(f"Normal records: {normal_count}")
    print(f"Suspicious records: {suspicious_count}")
    print(
        "Validation data saved to sequence_validation_features.json"
    )


if __name__ == "__main__":
    main()