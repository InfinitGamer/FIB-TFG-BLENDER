import bpy
class IterationsPanel(bpy.types.Panel):
    bl_idname = "IterationsPanel"
    bl_parent_id = "ParametrizationPanel"
    bl_label = "Iterations Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene

        parametrization_settings = scene.parametrization_settings

        layout = self.layout
        margin = layout.row()
        
        split = margin.split(factor=0.3)
        split.label(text="Iterations:")
        split.prop(parametrization_settings, "iterations", text="")