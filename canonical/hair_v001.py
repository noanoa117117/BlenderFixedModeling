"""Apply the visually accepted Lasyusha hair v001 to the open Blender scene.

Base: Lasyusha-ShoulderFlow-Fixed.blend
Intent: preserve the original long-hair flow while removing the obvious shoulder
        flip-ups and completing strands that had been cut too abruptly.
Visual review: 2026-09-18, Blender close-ups from both sides.

The versioned blend is a local dependency because the source is a commercial hair
asset. This script is intentionally idempotent: it replaces mesh data on the six
known hair objects and never creates duplicates.
"""

from pathlib import Path
import bpy


VERSION = "v001"
SOURCE_ARTIFACT = "artifacts/Lasyusha-v001.blend"
TARGET_OBJECTS = ("back", "bangs side", "base", "side1", "side2", "side3")


def repo_root() -> Path:
    injected = globals().get("HAIRFLOW_ROOT")
    if injected:
        return Path(injected)
    if "__file__" in globals():
        return Path(__file__).resolve().parents[1]
    raise RuntimeError("HAIRFLOW_ROOT is required when executed through Blender MCP")


def apply() -> None:
    source_path = repo_root() / SOURCE_ARTIFACT
    if not source_path.exists():
        raise FileNotFoundError(source_path)

    missing = [name for name in TARGET_OBJECTS if bpy.data.objects.get(name) is None]
    if missing:
        raise RuntimeError(f"Target hair objects are missing: {missing}")

    requested_names = list(TARGET_OBJECTS)
    with bpy.data.libraries.load(str(source_path), link=False) as (available, loaded):
        unavailable = [name for name in TARGET_OBJECTS if name not in available.objects]
        if unavailable:
            raise RuntimeError(f"Source artifact is missing objects: {unavailable}")
        # Blender replaces the assigned list entries with loaded Object instances.
        # Keep the immutable TARGET_OBJECTS tuple separate from that mutable list.
        loaded.objects = requested_names

    for name, source_object in zip(TARGET_OBJECTS, loaded.objects):
        if source_object is None:
            raise RuntimeError(f"Failed to load source object: {name}")
        target = bpy.data.objects[name]
        target.data = source_object.data.copy()
        target["hairflow_version"] = VERSION
        target["hairflow_source"] = SOURCE_ARTIFACT

    bpy.context.scene["hairflow_version"] = VERSION
    bpy.context.scene["hairflow_source"] = SOURCE_ARTIFACT
    bpy.context.view_layer.update()
    print(f"HAIRFLOW_APPLY_OK version={VERSION} objects={len(TARGET_OBJECTS)}")


apply()
