import bpy
import mathutils
import numpy as np
from itertools import combinations
class Analyzer(bpy.types.Operator):
    bl_idname = "uv.analyze"
    bl_label = "Analyzer"
    bl_description = "Distorsion Analyzer for parametrization"
    bl_options = {"REGISTER"}

    @staticmethod
    def polygon_to_tangent_plane(object: bpy.types.Object, vertices_indexes: list[int], normal_p: mathutils.Vector) -> list[mathutils.Vector]:
        
        # vertices en espacio world
        verts = [object.matrix_world @ object.data.vertices[vert_idx].co.to_4d() for vert_idx in vertices_indexes]
        
        # normal es espacio world, la normal es un vector fila, por eso la multiplicacion de manera izquierda a derecha
        normal = normal_p @ object.matrix_world.to_3x3().transposed()

        # creamos matriz de transformacion que pase normal al eje z
        z_axis = mathutils.Vector((0, 0, 1))
        rotation_axis = normal.cross(z_axis).normalized()
        angle = normal.angle(z_axis)
        rotation_matrix = mathutils.Matrix.Rotation(angle, 4, rotation_axis)
        
        # aplicamos rotacion
        transformed_verts = [rotation_matrix @ vert for vert in verts]
        
        # nos quedamos con la componente x e y
        final_verts = [mathutils.Vector((v.x, v.y)) for v in transformed_verts]
        return final_verts
    
    @staticmethod
    def get_eigen_values(tangent_points:list[mathutils.Vector],uv: list[mathutils.Vector]) -> tuple:
        indexs = list(range(len(tangent_points)))
        i_selected = None
        j_selected = None
        for i, j in combinations(indexs, 2):
                P1 = tangent_points[i]
                P2 = tangent_points[j]
                matrix = mathutils.Matrix([P1,P2])
                det = matrix.determinant()
                if det != 0:
                     i_selected = i
                     j_selected = j
                     break
                
        P1: mathutils.Vector = tangent_points[i_selected]
        P2: mathutils.Vector = tangent_points[j_selected]
        U1: mathutils.Vector = uv[i_selected]  
        U2: mathutils.Vector = uv[j_selected]       
        
        PF1 = np.array([[P1.x], [P2.x]])
        PF2 = np.array([[P1.y], [P2.y]])

        QF1 = np.array([[U1.x], [U2.x]])
        QF2 = np.array([[U1.y], [U2.y]])

        P = np.hstack([PF1, PF2])  
        Q = np.hstack([QF1, QF2])

        #Resolvemos Sistema M * P = Q
        M = Q @ np.linalg.inv(P)

        MtM = M.T @ M
        
        eigen_values = np.linalg.eigvals(MtM)

        return tuple(eigen_values.tolist())
    
    @staticmethod
    def get_eigen_values_general(tangent_points:list[mathutils.Vector],uv: list[mathutils.Vector]):
        
        length = len(tangent_points)
        if length == 3:
            
            eigen_values = Analyzer.get_eigen_values(tangent_points, uv)
            return [eigen_values]
        
        elif length == 4:
            tangent1 = tangent_points[0:3]
            uv1 = uv[0:3]
            tangent2 = [tangent_points[0]] + tangent_points[2:4]
            uv2 = [uv[0]] + uv[2:4]

            eigen_values1 =   Analyzer.get_eigen_values(tangent1, uv1)
            eigen_values2 =   Analyzer.get_eigen_values(tangent2, uv2)
            return [eigen_values1, eigen_values2]
        
        raise RuntimeError("Polygon is not a triangle or quad")
          
    
    @staticmethod
    def analyze(object: bpy.types.Object):
        mesh = object.data
        for polygon in mesh.polygons:
            vertex_index: list[int] = [mesh.loops[loop_index].vertex_index for loop_index in polygon.loop_indices]
            
            uv_layer = mesh.uv_layers.active.uv

            UVs: list[mathutils.Vector] = [uv_layer[loop_index].vector for loop_index in polygon.loop_indices]

            tangent_points:list[mathutils.Vector] = Analyzer.polygon_to_tangent_plane(object, vertex_index, polygon.normal)



    def execute(self, context):
        #hacer try catch
        return {"FINISHED"}
