bl_info = {
    "name": "Adeola's Motion Library",
    "author": "Adeola & Antigravity",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Adeola Motions",
    "description": "Procedural Geometry Nodes motion library.",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
from .motions import batch_01, batch_02, batch_03, interactions

class ADEOLA_PT_motion_panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Adeola's Motions"
    bl_idname = "ADEOLA_PT_motion_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Adeola Motions'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Global Settings
        layout.prop(scene, "adeola_apply_to_children")
        layout.separator()

        layout.label(text="Phase 1: Foundation")
        
        row = layout.row()
        row.operator("adeola.add_magnetic_cluster", text="Magnetic Cluster")
        
        row = layout.row()
        row.operator("adeola.add_jelly_bounce", text="Jelly Bounce")
        
        row = layout.row()
        row.operator("adeola.add_laser_scan", text="Laser Scan Reveal")
        
        layout.separator()
        layout.label(text="Phase 2: Physics & Layout")
        
        row = layout.row()
        row.operator("adeola.add_deflation", text="Deflation / Inflation")
        
        row = layout.row()
        row.operator("adeola.add_squash_stretch", text="Squash & Stretch")
        
        row = layout.row()
        row.operator("adeola.add_hex_ripple", text="Hex-Grid Ripple")
        
        layout.separator()
        layout.label(text="Phase 3: Slice, Dice & Reveal")
        
        row = layout.row()
        row.operator("adeola.add_wireframe_reveal", text="Wireframe to Solid")
        
        row = layout.row()
        row.operator("adeola.add_boolean_growth", text="Boolean Growth")
        
        row = layout.row()
        row.operator("adeola.add_voxelize", text="Voxelize Transition")
        
        layout.separator()
        layout.label(text="Phase 4: Interactions")
        
        box = layout.box()
        box.prop(scene, "adeola_source_obj", text="Source (A)")
        box.prop(scene, "adeola_target_obj", text="Target (B)")
        
        row = box.row()
        row.operator("adeola.add_morph_interaction", text="Morph A to B")

classes = (
    ADEOLA_PT_motion_panel,
    batch_01.ADEOLA_OT_add_magnetic_cluster,
    batch_01.ADEOLA_OT_add_jelly_bounce,
    batch_01.ADEOLA_OT_add_laser_scan,
    batch_02.ADEOLA_OT_add_deflation,
    batch_02.ADEOLA_OT_add_squash_stretch,
    batch_02.ADEOLA_OT_add_hex_ripple,
    batch_03.ADEOLA_OT_add_wireframe_reveal,
    batch_03.ADEOLA_OT_add_boolean_growth,
    batch_03.ADEOLA_OT_add_voxelize,
    interactions.ADEOLA_OT_add_morph_interaction,
)

def register():
    bpy.types.Scene.adeola_source_obj = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.adeola_target_obj = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.adeola_apply_to_children = bpy.props.BoolProperty(
        name="Apply to Children",
        description="If checked, applying a motion will also apply it to all mesh children of the selected object",
        default=False
    )
    
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    del bpy.types.Scene.adeola_source_obj
    del bpy.types.Scene.adeola_target_obj
    del bpy.types.Scene.adeola_apply_to_children
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
