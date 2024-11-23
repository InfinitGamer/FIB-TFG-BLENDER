import bpy


class AddonPanel(bpy.types.Panel):
    bl_idname = "AddonPanel"
    bl_label = "Baking y Parametrización"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"

    def draw(self, context):
        layout = self.layout
