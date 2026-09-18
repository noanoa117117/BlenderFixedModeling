"""Restore the accepted Lasyusha hair v002 meshes in the open Blender scene.

v002 keeps the v001 hair geometry unchanged and adds
``ShoulderWisps_Subtle`` to the reproducible set.  It is intentionally an
artifact-backed restore: the `.blend` contains the commercial asset data and
the complete manually reviewed object setup.
"""

from pathlib import Path

import bpy


VERSION = "v002"
SOURCE_ARTIFACT = "artifacts/Lasyusha-v002.blend"
TARGET_OBJECTS = (
    "back",
    "bangs side",
    "base",
    "side1",
    "side2",
    "side3",
)
WISP_OBJECT = "ShoulderWisps_Subtle"


def repo_root() -> Path:
    injected = globals().get("HAIRFLOW_ROOT")
    if injected:
        return Path(injected)
    if "__file__" in globals():
        return Path(__file__).resolve().parents[1]
    raise RuntimeError("HAIRFLOW_ROOT is required when executed through Blender MCP")


def artifact_path() -> Path:
    path = repo_root() / SOURCE_ARTIFACT
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def discard_transient_sources(objects: set[bpy.types.Object]) -> None:
    """Remove objects and meshes created only to read the source artifact."""
    meshes = [object_.data for object_ in objects if object_.type == "MESH"]
    # Source meshes can be children of a source armature, so discard children
    # before armatures.  These objects were created by libraries.load and were
    # never part of the target scene.
    for object_ in sorted(objects, key=lambda item: item.type == "ARMATURE"):
        if object_.name in bpy.data.objects:
            bpy.data.objects.remove(object_, do_unlink=True)
    for mesh in meshes:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def replace_mesh_data(names: tuple[str, ...], source_path: Path) -> None:
    missing = [name for name in names if bpy.data.objects.get(name) is None]
    if missing:
        raise RuntimeError(f"Target hair objects are missing: {missing}")

    before_objects = set(bpy.data.objects)
    requested_names = list(names)
    with bpy.data.libraries.load(str(source_path), link=False) as (available, loaded):
        unavailable = [name for name in names if name not in available.objects]
        if unavailable:
            raise RuntimeError(f"Source artifact is missing objects: {unavailable}")
        loaded.objects = requested_names

    source_objects = list(loaded.objects)
    for name, source_object in zip(names, source_objects):
        if source_object is None:
            raise RuntimeError(f"Failed to load source object: {name}")
        target = bpy.data.objects[name]
        previous_data = target.data
        target.data = source_object.data.copy()
        if previous_data.users == 0:
            bpy.data.meshes.remove(previous_data)
        target["hairflow_version"] = VERSION
        target["hairflow_source"] = SOURCE_ARTIFACT
    discard_transient_sources(set(bpy.data.objects) - before_objects)


def restore_wisps(source_path: Path, armature: bpy.types.Object) -> None:
    target = bpy.data.objects.get(WISP_OBJECT)
    if target is None:
        # Append the object instead of rebuilding it: this retains its armature
        # parent, armature modifier, vertex groups, and collection membership.
        directory = str(source_path) + "/Object/"
        result = bpy.ops.wm.append(
            filepath=directory + WISP_OBJECT,
            directory=directory,
            filename=WISP_OBJECT,
        )
        if "FINISHED" not in result:
            raise RuntimeError(f"Failed to append missing object: {WISP_OBJECT}")
        target = bpy.data.objects.get(WISP_OBJECT)
        if target is None:
            raise RuntimeError(f"Appended object is unavailable: {WISP_OBJECT}")
        appended_parent = target.parent
        world_matrix = target.matrix_world.copy()
        target.parent = armature
        target.matrix_parent_inverse = armature.matrix_world.inverted()
        target.matrix_world = world_matrix
        for modifier in target.modifiers:
            if modifier.type == "ARMATURE":
                modifier.object = armature
        # Appending a single object may also append its source armature.  The
        # six managed meshes establish the armature already present in the
        # target scene, so detach the wisp from that duplicate dependency.
        if appended_parent is not None and appended_parent != armature:
            if not appended_parent.children:
                bpy.data.objects.remove(appended_parent, do_unlink=True)
    else:
        before_objects = set(bpy.data.objects)
        with bpy.data.libraries.load(str(source_path), link=False) as (available, loaded):
            if WISP_OBJECT not in available.objects:
                raise RuntimeError(f"Source artifact is missing object: {WISP_OBJECT}")
            loaded.objects = [WISP_OBJECT]
        source_object = loaded.objects[0]
        if source_object is None:
            raise RuntimeError(f"Failed to load source object: {WISP_OBJECT}")
        previous_data = target.data
        target.data = source_object.data.copy()
        if previous_data.users == 0:
            bpy.data.meshes.remove(previous_data)
        discard_transient_sources(set(bpy.data.objects) - before_objects)

    target["hairflow_version"] = VERSION
    target["hairflow_source"] = SOURCE_ARTIFACT


def apply() -> None:
    source_path = artifact_path()
    replace_mesh_data(TARGET_OBJECTS, source_path)
    armature = bpy.data.objects[TARGET_OBJECTS[0]].parent
    if armature is None or armature.type != "ARMATURE":
        raise RuntimeError(f"{TARGET_OBJECTS[0]} must be parented to an armature")
    restore_wisps(source_path, armature)
    bpy.context.scene["hairflow_version"] = VERSION
    bpy.context.scene["hairflow_source"] = SOURCE_ARTIFACT
    bpy.context.view_layer.update()
    print(f"HAIRFLOW_APPLY_OK version={VERSION} objects={len(TARGET_OBJECTS) + 1}")


apply()
