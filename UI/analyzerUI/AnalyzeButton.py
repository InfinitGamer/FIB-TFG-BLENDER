import bpy
class AnalyzeButton(bpy.types.Operator):
    bl_idname = "ui.analyze_button"
    bl_label = "Analyze button"
    bl_options = {"REGISTER"}


    def execute(self, context):
        analyzer_settings = context.scene.analyzer_settings
        bpy.ops.uv.analyze(type=analyzer_settings.type, path=analyzer_settings.path)
        return {"FINISHED"}
