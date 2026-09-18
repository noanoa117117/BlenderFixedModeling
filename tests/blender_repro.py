"""Blender-side smoke test: apply v001 to the baseline and verify mesh counts."""

import json
from pathlib import Path
import runpy
import bpy


ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "config" / "project.json").read_text(encoding="utf-8"))

runpy.run_path(str(ROOT / config["canonical_script"]), run_name="__main__")

actual = {}
for name in config["hair_objects"]:
    data = bpy.data.objects[name].data
    actual[name] = {
        "vertices": len(data.vertices),
        "edges": len(data.edges),
        "polygons": len(data.polygons),
    }

if actual != config["expected"]:
    raise RuntimeError(json.dumps({"expected": config["expected"], "actual": actual}, ensure_ascii=False))

print("HAIRFLOW_REPRO_OK=" + json.dumps(actual, ensure_ascii=False))

