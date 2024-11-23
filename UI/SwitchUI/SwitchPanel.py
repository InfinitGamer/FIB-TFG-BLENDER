import bpy


class SwitchPanel(bpy.types.Panel):
    bl_idname = "Switch panel"
    bl_parent_id = "AddonPanel"
    bl_label = "Switch Section"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.operator(
            "ui.switch_button",
            text="Switch",
            icon="RADIOBUT_ON" if scene.UIswitch_settings.switch else "RADIOBUT_OFF",
        )
