import json


def load_correlations(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def analyze_correlation(correlation):
    rule = correlation["rule"]

    earlier_event = correlation["earlier_event"]
    later_event = correlation["later_event"]

    score = 0
    findings = []

    # ------------------------------------------------
    # Pattern 1:
    # Failed authentication followed by firewall activity
    # ------------------------------------------------

    if rule == "failed_login_followed_by_network_activity":

        score += 40

        findings.append(
            "A failed authentication attempt was detected."
        )

        findings.append(
            "Network activity occurred shortly after "
            "the failed authentication."
        )

        if later_event["action"] == "deny":
            score += 20

            findings.append(
                "The subsequent firewall activity was denied."
            )

    # ------------------------------------------------
    # Pattern 2:
    # Authentication followed by browser activity
    # ------------------------------------------------

    elif rule == "authentication_followed_by_browser_activity":

        score += 10

        findings.append(
            "Browser activity occurred shortly after authentication."
        )

        if earlier_event["status"] == "success":
            findings.append(
                "The authentication attempt was successful."
            )

    # ------------------------------------------------
    # Determine suspicion level
    # ------------------------------------------------

    if score >= 50:
        suspicion = "high"

    elif score >= 25:
        suspicion = "medium"

    else:
        suspicion = "low"

    return {
        "rule": rule,
        "suspicion_score": score,
        "suspicion_level": suspicion,
        "findings": findings,
        "explanation": generate_explanation(
            suspicion,
            findings
        )
    }


def generate_explanation(suspicion, findings):

    if suspicion == "high":
        introduction = (
            "The correlated events show a potentially suspicious "
            "behavioural pattern."
        )

    elif suspicion == "medium":
        introduction = (
            "The correlated events show a pattern that "
            "may require further investigation."
        )

    else:
        introduction = (
            "The correlated events do not currently indicate "
            "strongly suspicious behaviour."
        )

    return introduction + " " + " ".join(findings)


def analyze_all_correlations(correlations):
    results = []

    for correlation in correlations:

        analysis = analyze_correlation(
            correlation
        )

        results.append({
            "correlation": correlation,
            "ai_analysis": analysis
        })

    return results


def save_analysis(results, file_path):

    with open(file_path, "w") as file:
        json.dump(
            results,
            file,
            indent=4
        )


# ------------------------------------------------
# Main program
# ------------------------------------------------

correlations = load_correlations(
    "correlations.json"
)

results = analyze_all_correlations(
    correlations
)

save_analysis(
    results,
    "ai_analysis.json"
)

print(
    f"\nAI analysis completed for {len(results)} correlations."
)

print(
    "AI analysis saved to ai_analysis.json"
)