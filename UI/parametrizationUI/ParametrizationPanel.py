import bpy
class ParametrizationPanel(bpy.types.Panel):
    bl_idname = "ParametrizationPanel"
    bl_parent_id = "AddonPanel"
    bl_label = "Parametrization settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.operator("ui.parametrization_object", text="Parameterize")