import bpy


class FolderSelector(bpy.types.Operator):
    bl_idname = "ui.folder_selector"
    bl_label = "Select Folder"

    # parameters
    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def execute(self, context):
        
        context.scene.autobake_settings.path = self.directory

        return {"FINISHED"}

    def invoke(self, context, event):
        
        context.window_manager.fileselect_add(self)
        
        return {"RUNNING_MODAL"}
