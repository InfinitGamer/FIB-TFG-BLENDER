from algorithms.parameterization.models.ModelInterface import ModelInterface
import random
from sympy import symbols, Matrix, Eq, simplify
from sympy.geometry import Line3D, Point3D
class CylinderModel (ModelInterface):
    def __init__(self):
        super().__init__()

    @staticmethod
    def fit(data: list) -> 'ModelInterface':
        if len(data) < 7:
            raise RuntimeError("Minium points to create a cube is 7")
        
    @staticmethod
    def get_points(data) ->list:
        return random.sample(data, 7)

    
    
    def distance(self, point) -> float:
        pass