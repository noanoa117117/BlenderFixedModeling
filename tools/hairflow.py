"""Small command line entry point for the Blender hair workflow."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import socket
import sys


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "project.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def blender_call(code: str, config: dict) -> dict:
    mcp = config["mcp"]
    payload = json.dumps({"type": "execute_code", "params": {"code": code}}).encode("utf-8")
    with socket.create_connection((mcp["host"], mcp["port"]), mcp["timeout_seconds"]) as client:
        client.settimeout(mcp["timeout_seconds"])
        client.sendall(payload)
        chunks: list[bytes] = []
        while True:
            try:
                data = client.recv(1024 * 1024)
            except socket.timeout:
                break
            if not data:
                break
            chunks.append(data)
            try:
                return json.loads(b"".join(chunks).decode("utf-8"))
            except json.JSONDecodeError:
                continue
    raise RuntimeError("Blender MCP returned no complete JSON response")


def execute_file(path: Path, config: dict, prelude: str = "") -> dict:
    code = (
        f"HAIRFLOW_ROOT = {str(ROOT)!r}\n"
        + prelude
        + f"exec(compile(open({str(path)!r}, encoding='utf-8').read(), {str(path)!r}, 'exec'))"
    )
    return blender_call(code, config)


def response_text(response: dict) -> str:
    result = response.get("result", response)
    if isinstance(result, dict):
        return str(result.get("result", result))
    return str(result)


def command_status(config: dict) -> int:
    artifact = ROOT / config["artifact"]
    canonical = ROOT / config["canonical_script"]
    report = {
        "version": config["current_version"],
        "canonical_exists": canonical.exists(),
        "artifact_exists": artifact.exists(),
        "artifact_sha256": sha256(artifact) if artifact.exists() else None,
        "artifact_bytes": artifact.stat().st_size if artifact.exists() else None,
    }
    report["artifact_matches_manifest"] = (
        report["artifact_sha256"] == config.get("artifact_sha256")
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if (
        report["canonical_exists"]
        and report["artifact_exists"]
        and report["artifact_matches_manifest"]
    ) else 1


def command_apply(config: dict) -> int:
    response = execute_file(ROOT / config["canonical_script"], config)
    print(response_text(response))
    return 0 if response.get("status") == "success" else 1


def command_validate(config: dict) -> int:
    prelude = (
        f"HAIRFLOW_EXPECTED = {config['expected']!r}\n"
        f"HAIRFLOW_OBJECTS = {config['hair_objects']!r}\n"
    )
    response = execute_file(ROOT / "blender" / "validate.py", config, prelude)
    text = response_text(response)
    print(text)
    return 0 if '"ok": true' in text.lower() else 1


def command_view(config: dict, angle: str, closeup: bool) -> int:
    prelude = f"HAIRFLOW_ANGLE = {angle!r}\n"
    if closeup:
        prelude += "HAIRFLOW_VIEW_DISTANCE = 0.24\n"
    response = execute_file(ROOT / "blender" / "view_setup.py", config, prelude)
    print(response_text(response))
    return 0 if response.get("status") == "success" else 1


def command_gate(config: dict, silhouette_changed: bool, unresolved_visual: bool) -> int:
    valid = command_validate(config) == 0
    required = valid and silhouette_changed and unresolved_visual
    print("VISUAL_REVIEW_REQUIRED" if required else "STAY_IN_EDIT_LOOP")
    print(json.dumps({
        "numeric_validation": valid,
        "silhouette_changed": silhouette_changed,
        "unresolved_visual": unresolved_visual,
    }, ensure_ascii=False))
    return 0 if valid else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("apply")
    sub.add_parser("validate")
    view = sub.add_parser("view")
    view.add_argument("angle", choices=[
        "front", "front-right", "right", "back", "left", "front-left", "back-right", "back-left"
    ])
    view.add_argument("--closeup", action="store_true")
    gate = sub.add_parser("gate")
    gate.add_argument("--silhouette-changed", action="store_true")
    gate.add_argument("--unresolved-visual", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config()
    if args.command == "status":
        return command_status(config)
    if args.command == "apply":
        return command_apply(config)
    if args.command == "validate":
        return command_validate(config)
    if args.command == "view":
        return command_view(config, args.angle, args.closeup)
    if args.command == "gate":
        return command_gate(config, args.silhouette_changed, args.unresolved_visual)
    raise AssertionError(args.command)


if __name__ == "__main__":
    sys.exit(main())
