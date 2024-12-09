import bpy
import bmesh
import heapq
from collections import defaultdict
from typing import Dict
class MeshSeparator(bpy.types.Operator):
    bl_idname = "mesh.separator"
    bl_label = "Mesh Separtor"
    bl_description = "It separates the mesh based on set of points"
    bl_options = {"REGISTER"}

    @staticmethod
    def dijkstra(bm: bmesh.types.BMesh, pointA: int, pointB: int) -> list[bmesh.types.BMEdge]:

        seen_vertices = set()
        seen_vertices.add(pointA)
        distances = defaultdict(float)
        distances[pointA] = 0
        predecesor: Dict[int, bmesh.types.BMEdge] = {pointA: None}
        priority_queue = [(0, pointA)]
        
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            if current_vertex == pointB:
                break

        # Si la distancia actual es mayor que la registrada, lo ignoramos
            if current_distance > distances[current_vertex]:
                continue
            
            vertex = bm.verts[current_vertex]
            
            for edge in vertex.link_edges:
                neighbor = edge.other_vert(vertex)
                dist = (neighbor.co - vertex.co).length
                new_distance = current_distance + dist
                
                if not neighbor.index in seen_vertices:
                    distances[neighbor.index] = new_distance
                    predecesor[neighbor.index] = edge
                    seen_vertices.add(neighbor.index)
                    heapq.heappush(priority_queue, (new_distance, neighbor.index))

                elif new_distance < distances[neighbor.index]:
                    distances[neighbor.index] = new_distance
                    predecesor[neighbor.index] = edge
                    heapq.heappush(priority_queue, (new_distance, neighbor.index))

        edges = []

        point = pointB

        while predecesor[point] is not None:
            edge = predecesor[point]
            vertex = bm.verts[point]
            edges.append(edge)
            point = edge.other_vert(vertex).index
        
        return edges

              



    def make_seams(obj: bpy.types.Object):
        
        # Obtener el BMesh del objeto
        bm = bmesh.from_edit_mesh(obj.data)

        # Asegurar que la tabla de búsqueda de vértices esté disponible
        bm.verts.ensure_lookup_table()

        # Obtener los vértices seleccionados en el historial
        selected_points = [point for point in bm.select_history]

        # Verificar que todos los elementos seleccionados sean vértices
        if any(not isinstance(point, bmesh.types.BMVert) for point in selected_points):
            raise RuntimeError("There are selected elements that are not vertices")

        # Obtener índices de los vértices seleccionados
        selected_indices = [vert.index for vert in selected_points]
        

        # Iterar sobre los pares de vértices consecutivos
        for i in range(len(selected_indices) - 1):
            point1_index = selected_indices[i]
            point2_index = selected_indices[i + 1]
            
            edges: list[bmesh.types.BMEdge] = MeshSeparator.dijkstra(bm, point1_index, point2_index)
            
            for edge in edges:
                edge.seam = True

        # Cerrar el camino si hay al menos 3 puntos seleccionados
        if len(selected_indices) >= 3:
            point1_index = selected_indices[-1]
            point2_index = selected_indices[0]

            edges: list[bmesh.types.BMEdge] = MeshSeparator.dijkstra(bm, point1_index, point2_index)
            for edge in edges:
                edge.seam = True

        # Actualizar la malla con los cambios realizados
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)

 
    @staticmethod
    def separate_by_seams():
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_linked(delimit={'SEAM'})
        bpy.ops.mesh.separate(type='SELECTED')
    @staticmethod
    def mesh_separator(object: bpy.types.Object):
        
        bpy.ops.object.mode_set(mode='EDIT')

        MeshSeparator.make_seams(object)

       # MeshSeparator.separate_by_seams()


    def execute(self, context):
        active_object: bpy.types.Object= context.active_object
        
        try:
            MeshSeparator.mesh_separator(active_object)
            self.report({"INFO"}, "Mesh separated successfully")
        except Exception as e:
            self.report({"ERROR"}, str(e))
        
        return {"FINISHED"}
