"""Export the visible, evaluated hair shape in the Unity reference coordinate frame."""
import bpy, json
from pathlib import Path
NAMES = ['back','bangs side','base','pin','side1','side2','side3','ShoulderWisps_Subtle']
out=[]
deps=bpy.context.evaluated_depsgraph_get()
for name in NAMES:
    ob=bpy.data.objects[name]
    ev=ob.evaluated_get(deps)
    me=ev.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
    me.calc_loop_triangles()
    normal_matrix=ev.matrix_world.to_3x3().inverted().transposed()
    vertices=[]
    for loop in me.loops:
        vert=me.vertices[loop.vertex_index]
        p=ev.matrix_world@vert.co
        n=(normal_matrix@me.corner_normals[loop.index].vector).normalized()
        uv=me.uv_layers.active.data[loop.index].uv if me.uv_layers.active else (0,0)
        weights=sorted([(ob.vertex_groups[g.group].name,g.weight) for g in vert.groups if g.weight>0],key=lambda x:-x[1])[:4]
        vertices.append(dict(p=[-p.x,p.z+.016,-p.y-.0034],n=[-n.x,n.z,-n.y],uv=list(uv),bones=[w[0] for w in weights],weights=[w[1] for w in weights]))
    triangles=[[] for _ in range(max(1,len(me.materials)))]
    for tri in me.loop_triangles:
        a,b,c=tri.loops
        # The reflection converts Blender CCW faces into Unity clockwise faces.
        triangles[tri.material_index].extend([a,b,c])
    out.append(dict(name=name,enabled=not ob.hide_render,vertices=vertices,triangles=triangles,materials=[m.name if m else '' for m in me.materials]))
    print(name, len(me.vertices), len(vertices), 'enabled',not ob.hide_render)
    ev.to_mesh_clear()
path=Path(r'E:\BlenderHairWorkflow\artifacts\unity-evaluated.json')
path.write_text(json.dumps(out,separators=(',',':')),encoding='utf-8')
print(path)
