import bpy


class ObjectsPanelAuto(bpy.types.Panel):
    bl_idname = "ObjectsPanelPanelAuto"
    bl_parent_id = "AutomaticBakePanel"
    bl_label = "Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        
        autobake_settings = scene.autobake_settings

        UIbake_settings = scene.UIbake_settings
        
        column_object_list = layout.column()

        column_object_list.template_list(
            "ObjectList",
            "",
            autobake_settings,
            "objects",
            UIbake_settings,
            "object_index",
        )
        
        column_object_list.operator("ui.add_object", text="Add Selected Objects")
        column_object_list.operator("ui.delete_object", text="Delete Selected Object")
