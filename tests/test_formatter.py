import unittest
from unittest import mock

from edge_data_collector.formatter.data_formatter import format_data


class FormatDataTests(unittest.TestCase):
    def test_defaults_added_when_missing(self):
        metadata = {"timestamp": "2024-01-01T00:00:00"}
        sensor_data = {"temperature": 25}

        with mock.patch(
            "edge_data_collector.formatter.data_formatter.encode_image",
            return_value="encoded-image",
        ):
            payload = format_data("/tmp/image.jpg", sensor_data, metadata)

        meta = payload["metadata"]
        self.assertEqual(meta["motion"], "slow")
        self.assertFalse(meta["resource_constrained"])

    def test_existing_hints_are_normalised(self):
        metadata = {"motion": "FAST", "resource_constrained": True}
        sensor_data = {"temperature": 25}

        with mock.patch(
            "edge_data_collector.formatter.data_formatter.encode_image",
            return_value="encoded-image",
        ):
            payload = format_data("/tmp/image.jpg", sensor_data, metadata)

        meta = payload["metadata"]
        self.assertEqual(meta["motion"], "fast")
        self.assertTrue(meta["resource_constrained"])

    def test_invalid_motion_falls_back_to_default(self):
        metadata = {"motion": "hover", "resource_constrained": "false"}
        sensor_data = {"temperature": 25}

        with mock.patch(
            "edge_data_collector.formatter.data_formatter.encode_image",
            return_value="encoded-image",
        ):
            payload = format_data("/tmp/image.jpg", sensor_data, metadata)

        meta = payload["metadata"]
        self.assertEqual(meta["motion"], "slow")
        self.assertFalse(meta["resource_constrained"])


if __name__ == "__main__":
    unittest.main()
