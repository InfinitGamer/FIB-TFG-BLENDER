import bpy
import mathutils
import numpy as np
from itertools import combinations
from .indicators.IndicatorInterface import IndicatorInterface
from typing import Type
from .indicators import AreaDistortedIndicator
from .indicators import AverageDistorsionIndicator
from .indicators import RatioDistortedIndicator


class Analyzer(bpy.types.Operator):
    bl_idname = "uv.analyze"
    bl_label = "Analyzer"
    bl_description = "Distorsion Analyzer for parametrization"
    bl_options = {"REGISTER"}
    type: bpy.props.EnumProperty(
        items=[
            (
                "AVERAGEDISTORTION",
                "Average Distorsion",
                "Average distorsion from the whole object",
            ),
            (
                "AREADISTORTED",
                "Area Distorted",
                "Area distorted expressed in parts per units",
            ),
            (
                "RATIODISTORTED",
                "Ratio Distorted",
                "Image representing for each ratio of distorsion the number of polygons that have that ratio",
            ),
        ],
        default="AREADISTORTED",
    )
    path: bpy.props.StringProperty()

    @staticmethod
    def polygon_to_tangent_plane(
        object: bpy.types.Object,
        vertices_indexes: list[int],
        normal_p: mathutils.Vector,
    ) -> list[mathutils.Vector]:

        # vertices en espacio world
        verts = [
            object.matrix_world @ object.data.vertices[vert_idx].co.to_4d()
            for vert_idx in vertices_indexes
        ]
        # normal en espacio world
        new_matrix = object.matrix_world.to_3x3()
        new_matrix.invert_safe()
        new_matrix = new_matrix.transposed()
        normal = new_matrix @ normal_p.to_3d()
        # creamos matriz de transformacion que pase normal al eje z
        z_axis = mathutils.Vector((0, 0, 1))
        rotation_axis = normal.cross(z_axis).normalized()
        angle = normal.angle(z_axis)
        rotation_matrix = mathutils.Matrix.Rotation(angle, 4, rotation_axis)

        # aplicamos rotacion
        transformed_verts = [rotation_matrix @ vert for vert in verts]
        # nos quedamos con la componente x e y
        final_verts = [
            mathutils.Vector((round(v.x, 5), round(v.y, 5))) for v in transformed_verts
        ]
        return final_verts

    @staticmethod
    def get_eigen_values(
        tangent_points: list[mathutils.Vector], uv: list[mathutils.Vector]
    ) -> tuple:
        indexs = list(range(len(tangent_points)))
        i_selected = None
        j_selected = None
        for i, j in combinations(indexs, 2):
            P1 = tangent_points[i]
            P2 = tangent_points[j]
            matrix = mathutils.Matrix([P1, P2])
            det = matrix.determinant()
            if det != 0:
                i_selected = i
                j_selected = j
                break

        P1: mathutils.Vector = tangent_points[i_selected]
        P2: mathutils.Vector = tangent_points[j_selected]
        U1: mathutils.Vector = uv[i_selected]
        U2: mathutils.Vector = uv[j_selected]

        PF1 = np.array([[P1.x], [P1.y]])
        PF2 = np.array([[P2.x], [P2.y]])

        QF1 = np.array([[U1.x], [U1.y]])
        QF2 = np.array([[U2.x], [U2.y]])

        P = np.hstack([PF1, PF2])
        Q = np.hstack([QF1, QF2])

        # Resolvemos Sistema M * P = Q
        M = Q @ np.linalg.inv(P)

        MtM = M.T @ M

        eigen_values = np.linalg.eigvals(MtM)

        return tuple(eigen_values.tolist())

    @staticmethod
    def get_eigen_values_general(
        tangent_points: list[mathutils.Vector], uv: list[mathutils.Vector]
    ):

        length = len(tangent_points)
        if length == 3:

            eigen_values = Analyzer.get_eigen_values(tangent_points, uv)
            return [eigen_values]

        elif length == 4:
            tangent1 = tangent_points[0:3]
            uv1 = uv[0:3]
            tangent2 = [tangent_points[0]] + tangent_points[2:4]
            uv2 = [uv[0]] + uv[2:4]
            print(tangent1)
            print(uv1)
            print(tangent2)
            print(uv2)

            eigen_values1 = Analyzer.get_eigen_values(tangent1, uv1)
            eigen_values2 = Analyzer.get_eigen_values(tangent2, uv2)
            return [eigen_values1, eigen_values2]

        raise RuntimeError("Polygon is not a triangle or quad")

    @staticmethod
    def substract_vector(
        points: list[mathutils.Vector], vector: mathutils.Vector
    ) -> list[mathutils.Vector]:
        return [v - vector for v in points]

    @staticmethod
    def analyze(object: bpy.types.Object, indicator: Type[IndicatorInterface]) -> float:
        mesh = object.data
        eigen_values = []
        for polygon in mesh.polygons:
            vertex_index: list[int] = [
                mesh.loops[loop_index].vertex_index
                for loop_index in polygon.loop_indices
            ]

            uv_layer = mesh.uv_layers.active.uv

            UVs: list[mathutils.Vector] = [
                uv_layer[loop_index].vector for loop_index in polygon.loop_indices
            ]

            tangent_points: list[mathutils.Vector] = Analyzer.polygon_to_tangent_plane(
                object, vertex_index, polygon.normal
            )

            centered_tangent_point = Analyzer.substract_vector(
                tangent_points, tangent_points[0]
            )
            centered_tangent_UVs = Analyzer.substract_vector(UVs, UVs[0])

            eigen_value = Analyzer.get_eigen_values_general(
                centered_tangent_point, centered_tangent_UVs
            )
            eigen_values.append(eigen_value)
        print(f"eigen values list: {eigen_values}")

        return indicator.evaluate(eigen_values, mesh.polygons)

    @staticmethod
    def popup_message(context: bpy.types.Context, message: str, icon: str = "INFO"):
        def draw(self, context):
            self.layout.label(text=message)

        bpy.context.window_manager.popup_menu(draw, title="Score result", icon=icon)

    def execute(self, context):

        obj = context.active_object
        map = {
            "AVERAGEDISTORTION": AverageDistorsionIndicator,
            "AREADISTORTED": AreaDistortedIndicator,
            "RATIODISTORTED": RatioDistortedIndicator,
        }
        indicator = map.get(self.type)
        try:

            score = Analyzer.analyze(obj, indicator)
            
            if isinstance(score, int):
                Analyzer.popup_message(context, f"The score is {score}")
            else:

                path: str = self.path
                if not path.endswith(".png"):
                    path += ".png"

                with open(path, "wb") as f:
                    f.write(score.read())

                self.report({"INFO"}, "Plot saved")

        except Exception as e:
            self.report({"ERROR"}, str(e))
        return {"FINISHED"}
