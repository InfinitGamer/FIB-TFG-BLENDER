import bpy

class CommunicationData(bpy.types.PropertyGroup):

    baking_active: bpy.props.BoolProperty(default=False)

    switch_active: bpy.props.BoolProperty(default=False)

    ransac_active: bpy.props.BoolProperty(default=False)
    
    mesh_separator_active: bpy.props.BoolProperty(default=False)