from functools import lru_cache


class Constants:

    pressure_st: float = 101325
    temperature_st: float = 293.15
    gravity: float = 9.81
    saturated_vapour_pressure: float = 0.2e6
    heat_transfer: float = 1.3
    heat_capacity: float = 2e3
    temperature_viscosity_base: float = 283.15
    viscosity_base: float = 45e-6
    delta_viscosity: float = 0.0366


@lru_cache()
def get_constant() -> Constants:
    return Constants()
