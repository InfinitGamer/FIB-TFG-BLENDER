import bpy


class UIBakeSettings(bpy.types.PropertyGroup):

    object_index: bpy.props.IntProperty()
    
    automatic_setting_number: bpy.props.IntProperty(min=1)
