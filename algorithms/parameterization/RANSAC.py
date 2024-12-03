import bpy
from typing import Type
from algorithms.parameterization.models.ModelInterface import ModelInterface
import algorithms.parameterization.models as md
from math import sqrt
from random import uniform
import numpy as np
import bmesh

class RANSAC(bpy.types.Operator):
    bl_idname = "uv.auto_projection"
    bl_label = "Auto Projection RANSAC algorithm"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}
    #parameters
    iterations: bpy.props.IntProperty(default=100, min=0)
    density: bpy.props.FloatProperty(default=1.0, min=0.0)
    verbose: bpy.props.BoolProperty(default=False)
    @staticmethod
    def get_points_from_triangle(A: tuple[float,float,float], B: tuple[float,float,float], C: tuple[float,float,float], n: int):
        point_list :list[tuple[float,float,float]] = []
        A_list = list(A)
        B_list = list(B)
        C_list = list(C)
        for _ in range(0, n):
            c_a = uniform(0.0, 1.0)
            c_b = uniform(0.0, 1- c_a)
            c_c = 1 - c_a - c_b
            point = c_a* np.array(A_list) + c_b* np.array(B_list) + c_c*np.array(C_list)
            point = tuple(point)
            point_list.append(point)
        
        return point_list
    
    @staticmethod
    def get_points_from_square(A: tuple[float,float,float], B: tuple[float,float,float], C: tuple[float,float,float], D: tuple[float,float,float], n: int):
        
        mid = n // 2
        partial1 = RANSAC.get_points_from_triangle(A, B, C, mid)
        partial2 = RANSAC.get_points_from_triangle(A, C, D, n - mid)
        return partial1 + partial2
    
    @staticmethod
    def super_sampling(object: bpy.types.Object, density: float = 0):
        point_list :list[tuple[float,float,float]] = []

        for polygon in object.data.polygons:
            area = polygon.area
            number_points = int(area*density)
            list_vertices = [tuple(object.data.vertices[index].co) for index in polygon.vertices]
            if len(list_vertices) == 3:
                partial_list = RANSAC.get_points_from_triangle(*list_vertices, number_points)
                point_list.extend(partial_list)
            elif len(list_vertices) == 4:
                partial_list = RANSAC.get_points_from_square(*list_vertices, number_points)
                point_list.extend(partial_list)
        
        return point_list

    @staticmethod
    def RANSAC(data, ClassModel: Type[ModelInterface], iterations: int = 10, verbose:bool = False) -> tuple[float, ModelInterface]:

        best_error = float('inf')
        best_model = None

        for i in range(iterations):
            if verbose:
                print(f"Iteration {i}")
            try:
                
                elements = ClassModel.get_points(data)
                
                model = ClassModel.fit(elements)
                
                distances = list(map(lambda point: model.distance(point)**2, data))
                #RMSD error
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
        models = [
                  ("Sphere", md.SphereModel),
                  ("Cube", md.CubeModel),
                  ("Cylinder", md.CylinderModel)
                 ]
        functions ={"Sphere": bpy.ops.uv.sphere_project,
                    "Cube": bpy.ops.uv.cube_project,
                    "Cylinder": bpy.ops.uv.cylinder_project}
        
        obj: bpy.types.Object = context.active_object
        if obj.type != 'MESH':
            self.report({"ERROR_INVALID_INPUT"},"Object is not mesh type")
            return {"FINISHED"}
        
        mesh: bpy.types.Mesh = obj.data
        vertices = [tuple(v.co) for v in mesh.vertices]
        density_points = RANSAC.super_sampling(obj,self.density)
        vertices = vertices + density_points
        print(vertices)
        results =[]
        for type, model in models:
            result, _ = RANSAC.RANSAC(vertices,model, self.iterations, self.verbose)
            results.append((result, type))

        results = sorted(results, key=lambda tup: tup[0])
        print(results)
        key = results[0][1]
        func = functions[key]
        print(f"Se aplica {key}")

        new_uv_map = obj.data.uv_layers.new(name=f"{key}_projection_uv")
        
        obj.data.uv_layers.active = new_uv_map

    
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.select_all(action="SELECT")
    

        func(scale_to_bounds=True)
        bpy.ops.uv.select_all(action="SELECT")
        bpy.ops.uv.pack_islands(rotate=True, margin=0.02)

        bpy.ops.object.mode_set(mode="OBJECT")
        
        return {"FINISHED"}

    

