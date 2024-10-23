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

        #creamos lista
        layout.template_list("ObjectList", "", autobake_settings, "objects", UIbake_settings, "object_index")
        
        layout.operator("ui.add_object", text="Add Selected Objects")
        layout.operator("ui.delete_object", text="Delete Selected Object")