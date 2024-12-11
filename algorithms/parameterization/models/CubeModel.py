import random
from math import sqrt
from algorithms.parameterization.models.ModelInterface import ModelInterface

class CubeModel (ModelInterface):

    def __init__(self, min_coords: tuple[float, float, float] = None, max_coords: tuple[float, float, float] = None):
        super().__init__()
        self._min_coords = min_coords
        self._max_coords = max_coords

    @staticmethod
    def fit(data: list) -> 'ModelInterface':
        if len(data) < 2:
            raise RuntimeError("Minium points to create a cube is 2")
        xs = [p[0] for p in data]
        ys = [p[1] for p in data]
        zs = [p[2] for p in data]
        x_min = min(xs)
        y_min = min(ys)
        z_min = min(zs)
        x_max = max(xs)
        y_max = max(ys)
        z_max = max(zs)
        return CubeModel(min_coords=(x_min,y_min,z_min), max_coords=(x_max,y_max,z_max))
    

    @staticmethod
    def get_points(data) ->list:
        return random.sample(data,2)

    
    @staticmethod
    def is_inside(coordinate: float, min : float, max : float) -> bool:
        return min <= coordinate and coordinate <= max
    
    def distance(self, point) -> float:
        if self._min_coords is None or self._max_coords is None:
            raise RuntimeError("Cube model doesn't have needed attributes to calculate distance")
        
        dx = min(abs(point[0] -self._min_coords[0]),abs(point[0] -self._max_coords[0]))
        dy = min(abs(point[1] -self._min_coords[1]),abs(point[1] -self._max_coords[1]))
        dz = min(abs(point[1] -self._min_coords[2]),abs(point[2] -self._max_coords[2]))
        x_inside = CubeModel.is_inside(point[0], self._min_coords[0], self._max_coords[0])
        y_inside = CubeModel.is_inside(point[1], self._min_coords[1], self._max_coords[1])
        z_inside = CubeModel.is_inside(point[2], self._min_coords[2], self._max_coords[2])

        if x_inside and y_inside and z_inside:
            return min(dx,dy,dz)

        return sqrt(float(not x_inside) * dx**2 + float(not y_inside) * dy**2 + float(not z_inside) * dz**2)