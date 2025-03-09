from functools import lru_cache


class Constants:
    pressure_st: float = 101325
    temperature_st: float = 293.15
    gravity: float = 9.81
    pressure_min: float = 0.2e6


@lru_cache()
def get_constant() -> Constants:
    return Constants()
