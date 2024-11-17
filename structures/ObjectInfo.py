import bpy
from structures.PolygonsStructure import PolygonsStructure


class ObjectInfo(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    bake_type: bpy.props.StringProperty()
    polygons: bpy.props.CollectionProperty(type=PolygonsStructure)
    is_valid: bpy.props.BoolProperty()
