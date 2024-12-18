from .IndicatorInterface import IndicatorInterface
import bpy
import io
class AreaDistortedIndicator(IndicatorInterface):
    @staticmethod
    def is_distorted(eigen_values: tuple[float, float])-> bool:
        e_min = min(eigen_values)
        e_max = max(eigen_values)
        return e_max/e_min != 1
    @staticmethod
    def evaluate(eigen_values_list: list[list[tuple[float, float]]], polygons: bpy.types.MeshPolygons) -> float | io.BytesIO:
        total_area = 0
        distorted_area = 0
        for eigen_values, polygon in zip(eigen_values_list, polygons):
            if len(eigen_values) == 2:
                eigen_value1 = eigen_values[0]
                eigen_value2 = eigen_values[1]

                d1 = AreaDistortedIndicator.is_distorted(eigen_value1)
                d2 = AreaDistortedIndicator.is_distorted(eigen_value2)

                area = 0.5*(int(d1) + int(d2) )* polygon.area
                
                distorted_area += area
                total_area += polygon.area
            else:
                eigen_value1 = eigen_values[0]
                d1 = AreaDistortedIndicator.is_distorted(eigen_value1)
                area= int(d1)*polygon.area

                distorted_area += area
                total_area += polygon.area
        
        return distorted_area/total_area
                

