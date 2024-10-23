import bpy
from structures.ObjectName import ObjectName
class BakingSettings(bpy.types.PropertyGroup):

    
    objects: bpy.props.CollectionProperty(type=ObjectName)
    
    bake_type: bpy.props.EnumProperty(
        items=[
            ("COMBINED", "Combined", "Combined Bake"),
            ("AO", "Ao", "Ambient Occlusion"),
            ("EMIT", "Emit", "Emit Bake"),
            ("ENVIRONMENT", "Environment", "Environment Bake"),
            ("DIFFUSE", "Diffuse", "Diffuse Bake"),
            ("GLOSSY", "Glossy", "Glossy Bake"),
        ],
        default="COMBINED"
    )
    device: bpy.props.EnumProperty(
        items=[
            ("GPU", "Gpu", "GPU Device"),
            ("CPU", "Cpu", "CPU Device"),
        ],
        default="CPU"
    )
    width: bpy.props.IntProperty(min=1, default=1, subtype="PIXEL")

    height: bpy.props.IntProperty(min=1, default=1, subtype="PIXEL")
    
    margin: bpy.props.IntProperty(min=0, default=0, subtype="PIXEL")
    
    margin_type: bpy.props.EnumProperty(
        items=[
            ("ADJACENT_FACES", "Adjacent Faces", "Use pixels from adjacent faces across UV seams"),
            ("EXTEND", "Extend", "Extend border pixels outwards")
        ]
    )
    path: bpy.props.StringProperty()

    use_direct_light: bpy.props.BoolProperty(default=True)
    
    use_indirect_light: bpy.props.BoolProperty(default=True)
    
    use_color: bpy.props.BoolProperty(default=True)

