import bpy
class VerbosePanel(bpy.types.Panel):
    bl_idname = "VerbosePanel"
    bl_parent_id = "ParametrizationPanel"
    bl_label = "Verbose Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        parametrization_settings = scene.parametrization_settings
        
        layout = self.layout
        layout.prop(parametrization_settings, "verbose", text="verbose")