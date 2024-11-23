from algorithms.parameterization.models.ModelInterface import ModelInterface
import random
import sympy as sp


class SphereModel(ModelInterface):

    def __init__(
        self, r: float = None, x: float = None, y: float = None, z: float = None
    ):
        super().__init__()
        self.r = r
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def fit(data: list) -> "ModelInterface":

        Cx, Cy, Cz, R = sp.symbols("Cx Cy Cz R")
        equations = map(
            lambda p: (p[0] - Cx) ** 2 + (p[1] - Cy) ** 2 + (p[2] - Cz) ** 2 - R**2,
            data,
        )
        x, y, z, r = sp.solve(equations, Cx, Cy, Cz, R)

        return SphereModel(x=x, y=y, z=z, r=r)

    @staticmethod
    def get_points(data) -> list:
        return random.sample(data, 4)

    def distance(self, point) -> float:
        distance = 0
        distance += (point[0]-self.x)**2
        distance += (point[1]-self.y)**2
        distance += (point[2]-self.z)**2
        distance -= self.r**2
        return abs(distance)
