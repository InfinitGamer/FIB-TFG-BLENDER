import bpy
class ManualBakePanel(bpy.types.Panel):
    bl_idname = "ManualBakePanel"
    bl_parent_id ="AddonPanel"
    bl_label = "Auto Bake Manual Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {'DEFAULT_CLOSED'} 
    def draw(self, context):
        layout = self.layout
        layout.operator("ui.bake_object",text="Bake")
        