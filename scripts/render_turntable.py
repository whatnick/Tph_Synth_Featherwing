import math
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
glb, out, frames, test = argv[0], argv[1], int(argv[2]), argv[3] == "test"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
bpy.context.view_layer.update()
roots = [o for o in bpy.context.scene.objects if o.parent is None]
orient = bpy.data.objects.new("Orient", None)
bpy.context.scene.collection.objects.link(orient)
for o in roots:
    o.parent = orient
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]

def bounds():
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    return (Vector(min(c[i] for c in pts) for i in range(3)),
            Vector(max(c[i] for c in pts) for i in range(3)))

lo, hi = bounds()
ext = hi - lo
thin = min(range(3), key=lambda i: ext[i])
if thin == 1:
    orient.rotation_euler[0] = -math.pi / 2
elif thin == 0:
    orient.rotation_euler[1] = -math.pi / 2
lo, hi = bounds()
center = (lo + hi) / 2
size = max(hi - lo)

pivot = bpy.data.objects.new("Pivot", None)
bpy.context.scene.collection.objects.link(pivot)
pivot.location = center
bpy.context.view_layer.update()
orient.parent = pivot
orient.matrix_parent_inverse = pivot.matrix_world.inverted()
up = 2
for mat in bpy.data.materials:
    if not mat.node_tree:
        continue
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            r_, g_, b_, a_ = n.inputs["Base Color"].default_value
            goldish = r_ > 0.6 and g_ > 0.5 and b_ < 0.1
            metalish = abs(r_ - g_) < 0.03 and abs(g_ - b_) < 0.1 and 0.55 < r_ < 0.8
            n.inputs["Metallic"].default_value = 0.9 if goldish else (0.6 if metalish else 0.0)
            n.inputs["Roughness"].default_value = 0.3 if (goldish or metalish) else 0.5
            if n.inputs["Alpha"].default_value < 1.0 or getattr(mat, "surface_render_method", "") == "BLENDED":
                n.inputs["Alpha"].default_value = 1.0
                if hasattr(mat, "surface_render_method"):
                    mat.surface_render_method = "DITHERED"
                if g_ > r_ and g_ > b_ and r_ < 0.15:
                    n.inputs["Base Color"].default_value = (0.02, 0.09, 0.05, 1.0)
                    n.inputs["Roughness"].default_value = 0.25
                elif r_ > 0.9 and g_ > 0.9:
                    n.inputs["Base Color"].default_value = (0.85, 0.85, 0.82, 1.0)

scene = bpy.context.scene
cam_data = bpy.data.cameras.new("Camera")
cam_data.lens = 50
cam = bpy.data.objects.new("Camera", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
dist = size * 2.4
if up == 2:
    cam.location = center + Vector((0, -dist * 0.85, dist * 0.55))
else:
    cam.location = center + Vector((0, dist * 0.55, dist * 0.85))
track = cam.constraints.new("TRACK_TO")
track.target = pivot
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
cam_data.clip_start = size / 100
cam_data.clip_end = size * 20

def light(name, kind, loc, energy, s=1.0):
    d = bpy.data.lights.new(name, kind)
    d.energy = energy
    if kind == "AREA":
        d.size = size * s
    o = bpy.data.objects.new(name, d)
    o.location = loc
    scene.collection.objects.link(o)
    c = o.constraints.new("TRACK_TO")
    c.target = pivot
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"

k = size ** 2
upv = Vector((0, 0, 1)) if up == 2 else Vector((0, 1, 0))
side = Vector((1, 0, 0))
light("Key", "AREA", center + (upv * 1.6 + side * 1.2 - Vector((0, 1, 0)) * (1 if up == 2 else 0)) * size, 300 * k, 1.5)
light("Fill", "AREA", center + (upv * 1.2 - side * 1.6) * size, 120 * k, 2.0)
light("Rim", "AREA", center + (-upv * 1.2 + side * 0.3) * size, 80 * k, 2.0)

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.03, 0.035, 0.045, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.6

axis = 2 if up == 2 else 1
pivot.rotation_mode = "XYZ"
scene.frame_start = 1
scene.frame_end = frames
pivot.rotation_euler[axis] = 0
pivot.keyframe_insert("rotation_euler", index=axis, frame=1)
pivot.rotation_euler[axis] = 2 * math.pi
pivot.keyframe_insert("rotation_euler", index=axis, frame=frames + 1)
action = pivot.animation_data.action
curves = getattr(action, "fcurves", None)
if curves is None:
    curves = [c for layer in action.layers for strip in layer.strips for bag in strip.channelbags for c in bag.fcurves]
for fc in curves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"

r = scene.render
for engine in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try:
        r.engine = engine
        break
    except TypeError:
        pass
r.resolution_x, r.resolution_y = 1280, 720
r.fps = 30
r.film_transparent = False
scene.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in scene.view_settings.bl_rna.properties["view_transform"].enum_items] else "Filmic"
if test:
    scene.frame_set(int(argv[4]) if len(argv) > 4 else 1)
    r.image_settings.file_format = "PNG"
    r.filepath = out
    bpy.ops.render.render(write_still=True)
else:
    if hasattr(r.image_settings, "media_type"):
        r.image_settings.media_type = "VIDEO"
    r.image_settings.file_format = "FFMPEG"
    r.ffmpeg.format = "MPEG4"
    r.ffmpeg.codec = "H264"
    r.ffmpeg.constant_rate_factor = "HIGH"
    r.filepath = out
    bpy.ops.render.render(animation=True)
print("DONE", out, "up-axis", up, "size", size)
