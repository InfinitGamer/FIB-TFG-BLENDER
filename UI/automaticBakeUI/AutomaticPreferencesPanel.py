import bpy


class AutomaticPreferencesPanel(bpy.types.Panel):
    bl_idname = "AutomaticPreferencesPanel"
    bl_label = "Preferences"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_parent_id = "AutomaticBakePanel"

    @staticmethod
    def get_button(
        scene: bpy.types.Scene,
        row: bpy.types.UILayout,
        width: bpy.types.IntProperty,
        height: bpy.types.IntProperty,
        margin: bpy.types.IntProperty,
        margin_type: bpy.types.EnumProperty,
        button_number: bpy.types.IntProperty,
        text_button: str,
    ):

        button = row.operator(
            "ui.set_automatic_settings",
            text=text_button,
            icon=(
                "RADIOBUT_ON"
                if scene.UIbake_settings.automatic_setting_number == button_number
                else "RADIOBUT_OFF"
            ),
        )
        button.width = width
        button.height = height
        button.margin = margin
        button.margin_type = margin_type
        button.automatic_setting_number = button_number

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()

        AutomaticPreferencesPanel.get_button(
            scene=scene,
            row=row,
            width=512,
            height=512,
            margin=16,
            margin_type="EXTEND",
            button_number=1,
            text_button="Low",
        )
        AutomaticPreferencesPanel.get_button(
            scene=scene,
            row=row,
            width=1024,
            height=1024,
            margin=16,
            margin_type="ADJACENT_FACES",
            button_number=2,
            text_button="Medium",
        )
        AutomaticPreferencesPanel.get_button(
            scene=scene,
            row=row,
            width=2048,
            height=2048,
            margin=32,
            margin_type="ADJACENT_FACES",
            button_number=3,
            text_button="High",
        )
