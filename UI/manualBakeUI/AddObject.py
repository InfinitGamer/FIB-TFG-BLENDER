import bpy
from bpy.types import bpy_prop_collection
from structures.ObjectName import ObjectName


class AddObject(bpy.types.Operator):

    bl_idname = "ui.add_object"
    bl_label = "Add Selected Object"

    @staticmethod
    def exists_in_collection(collection: bpy.types.CollectionProperty, name: str):
        
        return any(item.object_name == name for item in collection)

    def execute(self, context):
        
        scene = context.scene

        selected_objects = context.selected_objects

        object_name_collection: bpy.types.CollectionProperty = (
            scene.autobake_settings.objects
        )
        
        if selected_objects:
            for object in selected_objects:

                if (
                    not AddObject.exists_in_collection(
                        object_name_collection, object.name
                    )
                    and scene.objects[object.name].type == "MESH"
                ):
                    new_item = object_name_collection.add()
                    new_item.object_name = object.name

                    self.report({"INFO"}, f"Added {object.name} to the list")

                elif scene.objects[object.name].type != "MESH":
                    self.report(
                        {"WARNING"},
                        f"{object.name} not added because is not a mesh object",
                    )
                    
        else:
            self.report({"WARNING"}, "No objects selected")

        return {"FINISHED"}
