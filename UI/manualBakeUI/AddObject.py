import bpy
from bpy.types import bpy_prop_collection
from structures.ObjectName import ObjectName

class AddObject(bpy.types.Operator):
    
    bl_idname = "ui.add_object"
    bl_label = "Add Selected Object"
    @staticmethod
    def exists_in_collection(collection: bpy.types.CollectionProperty, name: str):
        #miramos existe el nombre en la colleción
        return any(item.object_name == name for item in collection)
    
    def execute(self, context):
        #extraemos la escena del contexto (la actual)
        scene = context.scene

        #extraemos todos los objetos seleccionados
        selected_objects = context.selected_objects

        #extraemos la lista que contiene los objetos a hacer bake
        object_name_collection: bpy.types.CollectionProperty = scene.autobake_settings.objects
        
        #miramos si hay elementos seleccionados
        if selected_objects:

            #por cada objeto lo añadimos si no han sido añadidos en algún momento
            for object in selected_objects:

                if (not AddObject.exists_in_collection(object_name_collection, object.name) and 
                    scene.objects[object.name].type =='MESH'):
                    
                    new_item = object_name_collection.add()
                    new_item.object_name = object.name
                    
                    
            self.report({'INFO'}, f"Added {object.name} to the list")
        else:
            self.report({'WARNING'}, "No active object selected")
        
        return {'FINISHED'}