import bpy

from structures.ObjectInfo import ObjectInfo
from structures.PolygonsStructure import PolygonsStructure
from bpy.app.handlers import persistent
from structures.CommunicationData import CommunicationData


class UpdateModificationsHandler:
    @staticmethod
    def contains_object(objects_info: bpy.types.bpy_prop_collection, name: str) -> bool:
        return objects_info.find(name) != -1

    @staticmethod
    def scene_contains_object(scene_objects: bpy.types.SceneObjects, name: str) -> bool:
        index = scene_objects.find(name)
        return index != -1

    @staticmethod
    def object_index(objects_info: bpy.types.bpy_prop_collection, name: str) -> int:
        return objects_info.find(name)

    @staticmethod
    def regenerate_polygons(obj: bpy.types.Object, model: ObjectInfo):
        mesh: bpy.types.Mesh = obj.data
        polygons: bpy.types.MeshPolygons = mesh.polygons
        is_valid: bool = True
        model.polygons.clear()
        suffix = f"_{model.bake_type}_baked"
        for polygon in polygons:

            model_info: PolygonsStructure = model.polygons.add()
            model_info.index = polygon.index

            material: bpy.types.Material = mesh.materials[polygon.material_index]

            if material.name.endswith(suffix):

                original_material_name = material.name.removesuffix(suffix)

                original_material_index = mesh.materials.find(original_material_name)

                if original_material_index == -1:
                    is_valid = False

                model_info.original_material_index = original_material_index
                model_info.bake_material_index = polygon.material_index
            else:

                baked_material_name = material.name + suffix
                bake_material_index = mesh.materials.find(baked_material_name)

                if bake_material_index == -1:
                    is_valid = False

                model_info.original_material_index = polygon.material_index
                model_info.bake_material_index = bake_material_index

        model.is_valid = is_valid


@persistent
def execute(scene: bpy.types.Scene, despgraph: bpy.types.Depsgraph):

    communication_data: CommunicationData = scene.communication_data
    if communication_data.baking_active or communication_data.switch_active:
        return
    
    switch_settings: bpy.types.bpy_prop_collection = scene.switch_settings
    scene_objects: bpy.types.SceneObjects = scene.objects

    for update in despgraph.updates:

        if isinstance(update.id, bpy.types.Object):
            obj: bpy.types.Object = update.id
            print(obj.name)
            if obj.type == "MESH":

                if UpdateModificationsHandler.contains_object(
                    switch_settings, obj.name
                ) and not UpdateModificationsHandler.scene_contains_object(
                    scene_objects, obj.name
                ):

                    index: int = UpdateModificationsHandler.object_index(
                        switch_settings, obj.name
                    )
                    switch_settings.remove(index)

                elif UpdateModificationsHandler.contains_object(
                    switch_settings, obj.name
                ) and UpdateModificationsHandler.scene_contains_object(
                    scene_objects, obj.name
                ):

                    index: int = UpdateModificationsHandler.object_index(
                        switch_settings, obj.name
                    )
                    model: ObjectInfo = switch_settings[index]
                    UpdateModificationsHandler.regenerate_polygons(obj, model)
