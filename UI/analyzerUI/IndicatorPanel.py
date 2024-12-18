import bpy
class IndicatorPanel(bpy.types.Panel):
    bl_idname = "IndicatorPanel"
    bl_parent_id = "AnalyzePanel"
    bl_label = "Indicator Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        analyzer_settings = context.scene.analyzer_settings
        layout.prop(analyzer_settings,"type", text="Indicator method")

        if analyzer_settings.type == "RATIODISTORTED":
            row = layout.row(align=True)
            row.prop(analyzer_settings,"path", text="Path")
            row.operator("ui.file_selector", text="", icon="FILE_FOLDER")

    