import bpy

class ParametrizationSettings(bpy.types.PropertyGroup):
    iterations: bpy.props.IntProperty(default=100, min=0)
    density: bpy.props.FloatProperty(default=1.0, min=0.0)
    verbose: bpy.props.BoolProperty(default=False)
    