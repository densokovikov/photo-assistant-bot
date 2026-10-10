import json
import tempfile
import unittest
from pathlib import Path

from app_io import load_json, save_json


class JsonStorageTest(unittest.TestCase):
    def test_missing_file_returns_independent_default(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"
            default = {"photographer_index": 0}

            loaded = load_json(path, default)
            loaded["photographer_index"] = 4

            self.assertEqual(default["photographer_index"], 0)

    def test_saves_utf8_json_atomically(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"

            save_json(path, {"name": "Надар"})

            self.assertEqual(load_json(path, {}), {"name": "Надар"})
            self.assertFalse(path.with_suffix(".json.tmp").exists())
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["name"], "Надар")


if __name__ == "__main__":
    unittest.main()
