import bpy
from ..utils.node_builder import get_or_create_node_group, apply_modifier_to_object, clear_group

def build_deflation():
    group_name = "Motion_Deflation"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-600, 0)
    
    # Time based ping-pong scale
    transform = nodes.new('GeometryNodeTransform')
    transform.location = (0, 0)
    
    scene_time = nodes.new('GeometryNodeInputSceneTime')
    scene_time.location = (-600, -200)
    
    math_pingpong = nodes.new('ShaderNodeMath')
    math_pingpong.operation = 'PINGPONG'
    math_pingpong.inputs[1].default_value = 1.0
    math_pingpong.location = (-400, -200)
    
    # Map from [0, 1] to [0.2, 1.0] so it doesn't scale to 0
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.inputs[3].default_value = 0.2
    map_range.inputs[4].default_value = 1.0
    map_range.location = (-200, -200)
    
    combine_xyz = nodes.new('ShaderNodeCombineXYZ')
    combine_xyz.location = (0, -200)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    # Links
    links.new(scene_time.outputs['Seconds'], math_pingpong.inputs[0])
    links.new(math_pingpong.outputs['Value'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], combine_xyz.inputs['X'])
    links.new(map_range.outputs['Result'], combine_xyz.inputs['Y'])
    links.new(map_range.outputs['Result'], combine_xyz.inputs['Z'])
    links.new(combine_xyz.outputs['Vector'], transform.inputs['Scale'])
    
    links.new(input_node.outputs['Geometry'], transform.inputs['Geometry'])
    links.new(transform.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name

def build_squash_stretch():
    group_name = "Motion_SquashStretch"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    group.interface.new_socket(name="Squash Factor", in_out='INPUT', socket_type='NodeSocketFloat')
    # Default value for the socket in newer blender versions is set slightly differently, but we'll let it default to 0.0
    
    transform = nodes.new('GeometryNodeTransform')
    transform.location = (200, 0)
    
    # Math: Z scale = 1.0 + Factor, X/Y scale = 1.0 / (1.0 + Factor)
    math_add = nodes.new('ShaderNodeMath')
    math_add.operation = 'ADD'
    math_add.inputs[0].default_value = 1.0
    math_add.location = (-200, -100)
    
    math_div = nodes.new('ShaderNodeMath')
    math_div.operation = 'DIVIDE'
    math_div.inputs[0].default_value = 1.0
    math_div.location = (-200, -300)
    
    combine_xyz = nodes.new('ShaderNodeCombineXYZ')
    combine_xyz.location = (0, -200)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    # Links
    links.new(input_node.outputs['Squash Factor'], math_add.inputs[1])
    links.new(math_add.outputs['Value'], math_div.inputs[1])
    links.new(math_add.outputs['Value'], combine_xyz.inputs['Z'])
    links.new(math_div.outputs['Value'], combine_xyz.inputs['X'])
    links.new(math_div.outputs['Value'], combine_xyz.inputs['Y'])
    
    links.new(combine_xyz.outputs['Vector'], transform.inputs['Scale'])
    links.new(input_node.outputs['Geometry'], transform.inputs['Geometry'])
    links.new(transform.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name

def build_hex_ripple():
    group_name = "Motion_HexRipple"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-600, 0)
    
    set_pos = nodes.new('GeometryNodeSetPosition')
    set_pos.location = (200, 0)
    
    # Distance from center
    position = nodes.new('GeometryNodeInputPosition')
    position.location = (-600, -200)
    
    vector_math = nodes.new('ShaderNodeVectorMath')
    vector_math.operation = 'LENGTH'
    vector_math.location = (-400, -200)
    
    scene_time = nodes.new('GeometryNodeInputSceneTime')
    scene_time.location = (-600, -400)
    
    # (Distance - Time) * Speed
    math_sub = nodes.new('ShaderNodeMath')
    math_sub.operation = 'SUBTRACT'
    math_sub.location = (-200, -200)
    
    math_sine = nodes.new('ShaderNodeMath')
    math_sine.operation = 'SINE'
    math_sine.location = (0, -200)
    
    combine_xyz = nodes.new('ShaderNodeCombineXYZ')
    combine_xyz.location = (200, -200)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    # Links
    links.new(position.outputs['Position'], vector_math.inputs[0])
    links.new(vector_math.outputs['Value'], math_sub.inputs[0])
    links.new(scene_time.outputs['Seconds'], math_sub.inputs[1])
    links.new(math_sub.outputs['Value'], math_sine.inputs[0])
    links.new(math_sine.outputs['Value'], combine_xyz.inputs['Z'])
    
    links.new(combine_xyz.outputs['Vector'], set_pos.inputs['Offset'])
    links.new(input_node.outputs['Geometry'], set_pos.inputs['Geometry'])
    links.new(set_pos.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name


class ADEOLA_OT_add_deflation(bpy.types.Operator):
    bl_idname = "adeola.add_deflation"
    bl_label = "Add Deflation"
    
    def execute(self, context):
        obj = context.active_object
        if not obj:
            return {'CANCELLED'}
        apply_modifier_to_object(obj, build_deflation())
        return {'FINISHED'}

class ADEOLA_OT_add_squash_stretch(bpy.types.Operator):
    bl_idname = "adeola.add_squash_stretch"
    bl_label = "Add Squash & Stretch"
    
    def execute(self, context):
        obj = context.active_object
        if not obj:
            return {'CANCELLED'}
        apply_modifier_to_object(obj, build_squash_stretch())
        return {'FINISHED'}

class ADEOLA_OT_add_hex_ripple(bpy.types.Operator):
    bl_idname = "adeola.add_hex_ripple"
    bl_label = "Add Hex-Grid Ripple"
    
    def execute(self, context):
        obj = context.active_object
        if not obj:
            return {'CANCELLED'}
        apply_modifier_to_object(obj, build_hex_ripple())
        return {'FINISHED'}
