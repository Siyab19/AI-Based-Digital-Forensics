import unittest

from sequence_builder import build_sequences


class TestSequenceBuilder(unittest.TestCase):

    def test_events_within_window_form_one_sequence(self):
        evidence = [
            {
                "timestamp": "2026-09-07T14:30:00",
                "source": "authentication",
                "source_ip": "192.168.1.10"
            },
            {
                "timestamp": "2026-09-07T14:34:00",
                "source": "firewall",
                "source_ip": "192.168.1.10"
            }
        ]

        sequences = build_sequences(evidence)

        self.assertEqual(len(sequences), 1)
        self.assertEqual(len(sequences[0]["events"]), 2)

    def test_events_outside_window_form_separate_sequences(self):
        evidence = [
            {
                "timestamp": "2026-09-07T14:30:00",
                "source": "authentication",
                "source_ip": "192.168.1.10"
            },
            {
                "timestamp": "2026-09-07T14:36:00",
                "source": "firewall",
                "source_ip": "192.168.1.10"
            }
        ]

        sequences = build_sequences(evidence)

        self.assertEqual(len(sequences), 2)

    def test_different_source_ips_form_different_sequences(self):
        evidence = [
            {
                "timestamp": "2026-09-07T14:30:00",
                "source": "authentication",
                "source_ip": "192.168.1.10"
            },
            {
                "timestamp": "2026-09-07T14:31:00",
                "source": "authentication",
                "source_ip": "192.168.1.15"
            }
        ]

        sequences = build_sequences(evidence)

        self.assertEqual(len(sequences), 2)

    def test_events_are_sorted_chronologically(self):
        evidence = [
            {
                "timestamp": "2026-09-07T14:34:00",
                "source": "firewall",
                "source_ip": "192.168.1.10"
            },
            {
                "timestamp": "2026-09-07T14:30:00",
                "source": "authentication",
                "source_ip": "192.168.1.10"
            }
        ]

        sequences = build_sequences(evidence)

        self.assertEqual(
            sequences[0]["events"][0]["timestamp"],
            "2026-09-07T14:30:00"
        )

        self.assertEqual(
            sequences[0]["events"][1]["timestamp"],
            "2026-09-07T14:34:00"
        )

    def test_missing_source_ip_is_ignored(self):
        evidence = [
            {
                "timestamp": "2026-09-07T14:30:00",
                "source": "authentication",
                "source_ip": None
            }
        ]

        sequences = build_sequences(evidence)

        self.assertEqual(len(sequences), 0)


if __name__ == "__main__":
    unittest.main()