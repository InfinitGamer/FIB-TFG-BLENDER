from UI.manualBakeUI.ObjectsPanel import ObjectsPanel
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
        # cogemos la escena actual
        scene = context.scene

        # cogemos los settings del autobake
        autobake_settings = scene.autobake_settings

        # cogemos los elementos para la UI de bake
        UIbake_settings = scene.UIbake_settings
        # creamos lista de objetos
        column_object_list = layout.column()

        column_object_list.template_list(
            "ObjectList",
            "",
            autobake_settings,
            "objects",
            UIbake_settings,
            "object_index",
        )
        # botones para añadir y eliminar objetos
        column_object_list.operator("ui.add_object", text="Add Selected Objects")
        column_object_list.operator("ui.delete_object", text="Delete Selected Object")
