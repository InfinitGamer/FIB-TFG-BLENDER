import bpy


class SetAutomaticSettings(bpy.types.Operator):
    bl_idname = "ui.set_automatic_settings"
    bl_label = "Set automatic settings"
    bl_options = {"REGISTER"}

    device: bpy.props.EnumProperty(
        items=[
            ("GPU", "Gpu", "GPU Device"),
            ("CPU", "Cpu", "CPU Device"),
        ],
        default="CPU",
    )
    width: bpy.props.IntProperty(min=1, default=1, subtype="PIXEL")

    height: bpy.props.IntProperty(min=1, default=1, subtype="PIXEL")

    margin: bpy.props.IntProperty(min=0, default=0, subtype="PIXEL")

    margin_type: bpy.props.EnumProperty(
        items=[
            (
                "ADJACENT_FACES",
                "Adjacent Faces",
                "Use pixels from adjacent faces across UV seams",
            ),
            ("EXTEND", "Extend", "Extend border pixels outwards"),
        ]
    )

    automatic_setting_number: bpy.props.IntProperty(min=1)

    def execute(self, context):

        # extraemos escena
        scene = context.scene

        # extraemos los ajustes del autobake
        autobake_settings = scene.autobake_settings

        # si no tiene una GPU configurada, utilizará la GPU, sino la CPU
        autobake_settings.device = (
            "GPU"
            if context.preferences.addons["cycles"].preferences.has_active_device()
            else "CPU"
        )

        # asignamos los auto los valores por que se met
        autobake_settings.width = self.width
        autobake_settings.height = self.height
        autobake_settings.margin = self.margin
        autobake_settings.margin_type = self.margin_type

        # asignamos el boton que ha hecho la acción
        scene.UIbake_settings.automatic_setting_number = self.automatic_setting_number

        return {"FINISHED"}
