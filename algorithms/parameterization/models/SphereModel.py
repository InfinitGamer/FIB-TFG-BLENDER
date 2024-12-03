from algorithms.parameterization.models.ModelInterface import ModelInterface
import random

from math import sqrt
import numpy as np
class SphereModel(ModelInterface):

    def __init__(
        self, r: float = None, x: float = None, y: float = None, z: float = None
    ):
        super().__init__()
        self._r = r
        self._x = x
        self._y = y
        self._z = z

    @staticmethod
    def fit(data: list) -> "ModelInterface":
        if len(data) < 4:
            raise RuntimeError("Minium points to create a sphere is 4")
        
        
        A = []
        B = []
        for x, y, z in data[:4]:
            # expandiendo sistema de equaciones  x^2 +y^2 +z^2 = 2*z_0*z + 2*x_0*x + 2*y_0*y + constante(R^2 - y_0^2 - x_0^2 - z_0^2)
            A.append([2*x, 2*y, 2*z, 1])  # coeficientes de las incognitas
            B.append(x**2 + y**2 + z**2)  # resultado de cada equacion

        A = np.array(A)
        B = np.array(B)

        solution = np.linalg.solve(A, B) #da una excepcion si no es posible resolver

        # centro de la esfera
        x_c, y_c, z_c, D = solution

        # c partir de la constante D = R^2 - y_0^2 - x_0^2 - z_0^2 por lo tanto R es =  sqrt (D+ y_0^2 + x_0^2 + z_0^2)
        r = np.sqrt(x_c**2 + y_c**2 + z_c**2 + D) 
        
        return SphereModel(x=x_c , y=y_c , z=z_c , r= r)

    @staticmethod
    def get_points(data) -> list:
        return random.sample(data, 4)
     

    def distance(self, point) -> float:
        if self._x is None or self._y is None or self._z is None or self._r is None:
            raise RuntimeError("Sphere model doesn't have needed attributes to calculate distance")
        distance = 0
        distance += (point[0]-self._x)**2
        distance += (point[1]-self._y)**2
        distance += (point[2]-self._z)**2
        distance = sqrt(distance)
        distance -= self._r
        return abs(distance)

