---
name: hairflow
description: Run the controlled Blender hair adjustment loop in BlenderHairWorkflow. Use for hair shape, fit, penetration, or silhouette corrections in this repository.
---

# Hairflow

Use this repository's controlled edit loop. The goal is a natural hairstyle that follows clothing where required, without recreating the commercial source data.

1. Read `config/project.json`, `docs/STATE.md`, and `docs/KNOWLEDGE.md`.
2. Use `python tools/hairflow.py status` before changing the current version.
3. Make repeatable changes in the versioned canonical script or a versioned Blender script, then run `apply` and `validate` through `tools/hairflow.py`.
4. Use Computer Use only when `gate --silhouette-changed --unresolved-visual` requires visual confirmation. Inspect all relevant sides and close-ups.
5. For a manual correction, save a new `.blend` and run `tools/promote.py` so the edit becomes the next reproducible version.

Do not call Blender MCP tools directly and do not send ad-hoc Blender Python through MCP. `tools/hairflow.py` is the only Blender communication bridge. If it lacks an operation, add a tested, versioned operation before using it.
