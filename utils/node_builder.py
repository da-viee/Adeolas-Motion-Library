import bpy

def get_or_create_node_group(name):
    """Gets an existing node group or creates a new one."""
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    
    group = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    
    # Create default input and output nodes
    group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    
    input_node = group.nodes.new('NodeGroupInput')
    input_node.location = (-200, 0)
    
    output_node = group.nodes.new('NodeGroupOutput')
    output_node.location = (200, 0)
    
    # Link input to output by default
    group.links.new(input_node.outputs['Geometry'], output_node.inputs['Geometry'])
    
    return group

def apply_modifier_to_object(obj, group_name):
    """Applies a Geometry Nodes modifier to the object using the specified group."""
    
    objects_to_apply = [obj]
    
    # Check if the global "Apply to Children" property exists and is true
    if hasattr(bpy.context.scene, "adeola_apply_to_children") and bpy.context.scene.adeola_apply_to_children:
        def get_children_recursive(parent):
            children = []
            for child in parent.children:
                if child.type == 'MESH':
                    children.append(child)
                children.extend(get_children_recursive(child))
            return children
        objects_to_apply.extend(get_children_recursive(obj))
        
    for target_obj in objects_to_apply:
        if target_obj.type != 'MESH':
            continue
            
        modifier_name = group_name
        
        # Check if modifier already exists
        mod = target_obj.modifiers.get(modifier_name)
        if not mod:
            mod = target_obj.modifiers.new(name=modifier_name, type='NODES')
        
        # Assign the node group to the modifier
        if group_name in bpy.data.node_groups:
            mod.node_group = bpy.data.node_groups[group_name]
        else:
            print(f"Warning: Node group {group_name} not found.")

def clear_group(group):
    """Clears all nodes from a group except the input and output."""
    for node in group.nodes:
        if node.type not in {'GROUP_INPUT', 'GROUP_OUTPUT'}:
            group.nodes.remove(node)
