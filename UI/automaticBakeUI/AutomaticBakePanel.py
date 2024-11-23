import bpy


class AutomaticBakePanel(bpy.types.Panel):
    bl_idname = "AutomaticBakePanel"
    bl_parent_id = "AddonPanel"
    bl_label = "Bake Automatic Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.operator("ui.bake_object", text="Bake")
