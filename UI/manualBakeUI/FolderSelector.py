import bpy

class FolderSelector(bpy.types.Operator):
    bl_idname = "ui.file_selector"
    bl_label = "Select Folder"
    
    # Temporary property to hold the folder path during selection
    directory: bpy.props.StringProperty(subtype="DIR_PATH")
    
    def execute(self, context):
        #Asignamos el directorio escogido a la configuración del bake
        context.scene.autobake_settings.path = self.directory
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        #Abrimos el gestor archivos para elegir un path
        context.window_manager.fileselect_add(self)

        #mantenemos el gestor abierto hasta que el usuario escoja una    
        return {'RUNNING_MODAL'}