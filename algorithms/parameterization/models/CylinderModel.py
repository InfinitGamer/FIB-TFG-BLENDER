from algorithms.parameterization.models.ModelInterface import ModelInterface
import random
import numpy as np
from math import sqrt

class CylinderModel(ModelInterface):
    def __init__(self, matrix_transformation: np.ndarray = None, x: float = None, z: float = None, r: float = None):
        super().__init__()
        self.matrix_transformation = matrix_transformation
        self.x = x
        self.z = z
        self.r= r
        

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
        rotated_points = list(map(lambda x:tuple(rotation_matrix @ np.array(list(x))), data[2:5]))
        
        A = []
        B = []
        for x, _, z in rotated_points:
            #expandiendo sistema de equaciones  x^2  +z^2 = 2*z_0*z + 2*x_0*x + constante(R^2  - x_0^2 - z_0^2)
            A.append([2*x, 2*z, 1]) # coeficientes de las incognitas
            B.append(x**2 + z**2) # resultado de cada equacion

        A = np.array(A)
        B = np.array(B)
        
        solution = np.linalg.solve(A, B) #da una excepcion si no es posible resolver

        # centro del cilindro
        x_c, z_c, D = solution
        # a partir de la constante D = R^2  - x_0^2 - z_0^2 por lo tanto R es =  sqrt (D + x_0^2 + z_0^2)
        r = np.sqrt(x_c**2 + z_c**2 + D)

        
        return CylinderModel(x=x_c , z=z_c, matrix_transformation=rotation_matrix, r=r)

    @staticmethod
    def get_points(data) -> list:
        return random.sample(data, 5)
       
    def is_inside_cylinder(x, z, px,pz, radius) -> bool:
        return  ((x - px)**2 + (z -pz)**2) <= radius**2

    def distance(self, point) -> float:
        if (self.matrix_transformation is None or
        self.x is None or
        self.z is None or
        self.r is None):
            raise  RuntimeError("Cylinder model doesn't have needed attributes to calculate distance")
        # punto transformado a nuestro sistema
        t_point = self.matrix_transformation @ np.array(list(point))

        dCylinder = abs(sqrt((t_point[0]-self.x)**2 + (t_point[2]-self.z)**2) - self.r)

        return dCylinder