import bpy 
class DevicePanel(bpy.types.Panel):
    bl_idname = "DevicePanel"
    bl_label = "Device"
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
        #eleccion del device
        device_settings = layout.row()
        device_settings.prop(autobake_settings,"device",text="Device")
        