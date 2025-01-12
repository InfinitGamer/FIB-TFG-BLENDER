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
    def dijkstra(
        bm: bmesh.types.BMesh, pointA: int, pointB: int
    ) -> list[bmesh.types.BMEdge]:

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

        bm = bmesh.from_edit_mesh(obj.data)

        bm.verts.ensure_lookup_table()

        selected_points = [point for point in bm.select_history]

        if any(not isinstance(point, bmesh.types.BMVert) for point in selected_points):
            raise RuntimeError("There are selected elements that are not vertices")

        selected_indices = [vert.index for vert in selected_points]

        for i in range(len(selected_indices) - 1):

            point1_index = selected_indices[i]
            point2_index = selected_indices[i + 1]

            edges: list[bmesh.types.BMEdge] = MeshSeparator.dijkstra(
                bm, point1_index, point2_index
            )

            for edge in edges:

                edge.seam = True

        if len(selected_indices) >= 3:
            point1_index = selected_indices[-1]
            point2_index = selected_indices[0]

            edges: list[bmesh.types.BMEdge] = MeshSeparator.dijkstra(
                bm, point1_index, point2_index
            )
            for edge in edges:

                edge.seam = True

        for vertex in bm.verts:

            vertex.select = False

        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)

    @staticmethod
    def separate_by_seams(obj: bpy.types.Object):

        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.mesh.select_mode(type="FACE")

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces[0].select = True
        bmesh.update_edit_mesh(obj.data)

        bpy.ops.mesh.select_linked(delimit={"SEAM"})
        bpy.ops.mesh.separate(type="SELECTED")
        bpy.ops.mesh.select_all(action="DESELECT")

    @staticmethod
    def mesh_separator(object: bpy.types.Object):

        bpy.ops.object.mode_set(mode="EDIT")

        MeshSeparator.make_seams(object)

        MeshSeparator.separate_by_seams(object)

    def execute(self, context):

        context.scene.communication_data.mesh_separator_active = True
        active_object: bpy.types.Object = context.active_object

        try:
            MeshSeparator.mesh_separator(active_object)
            self.report({"INFO"}, "Mesh separated successfully")

        except Exception as e:
            self.report({"ERROR"}, str(e))

        context.scene.communication_data.mesh_separator_active = False
        return {"FINISHED"}
