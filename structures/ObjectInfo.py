import bpy
from structures.PolygonsStructure import PolygonsStructure


class ObjectInfo(bpy.types.PropertyGroup):
    object_name: bpy.props.StringProperty()
    bake_type: bpy.props.StringProperty
    polygons: bpy.props.CollectionProperty(type=PolygonsStructure)
