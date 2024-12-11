import bpy
from typing import Type
from algorithms.parameterization.models.ModelInterface import ModelInterface
import algorithms.parameterization.models as md
from math import sqrt
from random import uniform
import numpy as np



class RANSAC(bpy.types.Operator):
    bl_idname = "uv.auto_projection"
    bl_label = "Auto Projection RANSAC algorithm"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}
    # parameters
    iterations: bpy.props.IntProperty(default=100, min=0)
    density: bpy.props.FloatProperty(default=1.0, min=0.0)
    verbose: bpy.props.BoolProperty(default=False)

    @staticmethod
    def get_points_from_triangle(
        A: tuple[float, float, float],
        B: tuple[float, float, float],
        C: tuple[float, float, float],
        n: int,
    ):
        point_list: list[tuple[float, float, float]] = []
        A_list = list(A)
        B_list = list(B)
        C_list = list(C)
        for _ in range(0, n):
            c_a = uniform(0.0, 1.0)
            c_b = uniform(0.0, 1 - c_a)
            c_c = 1 - c_a - c_b
            point = (
                c_a * np.array(A_list) + c_b * np.array(B_list) + c_c * np.array(C_list)
            )
            point = tuple(point)
            point_list.append(point)

        return point_list

    @staticmethod
    def get_points_from_square(
        A: tuple[float, float, float],
        B: tuple[float, float, float],
        C: tuple[float, float, float],
        D: tuple[float, float, float],
        n: int,
    ):

        mid = n // 2
        partial1 = RANSAC.get_points_from_triangle(A, B, C, mid)
        partial2 = RANSAC.get_points_from_triangle(A, C, D, n - mid)
        return partial1 + partial2

    @staticmethod
    def super_sampling(object: bpy.types.Object, density: float = 0):
        point_list: list[tuple[float, float, float]] = []

        for polygon in object.data.polygons:
            area = polygon.area
            number_points = int(area * density)
            list_vertices = [
                tuple(object.data.vertices[index].co) for index in polygon.vertices
            ]
            if len(list_vertices) == 3:
                partial_list = RANSAC.get_points_from_triangle(
                    *list_vertices, number_points
                )
                point_list.extend(partial_list)
            elif len(list_vertices) == 4:
                partial_list = RANSAC.get_points_from_square(
                    *list_vertices, number_points
                )
                point_list.extend(partial_list)

        return point_list

    @staticmethod
    def RANSAC(
        data,
        ClassModel: Type[ModelInterface],
        iterations: int = 10,
        verbose: bool = False,
    ) -> tuple[float, ModelInterface]:

        best_error = float("inf")
        best_model = None

        for i in range(iterations):
            if verbose:
                print(f"Iteration {i}")
            try:

                elements = ClassModel.get_points(data)

                model = ClassModel.fit(elements)

                distances = list(map(lambda point: model.distance(point) ** 2, data))
                # RMSD error
                error = sqrt(sum(distances) / float(len(data)))

                if error < best_error:
                    best_error = error
                    best_model = model
                if verbose:
                    print(f"Current Error: {best_error}")
            except Exception as e:
                print(e)

        return best_error, best_model

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")

        models = [("Sphere", md.SphereModel), ("Cylinder", md.CylinderModel)]
        functions = {
            "Sphere": bpy.ops.uv.sphere_project,
            "Cylinder": bpy.ops.uv.cylinder_project,
        }

        objects: list[bpy.types.Object] = context.selected_objects
        for obj in objects:
            bpy.ops.object.select_all(action="DESELECT")

            if obj.type != "MESH":
                self.report({"ERROR_INVALID_INPUT"}, "Object is not mesh type")
                continue

            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            mesh: bpy.types.Mesh = obj.data
            vertices = [tuple(v.co) for v in mesh.vertices]
            density_points = RANSAC.super_sampling(obj, self.density)
            vertices = vertices + density_points

            min_error = float("inf")
            best_model = None
            for type, model in models:
                result, _ = RANSAC.RANSAC(
                    vertices, model, self.iterations, self.verbose
                )
                if result < min_error:
                    min_error = result
                    best_model = type

            func = functions[best_model]

            if self.verbose:
                print(f"Se aplica {best_model}")

            new_uv_map = obj.data.uv_layers.new(name=f"{best_model}_projection_uv")
            obj.data.uv_layers.active = new_uv_map

            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(type="FACE")
            bpy.ops.mesh.select_all(action="SELECT")

            current_rotation = bpy.context.space_data.region_3d.view_rotation.copy()

            # las posiciones se basan en la posción del viewport, por lo tanto, lo haremos las proyecciones de frente
            bpy.ops.view3d.view_axis(type="FRONT")

            func(scale_to_bounds=True)

            bpy.context.space_data.region_3d.view_rotation = current_rotation

            bpy.ops.object.mode_set(mode="OBJECT")

        return {"FINISHED"}
