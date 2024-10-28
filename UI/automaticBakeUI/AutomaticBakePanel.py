import bpy
class AutomaticBakePanel(bpy.types.Panel):
    bl_idname = "AutomaticBakePanel"
    bl_parent_id ="AddonPanel"
    bl_label = "Auto Bake Automatic Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"

    def draw(self, context):
        layout = self.layout
        