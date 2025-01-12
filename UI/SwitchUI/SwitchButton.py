import bpy


class SwitchButton(bpy.types.Operator):
    bl_idname = "ui.switch_button"
    bl_label = "Switch"
    bl_description = "Apply switch between materials baked and original"
    bl_options = {"REGISTER"}

    def execute(self, context):
        switch = context.scene.UIswitch_settings.switch

        bpy.ops.scene.bake_switch('INVOKE_DEFAULT', switch=(not switch))
        context.scene.UIswitch_settings.switch = not switch
        
        return {"FINISHED"}
