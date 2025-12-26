import unittest
import os
import json
import tempfile
from src.defect_scanner import FabricScanner


class TestFabricScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = FabricScanner()

    def test_initialization(self):
        """Test if the scanner initializes with correct defaults."""
        self.assertEqual(self.scanner.scanned_yards, 0)
        self.assertEqual(self.scanner.defects_found, 0)
        self.assertTrue(len(self.scanner.defects) > 0)

    def test_analyze_frame_structure(self):
        """Test if analyze_frame returns a dictionary with expected keys."""
        result = self.scanner.analyze_frame("TEST-FRAME-001")
        self.assertIsInstance(result, dict)
        self.assertIn("detected", result)
        if result["detected"]:
            self.assertIn("type", result)
            self.assertIn("confidence", result)

    def test_report_generation(self):
        """Test if run_simulation generates a valid JSON report."""
        # Create a temporary file for output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            output_path = temp_file.name

        try:
            # Run a very short simulation
            self.scanner.run_simulation(duration_seconds=1, output_file=output_path)

            # Verify file exists and contains valid JSON
            self.assertTrue(os.path.exists(output_path))
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertIn("start_time", data)
            self.assertIn("defects", data)
            self.assertIn("summary", data)
            self.assertIsInstance(data["defects"], list)

        finally:
            # Clean up
            if os.path.exists(output_path):
                os.remove(output_path)


if __name__ == "__main__":
    unittest.main()
