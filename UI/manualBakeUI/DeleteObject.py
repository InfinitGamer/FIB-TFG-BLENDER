import bpy


class DeleteObject(bpy.types.Operator):
    bl_idname = "ui.delete_object"
    bl_label = "Delete object item"

    def execute(self, context):
        
        scene = context.scene

        object_name_list = scene.autobake_settings.objects
        
        index = scene.UIbake_settings.object_index
        
        if index >= 0:
            object_name_list.remove(index)

        return {"FINISHED"}
