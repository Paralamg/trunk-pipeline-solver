import numpy as np


class Interpolator:

    def __init__(self, coords: np.ndarray, values: np.ndarray):
        if len(coords) != len(values):
            raise ValueError('Coordinates must be the same length as values')

        self.coords = coords
        self.values = values

    def __call__(self, value: float) -> float:
        return self.__interpolate(value)

    def __interpolate(self, value: float):
        """
        Интерполирует значение в точке x по кусочно-линейной функции.

        :param value: Координата, для которой нужно найти значение.
        :return: Интерполированное значение.
        """
        return float(np.interp(value, self.coords, self.values))  # Используем линейную интерполяцию 


if __name__ == '__main__':
    # Пример использования
    points = np.array([(0, 100), (50, 300), (200, 150)])
    print(points[-1,0])
    interpolator = Interpolator(points[:, 0], points[:, 1])
    x = 75
    print(interpolator(x))
    print(interpolator(0))
    print(interpolator(10))
    print(interpolator(50))
    print(interpolator(300))
