import bpy
from ..utils.node_builder import get_or_create_node_group, apply_modifier_to_object, clear_group

def create_text_asset(name, build_func):
    """Helper to create a new Text object and apply a node group to it."""
    # Create a text curve
    curve = bpy.data.curves.new(type="FONT", name="TextData")
    curve.body = "ADEOLA"
    obj = bpy.data.objects.new(name, curve)
    bpy.context.scene.collection.objects.link(obj)
    
    # Make active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Apply modifier
    group_name = build_func()
    apply_modifier_to_object(obj, group_name)
    return obj

def build_typewriter():
    group_name = "Text_Typewriter"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    string_to_curves = nodes.new('GeometryNodeStringToCurves')
    string_to_curves.location = (-200, 0)
    
    slice_curve = nodes.new('GeometryNodeCurveEndpointSelection')
    slice_curve.location = (0, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(string_to_curves.outputs['Curve Instances'], output_node.inputs['Geometry'])
    return group_name

def build_extrusion_pop():
    group_name = "Text_ExtrusionPop"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    extrude = nodes.new('GeometryNodeExtrudeMesh')
    extrude.location = (0, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-200, 0)
    
    links.new(input_node.outputs['Geometry'], extrude.inputs['Mesh'])
    links.new(extrude.outputs['Mesh'], output_node.inputs['Geometry'])
    return group_name

def build_wavy_text():
    group_name = "Text_Wavy"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    set_pos = nodes.new('GeometryNodeSetPosition')
    set_pos.location = (0, 0)
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-200, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(input_node.outputs['Geometry'], set_pos.inputs['Geometry'])
    links.new(set_pos.outputs['Geometry'], output_node.inputs['Geometry'])
    return group_name

def build_jiggle_text():
    group_name = "Text_Jiggle"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-200, 0)
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(input_node.outputs['Geometry'], output_node.inputs['Geometry'])
    return group_name

def build_glitch_slice():
    group_name = "Text_GlitchSlice"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-200, 0)
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(input_node.outputs['Geometry'], output_node.inputs['Geometry'])
    return group_name


class ADEOLA_OT_add_typewriter(bpy.types.Operator):
    bl_idname = "adeola.add_typewriter"
    bl_label = "Add Typewriter Reveal"
    def execute(self, context):
        create_text_asset("Text_Typewriter", build_typewriter)
        return {'FINISHED'}

class ADEOLA_OT_add_extrusion_pop(bpy.types.Operator):
    bl_idname = "adeola.add_extrusion_pop"
    bl_label = "Add Extrusion Pop"
    def execute(self, context):
        create_text_asset("Text_ExtrusionPop", build_extrusion_pop)
        return {'FINISHED'}

class ADEOLA_OT_add_wavy_text(bpy.types.Operator):
    bl_idname = "adeola.add_wavy_text"
    bl_label = "Add Wavy Text"
    def execute(self, context):
        create_text_asset("Text_WavyText", build_wavy_text)
        return {'FINISHED'}

class ADEOLA_OT_add_jiggle_text(bpy.types.Operator):
    bl_idname = "adeola.add_jiggle_text"
    bl_label = "Add Jiggle Physics Text"
    def execute(self, context):
        create_text_asset("Text_JiggleText", build_jiggle_text)
        return {'FINISHED'}

class ADEOLA_OT_add_glitch_slice(bpy.types.Operator):
    bl_idname = "adeola.add_glitch_slice"
    bl_label = "Add Glitch Slice Text"
    def execute(self, context):
        create_text_asset("Text_GlitchSlice", build_glitch_slice)
        return {'FINISHED'}
