import bpy
from typing import Type
from algorithms.parameterization.models.ModelInterface import ModelInterface
import algorithms.parameterization.models as md
from math import sqrt
class RANSAC(bpy.types.Operator):
    bl_idname = "object.auto_projection"
    bl_label = "Auto Projection RANSAC algorithm"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

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
        vertices = [v.co()[:] for v in mesh.vertices]
        results =[]
        for type, model in models:
            result, _ = RANSAC.RANSAC(vertices,model, 100)
            results.append((result, type))

        results = sorted(results, key=lambda tup: tup[0])
        key = results[0][1]
        func = functions[key]
        #mirar si se ha seleccionado bien el objeto
        func()
        
        return {"FINISHED"}

    

