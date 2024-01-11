import math
import random
import sys
from pathlib import Path

import bpy

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
dset_dir = Path(argv[0])

def create_node_once(nodes, name, location=(0,0)):
    existing = nodes.get(name)
    if existing is not None:
        return existing
    new_node = nodes.new('ShaderNodeTexImage')
    new_node.name = name
    new_node.location = location
    return new_node

def load_map_image(node, img_path, name, colorspace="sRGB"):
    existing = bpy.data.images.get(name)
    if existing is not None:
         bpy.data.images.remove(existing)
    node.image = bpy.data.images.load(img_path)
    node.image.colorspace_settings.name = colorspace
    node.image.name = name

bpy.context.scene.render.image_settings.file_format = "PNG"

material = bpy.data.materials.get("BSDFPlane")

# Set node tree editing
material.use_nodes = True
nodes = material.node_tree.nodes

# Compositing nodes
scene = bpy.context.scene
scene.render.use_compositing = True

# Get output nodes
p_out = nodes['Principled Output']

# Get principled BSDF node
bsdf_node = nodes.get("Principled BSDF")

normal_map_node = nodes.get("Normal Map")
displacement_node = nodes.get("Displacement")
scale_node = nodes.get("Scale")

# Get background node
bg_node = bpy.data.worlds['World'].node_tree.nodes["Background"]

# Get camera
obj_camera = bpy.data.objects["Camera"]
# Get the camera data block
camera_data = obj_camera.data

for item_bc in [x for x in dset_dir.glob("**/basecolor.png")][:]:
    item = item_bc.parent
    
    if (item/"renders/passes").exists() and len(list(Path(item/"renders/passes").glob('*'))) == 10:
        continue

    # Clear orphan data
    bpy.ops.outliner.orphans_purge()

    # Set maps paths
    basecolor_path = str(item/"basecolor.png")
    normal_path = str(item/"normal.png")
    roughness_path = str(item/"roughness.png")
    metallic_path = str(item/"metallic.png")
    height_path = str(item/"displacement.png")

    # Setup nodes
    basecolor_node = nodes.get("Base Color")
    load_map_image(basecolor_node, basecolor_path, name="BaseColor")

    normal_node = nodes.get("Normal")
    load_map_image(normal_node, normal_path, name="Normal", colorspace="Non-Color")

    roughness_node = nodes.get("Roughness")
    load_map_image(roughness_node, roughness_path, name="Roughness", colorspace="Non-Color")

    metallic_node = nodes.get("Metallic")
    load_map_image(metallic_node, metallic_path, name="Metallic", colorspace="Non-Color")

    height_node = nodes.get("Height")
    load_map_image(height_node, height_path, name="Height", colorspace="Non-Color")

    scale_node = nodes.get("Scale")
    
    # Set render settings
    render_folder = item/"renders/passes"
    render_folder.mkdir(exist_ok=True, parents=True)

    for hdri_i in range(5):
        env_node = bpy.data.worlds['World'].node_tree.nodes[f"Env {hdri_i}"]
        bpy.data.worlds['World'].node_tree.links.new(env_node.outputs['Color'], bg_node.inputs['Color'])
        bpy.data.worlds['World'].node_tree.nodes[f"HDRIRotation"].outputs[0].default_value = random.random() * math.pi * 2

        for render_pass in ["diffuse", "glossy"]:
            if render_pass == "diffuse":
                scene.node_tree.nodes.active = scene.node_tree.nodes["DiffusePass"]
                scale_node.outputs[0].default_value = 1.0
                camera_data.type = 'ORTHO'
            elif render_pass == "glossy":
                scene.node_tree.nodes.active = scene.node_tree.nodes['GlossyPass']
                scale_node.outputs[0].default_value = 0.0
                camera_data.type = 'PERSP'

            # Render
            bpy.context.scene.render.filepath = str(render_folder/f"render_{hdri_i:02d}_{render_pass}.png")
            bpy.ops.render.render(write_still=True)


# Execution command: blender.exe -b .\render_ambient.blend -P .\render_ambient.py -- ..\maps