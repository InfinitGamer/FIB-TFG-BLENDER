import bpy
class MarginPanel(bpy.types.Panel):
    bl_idname = "MarginPanel"
    bl_label = "Margin"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_parent_id ="ManualBakePanel"

    def draw(self, context):
        layout = self.layout
        
        #cogemos la escena actual
        scene = context.scene
        
        #cogemos los settings del autobake
        autobake_settings = scene.autobake_settings
    
        #seleccion del margin
        margin_type = layout.row()
        margin_type.prop(autobake_settings,"margin_type", text="Margin Type")

        margin = layout.row()
        margin.prop(autobake_settings,"margin", text="Margin")