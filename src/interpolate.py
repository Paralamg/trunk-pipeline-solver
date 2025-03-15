import numpy as np

def interpolate_value(points, x):
    """
    Интерполирует значение в точке x по кусочно-линейной функции.

    :param points: Отсортированный список кортежей (координата, значение).
    :param x: Координата, для которой нужно найти значение.
    :return: Интерполированное значение.
    """
    coords, values = zip(*points)  # Разбираем список на два массива
    return np.interp(x, coords, values)  # Используем линейную интерполяцию

# Пример использования
points = [(0, 100), (50, 300), (200, 150)]
x = 75
print(interpolate_value(points, x))
print(interpolate_value(points, 0))
print(interpolate_value(points, 10))
print(interpolate_value(points, 50))
print(interpolate_value(points, 100))