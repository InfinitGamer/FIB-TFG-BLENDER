import bpy


class BakeObject(bpy.types.Operator):
    bl_idname = "ui.bake_object"
    bl_label = "Bake Object"

    def execute(self, context):
        # cogemos la escena
        scene = context.scene

        # extraemos la configuracion del autobake
        autobake_settings = scene.autobake_settings

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
        if path is None or path == "":
            self.report(
                {"ERROR_INVALID_INPUT"}, "There is no path to store baking results"
            )
            return {"FINISHED"}

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

        self.report({"INFO"}, "Auto Bake completed")
        return {"FINISHED"}
