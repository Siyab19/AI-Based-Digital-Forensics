import json
from datetime import datetime


CORRELATION_WINDOW_MINUTES = 5


def load_evidence(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def save_correlations(correlations, file_path):
    with open(file_path, "w") as file:
        json.dump(correlations, file, indent=4)


def create_event_summary(event):
    entities = event["entities"]

    source_ips = entities["ip_addresses"]["source"]
    destination_ips = entities["ip_addresses"]["destination"]

    return {
        "timestamp": event["timestamp"],
        "source": event["source"],
        "event_type": event["event_type"],
        "action": event["action"],
        "status": event["status"],

        "user": (
            entities["users"][0]
            if entities["users"]
            else None
        ),

        "source_ip": (
            source_ips[0]
            if source_ips
            else None
        ),

        "destination_ip": (
            destination_ips[0]
            if destination_ips
            else None
        ),

        "device": (
            entities["devices"][0]
            if entities["devices"]
            else None
        ),

        "resource": (
            entities["resources"][0]
            if entities["resources"]
            else None
        )
    }


def get_time_difference(event1, event2):
    time1 = datetime.fromisoformat(event1["timestamp"])
    time2 = datetime.fromisoformat(event2["timestamp"])

    return abs((time2 - time1).total_seconds())


def correlate_events(events):
    correlations = []

    for i in range(len(events)):
        for j in range(i + 1, len(events)):

            event1 = events[i]
            event2 = events[j]

            # Ignore events from the same source
            if event1["source"] == event2["source"]:
                continue

            # Calculate time difference
            time_difference = get_time_difference(
                event1,
                event2
            )

            # Ignore events outside the correlation window
            if time_difference > CORRELATION_WINDOW_MINUTES * 60:
                continue

            # Put events in chronological order
            timestamp1 = datetime.fromisoformat(
                event1["timestamp"]
            )

            timestamp2 = datetime.fromisoformat(
                event2["timestamp"]
            )

            if timestamp1 <= timestamp2:
                earlier = event1
                later = event2
            else:
                earlier = event2
                later = event1

            earlier_summary = create_event_summary(earlier)
            later_summary = create_event_summary(later)

            # ------------------------------------------------
            # RULE 1:
            # Failed login followed by network activity
            # ------------------------------------------------

            earlier_is_failed_login = (
                earlier["source"] == "authentication"
                and earlier["event_type"] == "login"
                and earlier["status"] == "failed"
            )

            later_is_firewall = (
                later["source"] == "firewall"
            )

            earlier_ips = (
                earlier["entities"]["ip_addresses"]["source"]
            )

            later_ips = (
                later["entities"]["ip_addresses"]["source"]
            )

            shared_source_ip = (
                len(set(earlier_ips) & set(later_ips)) > 0
            )

            if (
                earlier_is_failed_login
                and later_is_firewall
                and shared_source_ip
            ):
                correlations.append({
                    "rule": "failed_login_followed_by_network_activity",

                    "time_difference_seconds": int(
                        time_difference
                    ),

                    "earlier_event": earlier_summary,

                    "later_event": later_summary,

                    "reason": (
                        "A failed authentication was followed by "
                        "network activity from the same source IP "
                        "within 5 minutes."
                    )
                })

                continue

            # ------------------------------------------------
            # RULE 2:
            # Authentication followed by browser activity
            # ------------------------------------------------

            earlier_is_authentication = (
                earlier["source"] == "authentication"
                and earlier["event_type"] == "login"
            )

            later_is_browser = (
                later["source"] == "browser_history"
                and later["event_type"] == "web_access"
            )

            earlier_users = (
                earlier["entities"]["users"]
            )

            later_users = (
                later["entities"]["users"]
            )

            earlier_devices = (
                earlier["entities"]["devices"]
            )

            later_devices = (
                later["entities"]["devices"]
            )

            shared_user = (
                len(set(earlier_users) & set(later_users)) > 0
            )

            shared_device = (
                len(set(earlier_devices) & set(later_devices)) > 0
            )

            if (
                earlier_is_authentication
                and later_is_browser
                and shared_user
                and shared_source_ip
                and shared_device
            ):
                correlations.append({
                    "rule": "authentication_followed_by_browser_activity",

                    "time_difference_seconds": int(
                        time_difference
                    ),

                    "earlier_event": earlier_summary,

                    "later_event": later_summary,

                    "reason": (
                        "The same user, source IP, and device "
                        "were observed during authentication "
                        "followed by browser activity within 5 minutes."
                    )
                })

    return correlations


# ------------------------------------------------
# Main program
# ------------------------------------------------

events = load_evidence(
    "extracted_entities.json"
)

correlations = correlate_events(events)

save_correlations(
    correlations,
    "correlations.json"
)

print(
    f"\nCorrelations found: {len(correlations)}"
)

print(
    "Correlation results saved to correlations.json"
)