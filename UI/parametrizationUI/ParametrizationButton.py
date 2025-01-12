import bpy
from structures.ParametrizationSettings import ParametrizationSettings
class ParametrizationButton(bpy.types.Operator):
    bl_idname = "ui.parametrization_object"
    bl_label = "Button for apply parametrization"
    bl_options = {"REGISTER"}

    def execute(self, context):

        scene = context.scene
        parametrization_settings : ParametrizationSettings = scene.parametrization_settings
        
        bpy.ops.uv.auto_projection(
            iterations = parametrization_settings.iterations,
            density = parametrization_settings.density,
            verbose = parametrization_settings.verbose
        )
        return {"FINISHED"}
