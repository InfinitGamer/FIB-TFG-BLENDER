import bpy


class PolygonsStructure(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()
    original_material_index: bpy.props.IntProperty()
    bake_material_index: bpy.props.IntProperty()
