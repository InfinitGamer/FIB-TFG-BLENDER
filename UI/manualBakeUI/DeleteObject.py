import bpy

class DeleteObject(bpy.types.Operator):
    bl_idname = "ui.delete_object"
    bl_label = "Delete object item"
    
    def execute(self, context):
        #extraemos la escena del contexto actual
        scene = context.scene

        #extraemos la lista de nombres de los objetos a hacer bake 
        object_name_list = scene.autobake_settings.objects
        
        #extraemos el indice que indica que objeto de la lista borrar
        index = scene.UIbake_settings.object_index

        #si el indice es mayor o igual a 0 eliminamos el elemento en la posicion
        #del indice
        if index >= 0:
            name = object_name_list[index].object_name

            object_name_list.remove(index)
            

        return {"FINISHED"}
