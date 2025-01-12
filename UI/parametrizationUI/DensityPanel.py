import bpy
class DensityPanel(bpy.types.Panel):
    bl_idname = "DensityPanel"
    bl_parent_id = "ParametrizationPanel"
    bl_label = "Density settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        scene = context.scene
        parametrization_settings = scene.parametrization_settings

        layout = self.layout
        margin = layout.row()
        
        split = margin.split(factor=0.25)
        split.label(text="Density:")
        split.prop(parametrization_settings, "density", text="", )

        row2 = layout.row()
        row2.label(text="Tooltip: The density is expressed in points/u^2")
        