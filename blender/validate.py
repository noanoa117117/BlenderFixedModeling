"""Numeric validation executed inside Blender."""

import json
import bpy


expected = globals().get("HAIRFLOW_EXPECTED", {})
names = globals().get("HAIRFLOW_OBJECTS", list(expected))
result = {"ok": True, "objects": {}, "errors": []}

for name in names:
    obj = bpy.data.objects.get(name)
    if obj is None:
        result["ok"] = False
        result["errors"].append(f"missing object: {name}")
        continue

    data = obj.data
    metrics = {
        "vertices": len(data.vertices),
        "edges": len(data.edges),
        "polygons": len(data.polygons),
    }

    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    points = [obj.matrix_world @ vertex.co for vertex in mesh.vertices]
    evaluated.to_mesh_clear()
    if points:
        metrics["bounds_min"] = [round(min(point[i] for point in points), 6) for i in range(3)]
        metrics["bounds_max"] = [round(max(point[i] for point in points), 6) for i in range(3)]

    result["objects"][name] = metrics
    for key, wanted in expected.get(name, {}).items():
        if metrics.get(key) != wanted:
            result["ok"] = False
            result["errors"].append(
                f"{name}.{key}: expected {wanted}, got {metrics.get(key)}"
            )

print("HAIRFLOW_RESULT=" + json.dumps(result, ensure_ascii=False))

