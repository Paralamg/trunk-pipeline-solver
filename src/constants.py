from functools import lru_cache


class Constants:

    pressure_st: float = 101325
    temperature_st: float = 293.15
    gravity: float = 9.81
    saturated_vapour_pressure: float = 5e3
    heat_capacity: float = 2e3
    temperature_viscosity_base: float = 283.15
    viscosity_base: float = 45e-6
    delta_viscosity: float = 0.0366
    ACCURACY: float = 0.001
    # Прочностной расчет
    n: float = 1.15
    R1n: float = 510e6
    m: float = 0.9
    k1: float = 1.55
    kn: float = 1

    @property
    def R1(self):
        return self.R1n * self.m / (self.k1 * self.kn)


@lru_cache()
def get_constant() -> Constants:
    return Constants()
