import unittest

from hybrid_analyzer import find_sequence_correlations


class TestHybridAnalyzer(unittest.TestCase):

    def setUp(self):
        self.correlations = [
            {
                "rule": "failed_login_followed_by_network_activity",
                "earlier_event": {
                    "source_ip": "192.168.1.15"
                },
                "later_event": {
                    "source_ip": "192.168.1.15"
                },
                "reason": "Failed login followed by network activity."
            },
            {
                "rule": "authentication_followed_by_browser_activity",
                "earlier_event": {
                    "source_ip": "192.168.1.10"
                },
                "later_event": {
                    "source_ip": "192.168.1.10"
                },
                "reason": "Authentication followed by browser activity."
            },
            {
                "rule": "authentication_followed_by_browser_activity",
                "earlier_event": {
                    "source_ip": "192.168.1.10"
                },
                "later_event": {
                    "source_ip": "192.168.1.10"
                },
                "reason": "Authentication followed by browser activity."
            }
        ]

    def test_single_correlation_matches_sequence(self):
        sequence = {
            "source_ip": "192.168.1.15"
        }

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
        sequence = {
            "source_ip": "192.168.1.10"
        }

        result = find_sequence_correlations(
            sequence,
            self.correlations
        )

        self.assertEqual(len(result), 2)

        for correlation in result:
            self.assertEqual(
                correlation["rule"],
                "authentication_followed_by_browser_activity"
            )

    def test_sequence_with_no_correlation(self):
        sequence = {
            "source_ip": "192.168.1.20"
        }

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


if __name__ == "__main__":
    unittest.main()