import bpy


class FileSelector(bpy.types.Operator):
    bl_idname = "ui.file_selector"
    bl_label = "Select file"

    
    filename: bpy.props.StringProperty(subtype="FILE_PATH")
    directory: bpy.props.StringProperty(subtype="DIR_PATH")
    
    def execute(self, context):
        context.scene.analyzer_settings.path = self.directory + self.filename

        return {"FINISHED"}

    def invoke(self, context, event):
        
        context.window_manager.fileselect_add(self)

        
        return {"RUNNING_MODAL"}