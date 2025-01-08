from abc import ABC, abstractmethod
import bpy
import io
class IndicatorInterface(ABC):
    
    @staticmethod
    @abstractmethod
    def evaluate(eigen_values_list: list[list[tuple[float, float]]], polygons: bpy.types.MeshPolygons) -> float | io.BytesIO:
        pass