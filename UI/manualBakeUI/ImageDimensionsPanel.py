import bpy
class ImageDimensionsPanel(bpy.types.Panel):
    bl_idname = "ImageDimensionsPanel"
    bl_label = "Image Dimensions"
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
    
        width_settings = layout.row()
        width_settings.prop(autobake_settings,"width",text="Width")
        
        height_settings = layout.row()
        height_settings.prop(autobake_settings,"height",text="Height")
        
    