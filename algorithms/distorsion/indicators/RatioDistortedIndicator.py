from .IndicatorInterface import IndicatorInterface
from collections import defaultdict
import bpy
import io
import matplotlib.pyplot as plt
import numpy as np


class RatioDistortedIndicator(IndicatorInterface):

    @staticmethod
    def eigen_ratio(eigen_values: tuple[float, float]) -> float:
        e_min = min(eigen_values)
        e_max = max(eigen_values)
        return round(e_max / e_min, 5)

    @staticmethod
    def evaluate(
        eigen_values_list: list[list[tuple[float, float]]],
        polygons: bpy.types.MeshPolygons,
    ) -> float | io.BytesIO:
        dict = defaultdict(float)

        for eigen_values in eigen_values_list:
            if len(eigen_values) == 2:
                eigen_value1 = eigen_values[0]
                eigen_value2 = eigen_values[1]

                d1 = RatioDistortedIndicator.eigen_ratio(eigen_value1)
                d2 = RatioDistortedIndicator.eigen_ratio(eigen_value2)

                dict[d1] += 0.5
                dict[d2] += 0.5

            else:
                eigen_value1 = eigen_values[0]

                d1 = RatioDistortedIndicator.eigen_ratio(eigen_value1)

                dict[d1] += 1

        dict = defaultdict(float, sorted(dict.items()))

        points = [key for key, val in dict.items() for _ in range(int(np.ceil(val)))]

        q75, q25 = np.percentile(points, [75, 25])
        iqr = q75 - q25
        h = 2 * iqr / (len(points) ** (1 / 3))
        max_v = max(points)
        min_v = min(points)
        range_fd = max_v - min_v

        n_bins = np.ceil(range_fd / h)

        plt.hist(points, bins=int(n_bins), color="b")

        plt.xticks(np.arange(min_v, max_v, 0.2))
        plt.xlabel("Ratio")
        plt.ylabel("Number of faces")
        plt.title("Frequency per ratio")
        plt.tight_layout()

        imagen_memoria = io.BytesIO()
        plt.savefig(imagen_memoria, format="png")
        imagen_memoria.seek(0)

        return imagen_memoria
