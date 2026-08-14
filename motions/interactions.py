import bpy
from ..utils.node_builder import get_or_create_node_group, apply_modifier_to_object, clear_group

def build_morph_interaction():
    group_name = "Motion_Morph_A_to_B"
    group = get_or_create_node_group(group_name)
    clear_group(group)
    
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-600, 0)
    
    # Expose the Target Object (B) to the modifier panel
    group.interface.new_socket(name="Target Object", in_out='INPUT', socket_type='NodeSocketObject')
    group.interface.new_socket(name="Morph Factor", in_out='INPUT', socket_type='NodeSocketFloat')
    
    # Object Info node to get Target B's geometry
    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.location = (-400, -200)
    obj_info.transform_space = 'RELATIVE'
    
    # Sample Nearest Surface to blend the positions
    sample_nearest = nodes.new('GeometryNodeSampleNearestSurface')
    sample_nearest.location = (-200, -200)
    
    # Mix node to interpolate between A and B
    mix_node = nodes.new('ShaderNodeMix')
    mix_node.data_type = 'VECTOR'
    mix_node.location = (0, -100)
    
    # Set Position node to move A's vertices to B's surface
    set_pos = nodes.new('GeometryNodeSetPosition')
    set_pos.location = (200, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)
    
    # Links
    links.new(input_node.outputs['Target Object'], obj_info.inputs['Object'])
    links.new(obj_info.outputs['Geometry'], sample_nearest.inputs['Mesh'])
    
    # Mix between original position and target position
    position_node = nodes.new('GeometryNodeInputPosition')
    position_node.location = (-200, 0)
    
    links.new(input_node.outputs['Morph Factor'], mix_node.inputs['Factor'])
    links.new(position_node.outputs['Position'], mix_node.inputs[4]) # A
    links.new(sample_nearest.outputs['Position'], mix_node.inputs[5]) # B
    
    links.new(mix_node.outputs[1], set_pos.inputs['Position'])
    links.new(input_node.outputs['Geometry'], set_pos.inputs['Geometry'])
    links.new(set_pos.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group_name


class ADEOLA_OT_add_morph_interaction(bpy.types.Operator):
    bl_idname = "adeola.add_morph_interaction"
    bl_label = "Add Morph A to B"
    
    def execute(self, context):
        scene = context.scene
        source_obj = scene.adeola_source_obj
        target_obj = scene.adeola_target_obj
        
        if not source_obj or not target_obj:
            self.report({'WARNING'}, "Please select both Source (A) and Target (B) objects in the panel.")
            return {'CANCELLED'}
        
        group_name = build_morph_interaction()
        
        # Apply modifier to Source Object (A)
        apply_modifier_to_object(source_obj, group_name)
        
        # Set the target object in the modifier's properties
        mod = source_obj.modifiers.get(group_name)
        if mod:
            # Depending on Blender version, input socket names can be accessed like this:
            try:
                mod["Socket_1"] = target_obj # Often the first custom input after Geometry
            except:
                pass
                
        self.report({'INFO'}, f"Morph effect added to {source_obj.name}, targeting {target_obj.name}")
        return {'FINISHED'}
