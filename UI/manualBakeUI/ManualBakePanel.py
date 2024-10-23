import bpy
class ManualBakePanel(bpy.types.Panel):
    bl_idname = "ManualBakePanel"
    bl_parent_id ="AddonPanel"
    bl_label = "Auto Bake Manual Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"

    def draw(self, context):
        layout = self.layout
        
        #cogemos la escena actual
        scene = context.scene
        
        #cogemos los settings del autobake
        autobake_settings = scene.autobake_settings
        
        #cogemos los elementos para la UI de bake
        UIbake_settings = scene.UIbake_settings

        #creamos selector del tipo del bake
        property_settings = layout.row()
        property_settings.prop(autobake_settings,"bake_type", text="Bake Type")
        
        #creamos lista de objetos
        column_object_list = layout.column()
        
        column_object_list.template_list("ObjectList", "", autobake_settings, "objects", UIbake_settings, "object_index")
        
        column_object_list.operator("ui.add_object", text="Add Selected Objects")
        column_object_list.operator("ui.delete_object", text="Delete Selected Object")

        device_settings = layout.row()
        
        device_settings.prop(autobake_settings,"device",text="Device")

        width_settings = layout.row()
        width_settings.prop(autobake_settings,"width",text="Width")
        
        height_settings = layout.row()
        height_settings.prop(autobake_settings,"height",text="Height")