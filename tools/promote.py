"""Promote a manually reviewed blend file to the next local hair version."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "project.json"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    if not args.version.startswith("v") or not args.version[1:].isdigit():
        raise SystemExit("version must look like v002")
    source = args.source.resolve()
    if not source.is_file() or source.suffix.lower() != ".blend":
        raise SystemExit(f"not a blend file: {source}")

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    destination = ROOT / "artifacts" / f"Lasyusha-{args.version}.blend"
    canonical = ROOT / "canonical" / f"hair_{args.version}.py"
    if destination.exists() or canonical.exists():
        raise SystemExit("destination version already exists; refusing to overwrite")

    previous = ROOT / config["canonical_script"]
    source_text = previous.read_text(encoding="utf-8")
    source_text = source_text.replace(config["current_version"], args.version)
    source_text = source_text.replace(config["artifact"], f"artifacts/Lasyusha-{args.version}.blend")

    shutil.copy2(source, destination)
    canonical.write_text(source_text, encoding="utf-8")
    config["current_version"] = args.version
    config["canonical_script"] = f"canonical/hair_{args.version}.py"
    config["artifact"] = f"artifacts/Lasyusha-{args.version}.blend"
    config["artifact_sha256"] = file_hash(destination)
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "version": args.version,
        "artifact": str(destination),
        "sha256": file_hash(destination),
        "canonical": str(canonical),
        "next": "update expected metrics, CHANGELOG.md, and visual-review handoff",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
