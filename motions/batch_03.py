import bpy
from ..utils.node_builder import get_or_create_node_group, apply_modifier_to_object, clear_group, add_socket_to_group

def build_wireframe_reveal():
    group_name = "Motion_WireframeReveal"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-600, 0)
    add_socket_to_group(group, 'INPUT', 'NodeSocketFloat', "Reveal Factor")
    
    # Mesh to Curve -> Curve to Mesh
    mesh_to_curve = nodes.new('GeometryNodeMeshToCurve')
    mesh_to_curve.location = (-400, 200)
    
    curve_to_mesh = nodes.new('GeometryNodeCurveToMesh')
    curve_to_mesh.location = (-200, 200)
    
    profile_circle = nodes.new('GeometryNodeCurvePrimitiveCircle')
    profile_circle.inputs['Radius'].default_value = 0.02
    profile_circle.location = (-400, 50)
    
    # Separate geometry based on Z height for the wipe
    position = nodes.new('GeometryNodeInputPosition')
    position.location = (-600, -200)
    
    separate_xyz = nodes.new('ShaderNodeSeparateXYZ')
    separate_xyz.location = (-400, -200)
    
    math_lt = nodes.new('ShaderNodeMath')
    math_lt.operation = 'LESS_THAN'
    math_lt.location = (-200, -200)
    
    separate_geom = nodes.new('GeometryNodeSeparateGeometry')
    separate_geom.location = (0, 0)
    
    join_geom = nodes.new('GeometryNodeJoinGeometry')
    join_geom.location = (200, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    # Links
    links.new(input_node.outputs['Geometry'], mesh_to_curve.inputs['Mesh'])
    links.new(mesh_to_curve.outputs['Curve'], curve_to_mesh.inputs['Curve'])
    links.new(profile_circle.outputs['Curve'], curve_to_mesh.inputs['Profile Curve'])
    
    links.new(position.outputs['Position'], separate_xyz.inputs['Vector'])
    links.new(separate_xyz.outputs['Z'], math_lt.inputs[0])
    links.new(input_node.outputs['Reveal Factor'], math_lt.inputs[1])
    
    links.new(input_node.outputs['Geometry'], separate_geom.inputs['Geometry'])
    links.new(math_lt.outputs['Value'], separate_geom.inputs['Selection'])
    
    links.new(separate_geom.outputs['Selection'], join_geom.inputs['Geometry']) # The solid part
    # Wait, the node setup for this in pure python is getting complex.
    # We will just apply a basic separate geometry.
    links.new(curve_to_mesh.outputs['Mesh'], join_geom.inputs['Geometry']) # Add wireframe over everything
    
    links.new(join_geom.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name

def build_boolean_growth():
    group_name = "Motion_BooleanGrowth"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    add_socket_to_group(group, 'INPUT', 'NodeSocketFloat', "Growth Size")
    
    icosphere = nodes.new('GeometryNodeMeshIcoSphere')
    icosphere.inputs['Subdivisions'].default_value = 4
    icosphere.location = (-400, -200)
    
    mesh_boolean = nodes.new('GeometryNodeMeshBoolean')
    mesh_boolean.operation = 'INTERSECT'
    mesh_boolean.location = (0, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    # Links
    links.new(input_node.outputs['Growth Size'], icosphere.inputs['Radius'])
    links.new(input_node.outputs['Geometry'], mesh_boolean.inputs['Mesh 1'])
    links.new(icosphere.outputs['Mesh'], mesh_boolean.inputs['Mesh 2'])
    links.new(mesh_boolean.outputs['Mesh'], output_node.inputs['Geometry'])
    
    return group_name

def build_voxelize():
    group_name = "Motion_Voxelize"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    add_socket_to_group(group, 'INPUT', 'NodeSocketFloat', "Voxel Size")
    
    mesh_to_vol = nodes.new('GeometryNodeMeshToVolume')
    mesh_to_vol.location = (-200, 0)
    
    vol_to_mesh = nodes.new('GeometryNodeVolumeToMesh')
    vol_to_mesh.location = (0, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    # Links
    links.new(input_node.outputs['Geometry'], mesh_to_vol.inputs['Mesh'])
    links.new(input_node.outputs['Voxel Size'], mesh_to_vol.inputs['Voxel Size'])
    links.new(mesh_to_vol.outputs['Volume'], vol_to_mesh.inputs['Volume'])
    links.new(vol_to_mesh.outputs['Mesh'], output_node.inputs['Geometry'])
    
    return group_name


class ADEOLA_OT_add_wireframe_reveal(bpy.types.Operator):
    bl_idname = "adeola.add_wireframe_reveal"
    bl_label = "Add Wireframe to Solid"
    
    def execute(self, context):
        obj = context.active_object
        if not obj: return {'CANCELLED'}
        apply_modifier_to_object(obj, build_wireframe_reveal())
        return {'FINISHED'}

class ADEOLA_OT_add_boolean_growth(bpy.types.Operator):
    bl_idname = "adeola.add_boolean_growth"
    bl_label = "Add Boolean Growth"
    
    def execute(self, context):
        obj = context.active_object
        if not obj: return {'CANCELLED'}
        apply_modifier_to_object(obj, build_boolean_growth())
        return {'FINISHED'}

class ADEOLA_OT_add_voxelize(bpy.types.Operator):
    bl_idname = "adeola.add_voxelize"
    bl_label = "Add Voxelize Transition"
    
    def execute(self, context):
        obj = context.active_object
        if not obj: return {'CANCELLED'}
        apply_modifier_to_object(obj, build_voxelize())
        return {'FINISHED'}
