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
from .motions import batch_01

class ADEOLA_PT_motion_panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Adeola's Motions"
    bl_idname = "ADEOLA_PT_motion_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Adeola Motions'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Phase 1: Foundation")
        
        row = layout.row()
        row.operator("adeola.add_magnetic_cluster", text="Magnetic Cluster")
        
        row = layout.row()
        row.operator("adeola.add_jelly_bounce", text="Jelly Bounce")
        
        row = layout.row()
        row.operator("adeola.add_laser_scan", text="Laser Scan Reveal")

classes = (
    ADEOLA_PT_motion_panel,
    batch_01.ADEOLA_OT_add_magnetic_cluster,
    batch_01.ADEOLA_OT_add_jelly_bounce,
    batch_01.ADEOLA_OT_add_laser_scan,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
