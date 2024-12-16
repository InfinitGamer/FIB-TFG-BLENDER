import bpy
class AnalyzePanel(bpy.types.Panel):
    bl_idname = "AnalyzePanel"
    bl_parent_id = "AddonPanel"
    bl_label = "Analyze Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        layout.operator("ui.analyze_button",text="Analyze")
        