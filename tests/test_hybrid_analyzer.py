
import unittest

from src.analysis.hybrid_analyzer import (
    find_sequence_correlations,
    build_rule_findings,
    build_correlated_events,
    determine_assessment
)


class TestHybridAnalyzer(unittest.TestCase):

    def setUp(self):
        self.correlations = [
            {
                "rule": "failed_login_followed_by_network_activity",
                "earlier_event": {
                    "source_ip": "192.168.1.15",
                    "user": "bob"
                },
                "later_event": {
                    "source_ip": "192.168.1.15"
                },
                "time_difference_seconds": 246,
                "reason": "Failed login followed by network activity."
            },
            {
                "rule": "authentication_followed_by_browser_activity",
                "earlier_event": {
                    "source_ip": "192.168.1.10",
                    "user": "alice"
                },
                "later_event": {
                    "source_ip": "192.168.1.10",
                    "resource": "https://example.com/login"
                },
                "time_difference_seconds": 183,
                "reason": "Authentication followed by browser activity."
            },
            {
                "rule": "authentication_followed_by_browser_activity",
                "earlier_event": {
                    "source_ip": "192.168.1.10",
                    "user": "alice"
                },
                "later_event": {
                    "source_ip": "192.168.1.10",
                    "resource": "https://example.com/download"
                },
                "time_difference_seconds": 250,
                "reason": "Authentication followed by browser activity."
            }
        ]

    def test_single_correlation_matches_sequence(self):
        sequence = {"source_ip": "192.168.1.15"}

        result = find_sequence_correlations(
            sequence,
            self.correlations
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["rule"],
            "failed_login_followed_by_network_activity"
        )

    def test_multiple_correlations_match_sequence(self):
        sequence = {"source_ip": "192.168.1.10"}

        result = find_sequence_correlations(
            sequence,
            self.correlations
        )

        self.assertEqual(len(result), 2)

    def test_sequence_with_no_correlation(self):
        sequence = {"source_ip": "192.168.1.20"}

        result = find_sequence_correlations(
            sequence,
            self.correlations
        )

        self.assertEqual(result, [])

    def test_sequence_with_missing_source_ip(self):
        sequence = {}

        result = find_sequence_correlations(
            sequence,
            self.correlations
        )

        self.assertEqual(result, [])

    def test_duplicate_findings_are_removed(self):
        findings = build_rule_findings(
            self.correlations[1:]
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0],
            "Authentication followed by browser activity."
        )

    def test_correlated_events_are_preserved(self):
        events = build_correlated_events(
            self.correlations[1:]
        )

        self.assertEqual(len(events), 2)

        self.assertEqual(
            events[0]["later_event"]["resource"],
            "https://example.com/login"
        )

        self.assertEqual(
            events[1]["later_event"]["resource"],
            "https://example.com/download"
        )

        self.assertEqual(
            events[0]["time_difference_seconds"],
            183
        )

        self.assertEqual(
            events[1]["time_difference_seconds"],
            250
        )

    def test_assessment_for_normal_correlated_activity(self):
        assessment = determine_assessment(
            ["Authentication followed by browser activity."],
            {"prediction": "normal"}
        )

        self.assertEqual(
            assessment,
            "correlated_activity_observed"
        )

    def test_assessment_for_suspicious_correlated_activity(self):
        assessment = determine_assessment(
            ["Failed login followed by network activity."],
            {"prediction": "suspicious"}
        )

        self.assertEqual(
            assessment,
            "requires_investigation"
        )


if __name__ == "__main__":
    unittest.main()
