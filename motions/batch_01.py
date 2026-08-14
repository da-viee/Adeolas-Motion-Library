import bpy
from ..utils.node_builder import get_or_create_node_group, apply_modifier_to_object, clear_group

def build_magnetic_cluster():
    group_name = "Motion_MagneticCluster"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    # Input
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    # Example placeholder for Magnetic Cluster logic
    # In reality, this would involve Set Position, Vector Math (Distance), and a Target Object
    transform_node = nodes.new('GeometryNodeTransform')
    transform_node.location = (0, 0)
    
    # Output
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    # Link
    links.new(input_node.outputs['Geometry'], transform_node.inputs['Geometry'])
    links.new(transform_node.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name

def build_jelly_bounce():
    group_name = "Motion_JellyBounce"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    # Placeholder for Simulation Zone or complex math
    set_pos_node = nodes.new('GeometryNodeSetPosition')
    set_pos_node.location = (0, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    links.new(input_node.outputs['Geometry'], set_pos_node.inputs['Geometry'])
    links.new(set_pos_node.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name

def build_laser_scan():
    group_name = "Motion_LaserScanReveal"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    # Placeholder for Boolean math or Delete Geometry
    delete_geom_node = nodes.new('GeometryNodeDeleteGeometry')
    delete_geom_node.location = (0, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    links.new(input_node.outputs['Geometry'], delete_geom_node.inputs['Geometry'])
    links.new(delete_geom_node.outputs['Geometry'], output_node.inputs['Geometry'])
    
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
