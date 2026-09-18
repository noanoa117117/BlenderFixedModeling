import json
import hashlib
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowFilesTest(unittest.TestCase):
    def test_config_references_existing_files(self):
        config = json.loads((ROOT / "config" / "project.json").read_text(encoding="utf-8"))
        self.assertTrue((ROOT / config["canonical_script"]).is_file())
        self.assertTrue((ROOT / config["artifact"]).is_file())
        self.assertEqual(set(config["hair_objects"]), set(config["expected"]))

    def test_expected_counts_are_positive(self):
        config = json.loads((ROOT / "config" / "project.json").read_text(encoding="utf-8"))
        for metrics in config["expected"].values():
            self.assertGreater(metrics["vertices"], 0)
            self.assertGreater(metrics["edges"], 0)
            self.assertGreater(metrics["polygons"], 0)

    def test_artifact_matches_manifest(self):
        config = json.loads((ROOT / "config" / "project.json").read_text(encoding="utf-8"))
        artifact = ROOT / config["artifact"]
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        self.assertEqual(config["artifact_sha256"], digest)

    def test_local_blends_are_ignored(self):
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("artifacts/*.blend", ignore)


if __name__ == "__main__":
    unittest.main()
