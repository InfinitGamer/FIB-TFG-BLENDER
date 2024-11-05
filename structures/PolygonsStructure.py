import bpy

class PolygonsStructure(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()
    original_material_index: bpy.props.IntProperty()
    bake_material_index: bpy.props.IntProperty()
    vertices: bpy.props.IntVectorProperty(name="Índices de Vértices", size=5, default=5*(-1,))

    def set_vertices(self, vertices):
        length =len(vertices)
        self.vertices[0: length] = vertices[0:length]