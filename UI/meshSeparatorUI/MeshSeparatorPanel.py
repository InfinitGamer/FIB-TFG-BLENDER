import bpy

class MeshSeparatorPanel(bpy.types.Panel):
    bl_idname = "MeshSeparatorPanel"
    bl_parent_id = "AddonPanel"
    bl_label = "Mesh Separator Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        layout = self.layout
        layout.operator("ui.mesh_separator", text="Separate")
        