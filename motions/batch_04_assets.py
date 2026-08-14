import bpy
from ..utils.node_builder import get_or_create_node_group, apply_modifier_to_object, clear_group

def create_vfx_asset(name, build_func):
    """Helper to create a new mesh object and apply a VFX node group to it."""
    # Create a simple plane as the base for the VFX
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    obj = bpy.context.active_object
    obj.name = name
    
    # Generate the nodes and apply
    group_name = build_func()
    apply_modifier_to_object(obj, group_name)
    return obj

def build_crown_splash():
    group_name = "Asset_CrownSplash"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    # Placeholder: Generates a Cylinder that scales up and flares out
    cylinder = nodes.new('GeometryNodeMeshCylinder')
    cylinder.location = (-200, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(cylinder.outputs['Mesh'], output_node.inputs['Geometry'])
    return group_name

def build_confetti_cannon():
    group_name = "Asset_ConfettiCannon"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    # Placeholder: Distribute points on the plane and instance small planes
    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.location = (-200, 0)
    
    instance = nodes.new('GeometryNodeInstanceOnPoints')
    instance.location = (0, 0)
    
    confetti_piece = nodes.new('GeometryNodeMeshGrid')
    confetti_piece.inputs['Size X'].default_value = 0.05
    confetti_piece.inputs['Size Y'].default_value = 0.02
    confetti_piece.location = (-200, -200)
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(input_node.outputs['Geometry'], distribute.inputs['Mesh'])
    links.new(distribute.outputs['Points'], instance.inputs['Points'])
    links.new(confetti_piece.outputs['Mesh'], instance.inputs['Instance'])
    links.new(instance.outputs['Instances'], output_node.inputs['Geometry'])
    return group_name

def build_dust_poof():
    group_name = "Asset_DustPoof"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    ico = nodes.new('GeometryNodeMeshIcoSphere')
    ico.location = (-200, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(ico.outputs['Mesh'], output_node.inputs['Geometry'])
    return group_name

def build_impact_debris():
    group_name = "Asset_ImpactDebris"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    cube = nodes.new('GeometryNodeMeshCube')
    cube.location = (-200, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(cube.outputs['Mesh'], output_node.inputs['Geometry'])
    return group_name

def build_speed_lines():
    group_name = "Asset_SpeedLines"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    nodes = group.nodes
    links = group.links
    
    line = nodes.new('GeometryNodeCurvePrimitiveLine')
    line.location = (-200, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    links.new(line.outputs['Curve'], output_node.inputs['Geometry'])
    return group_name

class ADEOLA_OT_add_crown_splash(bpy.types.Operator):
    bl_idname = "adeola.add_crown_splash"
    bl_label = "Add Crown Splash VFX"
    def execute(self, context):
        create_vfx_asset("VFX_CrownSplash", build_crown_splash)
        return {'FINISHED'}

class ADEOLA_OT_add_confetti(bpy.types.Operator):
    bl_idname = "adeola.add_confetti"
    bl_label = "Add Confetti Cannon VFX"
    def execute(self, context):
        create_vfx_asset("VFX_Confetti", build_confetti_cannon)
        return {'FINISHED'}

class ADEOLA_OT_add_dust_poof(bpy.types.Operator):
    bl_idname = "adeola.add_dust_poof"
    bl_label = "Add Dust Poof VFX"
    def execute(self, context):
        create_vfx_asset("VFX_DustPoof", build_dust_poof)
        return {'FINISHED'}

class ADEOLA_OT_add_impact_debris(bpy.types.Operator):
    bl_idname = "adeola.add_impact_debris"
    bl_label = "Add Impact Debris VFX"
    def execute(self, context):
        create_vfx_asset("VFX_ImpactDebris", build_impact_debris)
        return {'FINISHED'}

class ADEOLA_OT_add_speed_lines(bpy.types.Operator):
    bl_idname = "adeola.add_speed_lines"
    bl_label = "Add Speed Lines VFX"
    def execute(self, context):
        create_vfx_asset("VFX_SpeedLines", build_speed_lines)
        return {'FINISHED'}
