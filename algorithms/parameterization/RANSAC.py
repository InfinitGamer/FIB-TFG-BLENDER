from typing import Type
from algorithms.parameterization.models.ModelInterface import ModelInterface
class RANSAC:

    @staticmethod
    def execute(data, ClassModel: Type[ModelInterface], iterations: int = 10,  threshold: float = 0.1) -> tuple[float, ModelInterface]:

        best_error = float('inf')
        best_model = None

        for _ in range(iterations):
            
            elements = ClassModel.get_points(data)
            model = ClassModel.fit(elements)
            
            distances = map(lambda point: model.distance(point))
            error = sum(distances)

            if error < best_error:
                best_error = error
                best_model = model
        

        return best_error, best_model
    

