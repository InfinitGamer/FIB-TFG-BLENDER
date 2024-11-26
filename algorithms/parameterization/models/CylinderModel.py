from algorithms.parameterization.models.ModelInterface import ModelInterface
import random
import sympy as sp
import numpy as np
from math import sqrt

class CylinderModel(ModelInterface):
    def __init__(self, matrix_transformation: np.ndarray = None, x: float = None, z: float = None, r_squared: float = None, y_min: float = None, y_max: float = None):
        super().__init__()
        self.matrix_transformation = matrix_transformation
        self.x = x
        self.z = z
        self.r_squared = r_squared
        self.y_min = y_min
        self.y_max = y_max

    @staticmethod
    def matrix_rotation_vector(vector: np.ndarray, target: np.ndarray) -> np.ndarray:
        vector_norm = vector / np.linalg.norm(vector)
        target_norm = target / np.linalg.norm(target)

        # calculamos eje de rotacion 
        # importante poner primero vector origen y después el vector destino
        # de este manera el angulo es el correcto y no el negativo
        axis = np.cross(vector_norm, target_norm)
        axis_norm = np.linalg.norm(axis)
        # si es esta alineado devolvemos identidad

        if axis_norm == 0:
            return np.eye(3)
        axis = axis / axis_norm
        # calculo angulo entre vector_norm y target_norm
        cos_theta = np.dot(vector_norm, target_norm)
        theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))

        # componentes del coseno y seno
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        one_minus_cos_t = 1 - cos_t
        # descomponemos eje de rotacion
        u, v, w = axis
        # creamos matriz de transformacion

        R = np.array([
        [cos_t + u**2 * one_minus_cos_t, u * v * one_minus_cos_t - w * sin_t, u * w * one_minus_cos_t + v * sin_t],
        [v * u * one_minus_cos_t + w * sin_t, cos_t + v**2 * one_minus_cos_t, v * w * one_minus_cos_t - u * sin_t],
        [w * u * one_minus_cos_t - v * sin_t, w * v * one_minus_cos_t + u * sin_t, cos_t + w**2 * one_minus_cos_t]
        ])
        return R

    @staticmethod
    def fit(data: list) -> "ModelInterface":
        if len(data) < 5:
            raise RuntimeError("Minium points to create a cube is 5")

        P0 = np.array(list(data[0]))
        P1 = np.array(list(data[1]))
        #creamos un eje
        Vector = P1 - P0
        target = np.array([0, 1, 0])
        # creamos un matriz de rotacion a que pasa un vector al vector (0,1,0) y así
        # poder trabajar con un cilidro alineado con este eje
        rotation_matrix = CylinderModel.matrix_rotation_vector(Vector, target)
        rotated_points = map(lambda x:tuple(rotation_matrix @ np.array(list(x))), data[2:5])
        
        #calculamos cilindro
        Cx, Cz, R2 = sp.symbols("Cx Cz R2")
        equations = map(
            lambda p: (p[0] - Cx) ** 2 +  + (p[2] - Cz) ** 2 - R2,
            rotated_points,
        )
        solutions = sp.solve(equations, Cx, Cz, R2, dict=True)
        if len(solutions) <= 0:
            raise RuntimeError("It doesn't exist a Sphere that can be expressed with the given data")
        sol = solutions[0]
        ys = [p[1] for p in rotated_points]
        min_y = min(ys)
        max_y = max(ys)
        X = sol[Cx].evalf()
        Z = sol[Cz].evalf()    
        R_squared = sol[R2].evalf()
        return CylinderModel(x=X , z=Z, matrix_transformation=rotation_matrix, r_squared=R_squared, y_max=max_y, y_min=min_y)

    @staticmethod
    def get_points(data) -> list:
        for _ in range(1000):
            random_sample:list[tuple] =random.sample(data, 5)
            random_sample_list: list[list] = map(lambda x: list(x), random_sample)
            matrix = np.array(random_sample_list)
            P1 = matrix[0]
            vectors = matrix[1:] - P1
            rank = np.linalg.matrix_rank(vectors)
            if rank != 1:
                return random_sample
        
        raise RuntimeError("There aren't non co-lienal points")
    @staticmethod
    def is_inside_range(x:float , min: float, max: float) -> bool:
        return min <= x and x <= max        
    def is_inside_cylinder(x, z, px,pz, radius) -> bool:
        return  ((x - px)**2 + (z -pz)**2) <= radius**2

    def distance(self, point) -> float:
        if (self.matrix_transformation is None or
        self.x is None or
        self.z is None or
        self.r_squared is None or
        self.y_min is None or
        self.y_max is None):
            raise  RuntimeError("Cylinder model doesn't have needed attributes to calculate distance")
        dy =min(abs(point[1] - self.y_min), abs(point[1] - self.y_max))
        dCylinder = abs(sqrt((point[0]-self.x)**2 + (point[2]-self.z)**2) - sqrt(self.r_squared))

        inside_y = CylinderModel.is_inside_range(point[1],self.y_min, self.y_max)
        inside_cylinder = CylinderModel.is_inside_cylinder(point[0], point[2], self.x, self.z, sqrt(self.r_squared))

        # si esta dentro del cilindro, la menor distancia se obtiene a partir de la distancia ortogonal
        # a todas las caras existentes
        if inside_y and inside_cylinder:
            return min(dy, dCylinder)
        
        return sqrt(float(not inside_y)*dy**2 + float(not inside_cylinder)*dCylinder**2)