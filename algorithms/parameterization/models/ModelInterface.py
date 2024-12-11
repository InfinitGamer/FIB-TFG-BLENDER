from abc import ABC, abstractmethod


class ModelInterface(ABC):

    @staticmethod
    @abstractmethod
    def fit(data: list) -> 'ModelInterface':
        pass

    @staticmethod
    @abstractmethod
    def get_points(data) ->list:
        pass

    
    @abstractmethod
    def distance(self, point) -> float:
        pass