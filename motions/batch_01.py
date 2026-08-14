import bpy
from ..utils.node_builder import get_or_create_node_group, apply_modifier_to_object, clear_group

def build_magnetic_cluster():
    group_name = "Motion_MagneticCluster"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    # Random Scale to simulate clustering effect
    transform = nodes.new('GeometryNodeTransform')
    transform.location = (0, 0)
    
    random_val = nodes.new('FunctionNodeRandomValue')
    random_val.location = (-200, -100)
    random_val.data_type = 'FLOAT'
    random_val.inputs[2].default_value = 0.5  # Min
    random_val.inputs[3].default_value = 1.5  # Max
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    # Links
    links.new(random_val.outputs['Value'], transform.inputs['Scale'])
    links.new(input_node.outputs['Geometry'], transform.inputs['Geometry'])
    links.new(transform.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name

def build_jelly_bounce():
    group_name = "Motion_JellyBounce"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    # Time based sine wave bobbing (Jelly Bounce)
    set_pos = nodes.new('GeometryNodeSetPosition')
    set_pos.location = (0, 0)
    
    scene_time = nodes.new('GeometryNodeInputSceneTime')
    scene_time.location = (-400, -200)
    
    math_sine = nodes.new('ShaderNodeMath')
    math_sine.operation = 'SINE'
    math_sine.location = (-200, -200)
    
    math_mult = nodes.new('ShaderNodeMath')
    math_mult.operation = 'MULTIPLY'
    math_mult.inputs[1].default_value = 2.0  # Speed
    math_mult.location = (-400, -400)
    
    combine_xyz = nodes.new('ShaderNodeCombineXYZ')
    combine_xyz.location = (-200, -400)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    # Links
    links.new(scene_time.outputs['Seconds'], math_mult.inputs[0])
    links.new(math_mult.outputs['Value'], math_sine.inputs[0])
    links.new(math_sine.outputs['Value'], combine_xyz.inputs['Z'])
    links.new(combine_xyz.outputs['Vector'], set_pos.inputs['Offset'])
    links.new(input_node.outputs['Geometry'], set_pos.inputs['Geometry'])
    links.new(set_pos.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name

def build_laser_scan():
    group_name = "Motion_LaserScanReveal"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-600, 0)
    
    # Delete geometry based on Z height (Laser Scan)
    delete_geom = nodes.new('GeometryNodeDeleteGeometry')
    delete_geom.location = (0, 0)
    
    position = nodes.new('GeometryNodeInputPosition')
    position.location = (-600, -200)
    
    separate_xyz = nodes.new('ShaderNodeSeparateXYZ')
    separate_xyz.location = (-400, -200)
    
    math_gt = nodes.new('ShaderNodeMath')
    math_gt.operation = 'GREATER_THAN'
    math_gt.inputs[1].default_value = 0.0  # Cutoff height
    math_gt.location = (-200, -200)
    
    # Expose the cutoff height to the modifier panel
    group.interface.new_socket(name="Scan Height", in_out='INPUT', socket_type='NodeSocketFloat')
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    # Links
    links.new(position.outputs['Position'], separate_xyz.inputs['Vector'])
    links.new(separate_xyz.outputs['Z'], math_gt.inputs[0])
    links.new(input_node.outputs['Scan Height'], math_gt.inputs[1])
    links.new(math_gt.outputs['Value'], delete_geom.inputs['Selection'])
    links.new(input_node.outputs['Geometry'], delete_geom.inputs['Geometry'])
    links.new(delete_geom.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name


class ADEOLA_OT_add_magnetic_cluster(bpy.types.Operator):
    bl_idname = "adeola.add_magnetic_cluster"
    bl_label = "Add Magnetic Cluster"
    
    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        group_name = build_magnetic_cluster()
        apply_modifier_to_object(obj, group_name)
        return {'FINISHED'}

class ADEOLA_OT_add_jelly_bounce(bpy.types.Operator):
    bl_idname = "adeola.add_jelly_bounce"
    bl_label = "Add Jelly Bounce"
    
    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        group_name = build_jelly_bounce()
        apply_modifier_to_object(obj, group_name)
        return {'FINISHED'}

class ADEOLA_OT_add_laser_scan(bpy.types.Operator):
    bl_idname = "adeola.add_laser_scan"
    bl_label = "Add Laser Scan Reveal"
    
    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        group_name = build_laser_scan()
        apply_modifier_to_object(obj, group_name)
        return {'FINISHED'}
