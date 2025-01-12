import bpy


class UISwichSettings(bpy.types.PropertyGroup):
    
    switch: bpy.props.BoolProperty(default=False)
