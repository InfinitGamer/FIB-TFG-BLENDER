from algorithms.parameterization.models.ModelInterface import ModelInterface
import random
import sympy as sp


class SphereModel(ModelInterface):

    def __init__(
        self, r_squared: float = None, x: float = None, y: float = None, z: float = None
    ):
        super().__init__()
        self._r_squared = r_squared
        self._x = x
        self._y = y
        self._z = z

    @staticmethod
    def fit(data: list) -> "ModelInterface":
        if len(data) < 4:
            raise RuntimeError("Minium points to create a sphere is 4")
        Cx, Cy, Cz, R2 = sp.symbols("Cx Cy Cz R2")
        equations = map(
            lambda p: (p[0] - Cx) ** 2 + (p[1] - Cy) ** 2 + (p[2] - Cz) ** 2 - R2,
            data,
        )
        solutions = sp.solve(equations, Cx, Cy, Cz, R2, dict=True)
        if len(solutions) <= 0:
            raise RuntimeError("It doesn't exist a Sphere that can be expressed with the given data")
        sol = solutions[0]
        return SphereModel(x=sol[Cx].evalf() , y=sol[Cy].evalf() , z=sol[Cz].evalf() , r_squared=sol[R2].evalf())

    @staticmethod
    def get_points(data) -> list:
        return random.sample(data, 4)

    def distance(self, point) -> float:
        if self._x is None or self._y is None or self._z is None or self._r_squared is None:
            raise RuntimeError("Sphere model doesn't have needed attributes to calculate distance")
        distance = 0
        distance += (point[0]-self._x)**2
        distance += (point[1]-self._y)**2
        distance += (point[2]-self._z)**2
        distance -= self._r_squared
        return abs(distance)
