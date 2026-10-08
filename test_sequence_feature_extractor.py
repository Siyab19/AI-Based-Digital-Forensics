import unittest

from sequence_feature_extractor import extract_features


class TestSequenceFeatureExtractor(unittest.TestCase):

    def test_failed_login_and_firewall_denial(self):
        sequence = {
            "sequence_id": 1,
            "source_ip": "192.168.1.15",
            "start_time": "2026-09-07T14:31:15",
            "end_time": "2026-09-07T14:35:21",
            "events": [
                {
                    "timestamp": "2026-09-07T14:31:15",
                    "source": "authentication",
                    "status": "failed",
                    "action": "login"
                },
                {
                    "timestamp": "2026-09-07T14:35:21",
                    "source": "firewall",
                    "status": None,
                    "action": "deny"
                }
            ]
        }

        features = extract_features(sequence)

        self.assertEqual(features["failed_login_count"], 1)
        self.assertEqual(features["firewall_denial_count"], 1)
        self.assertEqual(features["total_event_count"], 2)

    def test_successful_login_after_failure(self):
        sequence = {
            "sequence_id": 2,
            "source_ip": "192.168.1.10",
            "start_time": "2026-09-07T14:30:00",
            "end_time": "2026-09-07T14:32:00",
            "events": [
                {
                    "timestamp": "2026-09-07T14:30:00",
                    "source": "authentication",
                    "status": "failed",
                    "action": "login"
                },
                {
                    "timestamp": "2026-09-07T14:32:00",
                    "source": "authentication",
                    "status": "success",
                    "action": "login"
                }
            ]
        }

        features = extract_features(sequence)

        self.assertEqual(features["failed_login_count"], 1)
        self.assertEqual(features["successful_login_count"], 1)
        self.assertEqual(
            features["successful_login_after_failure"],
            1
        )

    def test_browser_activity(self):
        sequence = {
            "sequence_id": 3,
            "source_ip": "192.168.1.20",
            "start_time": "2026-09-07T14:30:00",
            "end_time": "2026-09-07T14:33:00",
            "events": [
                {
                    "timestamp": "2026-09-07T14:30:00",
                    "source": "browser_history",
                    "status": None,
                    "action": "access"
                },
                {
                    "timestamp": "2026-09-07T14:33:00",
                    "source": "browser_history",
                    "status": None,
                    "action": "access"
                }
            ]
        }

        features = extract_features(sequence)

        self.assertEqual(features["browser_activity_count"], 2)
        self.assertEqual(features["number_of_evidence_sources"], 1)

    def test_sequence_duration(self):
        sequence = {
            "sequence_id": 4,
            "source_ip": "192.168.1.30",
            "start_time": "2026-09-07T14:30:00",
            "end_time": "2026-09-07T14:35:00",
            "events": [
                {
                    "timestamp": "2026-09-07T14:30:00",
                    "source": "firewall",
                    "status": None,
                    "action": "allow"
                },
                {
                    "timestamp": "2026-09-07T14:35:00",
                    "source": "firewall",
                    "status": None,
                    "action": "allow"
                }
            ]
        }

        features = extract_features(sequence)

        self.assertEqual(
            features["sequence_duration_seconds"],
            300
        )


if __name__ == "__main__":
    unittest.main()