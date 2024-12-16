from abc import ABC, abstractmethod
import bpy
class IndicatorInterface(ABC):
    
    @staticmethod
    @abstractmethod
    def evaluate(eigen_values: list[list[tuple[float, float]]], polygons: bpy.types.MeshPolygons) -> float:
        pass