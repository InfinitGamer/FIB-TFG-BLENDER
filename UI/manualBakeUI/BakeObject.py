import bpy
class BakeObject(bpy.types.Operator):
    bl_idname = "ui.bake_object"
    bl_label = "Bake Object"
    

    def execute(self, context):
        #cogemos la escena
        scene = context.scene

        #extraemos la configuracion del autobake
        autobake_settings = scene.autobake_settings

        device = autobake_settings.device
        bake_type = autobake_settings.bake_type
        width = autobake_settings.width
        height= autobake_settings.height
        path= autobake_settings.path
        pass_filter= autobake_settings.pass_filter
        margin = autobake_settings.margin
        margin_type = autobake_settings.margin_type

        bpy.ops.scene.autobake(device=device,
                                bake_type=bake_type,
                                width = width,
                                height=height,
                                path=path,
                                margin =margin,
                                margin_type = margin_type,
                                pass_filter =pass_filter)
        
        self.report({"INFO"},"Auto Bake completed")
        return {"FINISHED"}
