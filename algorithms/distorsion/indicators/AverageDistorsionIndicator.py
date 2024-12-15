from .IndicatorInterface import IndicatorInterface
import bpy
class AverageDistorsionIndicator(IndicatorInterface):
    @staticmethod
    def eigen_ratio(eigen_values: tuple[float, float])-> float:
        e_min = min(eigen_values)
        e_max = max(eigen_values)
        return e_max/e_min 
    @staticmethod
    def evaluate(eigen_values_list: list[list[tuple[float, float]]], polygons: bpy.types.MeshPolygons) -> float:
        total_area = 0
        average_distorsion = 0
        for eigen_values, polygon in zip(eigen_values_list, polygons):
            if len(eigen_values) == 2:
                eigen_value1 = eigen_values[0]
                eigen_value2 = eigen_values[1]

                d1 = AverageDistorsionIndicator.eigen_ratio(eigen_value1) -1
                d2 = AverageDistorsionIndicator.eigen_ratio(eigen_value2) -1

                area = 0.5*(d1 + d2 )* polygon.area
                
                average_distorsion += area
                total_area += polygon.area
            else:
                eigen_value1 = eigen_values[0]
                d1 = AverageDistorsionIndicator.eigen_ratio(eigen_value1) -1
                area = d1*polygon.area

                average_distorsion += area
                total_area += polygon.area
        
        return average_distorsion/total_area
                

