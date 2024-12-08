import bpy
import bmesh
class MeshSeparator(bpy.types.Operator):
    bl_idname = "mesh.separator"
    bl_label = "Mesh Separtor"
    bl_description = "It separates the mesh based on set of points"
    bl_options = {"REGISTER"}

    @staticmethod
    def make_seams(object: bpy.types.Object):
        
        bm = bmesh.from_edit_mesh(object.data)

        selected_points = [point for point in bm.select_history]

        if any(map(lambda x: not isinstance(x, bmesh.types.BMVert), selected_points)):
            raise RuntimeError("There are selected elements that are not vertices")

        length = len(selected_points)

        for i in range(0, length-1):
            point1: bmesh.types.BMVert = selected_points[i]
            point2: bmesh.types.BMVert = selected_points[i+1]

            for edge in bm.edges:
                edge.select = False

            for vert in bm.verts:
                if vert.index in [point1.index, point2.index]:
                    vert.select = True
                else:
                    vert.select = False

            bmesh.update_edit_mesh(object.data)

            bpy.ops.mesh.shortest_path_select(use_face_step=False)
            for edge in object.data.edges:
                if edge.select:
                    edge.use_seam = True

            #cargamos de nuevo para la siguiente iteracion
            bm = bmesh.from_edit_mesh(object.data)
        
        #cerrar camino
        if length >= 3:
            point1: bmesh.types.BMVert = selected_points[length-1]
            point2: bmesh.types.BMVert = selected_points[0]

            for edge in bm.edges:
                edge.select = False

            for vert in bm.verts:
                if vert.index in [point1.index, point2.index]:
                    vert.select = True
                else:
                    vert.select = False
            bmesh.update_edit_mesh(object.data)

            bpy.ops.mesh.shortest_path_select(use_face_step=False)
            for edge in object.data.edges:
                if edge.select:
                    edge.use_seam = True

            #cargamos de nuevo para la siguiente iteracion
            bm = bmesh.from_edit_mesh(object.data)
    @staticmethod
    def separate_by_seams():
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_linked(delimit={'SEAM'})
        bpy.ops.mesh.separate(type='SELECTED')
    @staticmethod
    def mesh_separator(object: bpy.types.Object):
        
        bpy.ops.object.mode_set(mode='EDIT')

        MeshSeparator.make_seams(object)

        MeshSeparator.separate_by_seams()


    def execute(self, context):
        active_object: bpy.types.Object= context.active_object
        
        try:
            MeshSeparator.mesh_separator(active_object)
            self.report({"INFO"}, "Mesh separated successfully")
        except Exception as e:
            self.report({"ERROR"}, str(e))
        
        return {"FINISHED"}
