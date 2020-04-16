import bpy
from bpy import context
from mathutils import Matrix, Vector, Euler
from math import degrees

rodradius = 0.25 # set radius of truss rods
rodrez = 8

jointradius = 0.28 # set radius of ball joints
jointrez = 2

obj = context.active_object

# get all verts and generate ball joints in vert locations
for i in range(len(obj.data.vertices)):
    v = obj.data.vertices[i]
    co_final = obj.matrix_world @ v.co
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=jointrez, radius=jointradius, location=co_final)
    bpy.ops.object.shade_smooth()
    bpy.context.active_object.name = 'trussballs'   
    bpy.ops.object.select_all(action='DESELECT')

# get edges
vectors = []
arrow = []

axis = Vector((0, 0, 1))

for e in range(len(obj.data.edges)):
    edge = obj.data.edges[e]
    for i in range(2):
        edgeverts = edge.vertices[i]
        v = obj.data.vertices[edgeverts]
        co_final = obj.matrix_world @ v.co
        arrow.append(co_final)
    vectors.append(arrow)
    arrow = []
bpy.ops.object.select_all(action='DESELECT')

for p in range(len(vectors)):
    edgevec = vectors[p][1] - vectors[p][0]
    veclength = edgevec.length
    print(edgevec.length)

    rotation = axis.rotation_difference(edgevec)
    rot = axis.rotation_difference(edgevec).to_euler()

    edgevec = edgevec + vectors[p][0]    
    bpy.ops.mesh.primitive_cylinder_add(vertices=rodrez, radius=rodradius, depth=1, end_fill_type='NGON', calc_uvs=True,
                                    enter_editmode=True, location=(edgevec))
    bpy.ops.transform.translate(value=(0, 0, -0.5), orient_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, release_confirm=True, use_accurate=False)
    bpy.ops.object.editmode_toggle()
    
    obj = context.active_object
    bpy.ops.transform.resize(value=(1, 1, abs(veclength)))
    obj.rotation_euler = rot
    bpy.ops.object.select_all(action='TOGGLE')
