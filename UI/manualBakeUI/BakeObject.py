import bpy
from structures.BakingSettings import BakingSettings
from structures.UISwitchSettings import UISwichSettings
from structures.ObjectName import ObjectName


class BakeObject(bpy.types.Operator):

    bl_idname = "ui.bake_object"
    bl_label = "Bake Object"

    def turn_off_switch(self, switch_settings: UISwichSettings):

        if switch_settings.switch:
            bpy.ops.ui.switch_button()

    def turn_on_switch(self, switch_settings: UISwichSettings):

        if not switch_settings.switch:
            bpy.ops.ui.switch_button()

    def check_parameters(self, autobake_settings: BakingSettings):

        path = autobake_settings.path
        if path is None or path == "":
            self.report(
                {"ERROR_INVALID_INPUT"}, "There is no path to store baking results"
            )
            return False
        return True

    def remove_materials_previously_baked(
        self,
        scene: bpy.types.Scene,
        object_name_list: list[ObjectName],
        autobake_settings: BakingSettings,
    ):

        bake_type: str = autobake_settings.bake_type
        suffix = f"_{bake_type.lower()}_baked"

        remove_materials_name: set[str] = set()

        for object_name in object_name_list:
            name = object_name.object_name
            object: bpy.types.Object = scene.objects[name]
            materials: bpy.types.IDMaterials = object.data.materials

            for material in materials[:]:

                if material.name.endswith(suffix):
                    remove_materials_name.add(material.name)

                    index = materials.find(material.name)
                    materials.pop(index=index)

        for baked_material in remove_materials_name:

            material = bpy.data.materials.get(baked_material)
            bpy.data.materials.remove(material=material)

    def execute_bake(self, autobake_settings: BakingSettings):

        device = autobake_settings.device
        bake_type = autobake_settings.bake_type
        width = autobake_settings.width
        height = autobake_settings.height
        path = autobake_settings.path
        margin = autobake_settings.margin
        margin_type = autobake_settings.margin_type
        pass_filter = set()
        pass_filter_values = ["COMBINED", "GLOSSY", "DIFFUSE"]
        if autobake_settings.bake_type in pass_filter_values:

            if autobake_settings.use_direct:
                pass_filter = pass_filter | {"DIRECT"}

            if autobake_settings.use_indirect:
                pass_filter = pass_filter | {"INDIRECT"}

            if autobake_settings.use_color:
                pass_filter = pass_filter | {"COLOR"}

            if autobake_settings.bake_type == "COMBINED":

                if autobake_settings.use_diffuse:
                    pass_filter = pass_filter | {"DIFFUSE"}

                if autobake_settings.use_glossy:
                    pass_filter = pass_filter | {"GLOSSY"}

                if autobake_settings.use_transmission:
                    pass_filter = pass_filter | {"TRANSMISSION"}

                if autobake_settings.use_emit:
                    pass_filter = pass_filter | {"EMIT"}

        bpy.ops.scene.autobake(
            device=device,
            bake_type=bake_type,
            width=width,
            height=height,
            path=path,
            margin=margin,
            margin_type=margin_type,
            pass_filter=pass_filter,
        )

    def execute(self, context):

        scene = context.scene

        UIswitch_settings: UISwichSettings = scene.UIswitch_settings

        autobake_settings: BakingSettings = scene.autobake_settings

        if not self.check_parameters(autobake_settings):
            return {"FINISHED"}

        self.turn_off_switch(UIswitch_settings)

        objects_names: list[ObjectName] = autobake_settings.objects

        self.remove_materials_previously_baked(scene, objects_names, autobake_settings)

        self.execute_bake(autobake_settings)

        self.turn_on_switch(UIswitch_settings)

        self.report({"INFO"}, "Auto Bake completed")

        return {"FINISHED"}
