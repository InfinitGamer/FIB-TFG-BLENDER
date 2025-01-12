import bpy


class DirectoryPanelAuto(bpy.types.Panel):
    bl_idname = "DirectoryPanelPanelAuto"
    bl_parent_id = "AutomaticBakePanel"
    bl_label = "Directory"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene

        autobake_settings = scene.autobake_settings

        path_settings = layout.row(align=True)
        path_settings.prop(autobake_settings, "path", text="Path")

        path_settings.operator("ui.folder_selector", text="", icon="FILE_FOLDER")
