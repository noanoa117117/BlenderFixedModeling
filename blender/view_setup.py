"""Set a repeatable Blender viewport angle for visual review."""

import math
import bpy


ANGLE = globals().get("HAIRFLOW_ANGLE", "front")
CENTER = globals().get("HAIRFLOW_VIEW_CENTER", (0.0, 0.0, 1.27))
DISTANCE = globals().get("HAIRFLOW_VIEW_DISTANCE", 0.58)

base_axis = {
    "front": "FRONT",
    "right": "RIGHT",
    "back": "BACK",
    "left": "LEFT",
}
orbit = {
    "front-right": ("FRONT", "ORBITLEFT", math.pi / 4),
    "front-left": ("FRONT", "ORBITRIGHT", math.pi / 4),
    "back-right": ("BACK", "ORBITRIGHT", math.pi / 4),
    "back-left": ("BACK", "ORBITLEFT", math.pi / 4),
}

if ANGLE not in base_axis and ANGLE not in orbit:
    raise ValueError(f"Unknown review angle: {ANGLE}")

changed = 0
for area in bpy.context.screen.areas:
    if area.type != "VIEW_3D":
        continue
    region = next((item for item in area.regions if item.type == "WINDOW"), None)
    if region is None:
        continue
    with bpy.context.temp_override(area=area, region=region):
        if ANGLE in base_axis:
            bpy.ops.view3d.view_axis(type=base_axis[ANGLE])
        else:
            axis, direction, radians = orbit[ANGLE]
            bpy.ops.view3d.view_axis(type=axis)
            bpy.ops.view3d.view_orbit(type=direction, angle=radians)
    area.spaces.active.region_3d.view_location = CENTER
    area.spaces.active.region_3d.view_distance = DISTANCE
    area.tag_redraw()
    changed += 1

print(f"HAIRFLOW_VIEW_OK angle={ANGLE} areas={changed}")

