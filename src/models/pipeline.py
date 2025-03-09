import math
from typing import List, override
from ..constants import get_constant
from .model_base import ModelBase

constant = get_constant()


def get_pressure(head: float, density: float) -> float:
    pressure = head / (constant.gravity * density)
    return pressure


def get_head(pressure: float, density: float) -> float:
    head = pressure * constant.gravity * density
    return pressure


class Pipe(ModelBase):
    def __init__(self, **kwargs):
        self.outer_diameter = kwargs["outer_diameter"]
        self.inner_diameter = kwargs["inner_diameter"]
        self.length = kwargs["length"]
        self.roughness = kwargs["roughness"]
        self.viscosity = kwargs["viscosity"]
        self.density = kwargs["density"]
        self.temperature_env = kwargs["temperature_env"]
        self.temperature_crit = kwargs["temperature_crit"]
        self.pressure_crit = kwargs["pressure_crit"]

        self.inlet_head: float | None = None
        self.inlet_temperature: float | None = None
        self.inlet_elevation: float | None = None
        self.inlet_pressure: float | None = None

        self.outlet_head: float | None = None
        self.outlet_temperature: float | None = None
        self.outlet_elevation: float | None = None
        self.outlet_pressure: float | None = None

        self.pressure_mean = constant.pressure_st
        self.temperature_mean = constant.temperature_st

    @override
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float:
        self.outlet_head = outlet_head
        calc_lambda = self.__get_lambda(flow_rate)
        head_loss = (1.02 * calc_lambda * self.length * 8 * flow_rate ** 2 /
                     (self.inner_diameter ** 5 * math.pi ** 2 * 9.81))
        self.inlet_head = outlet_head + head_loss
        self.inlet_pressure = get_pressure(self.inlet_head - self.inlet_elevation, self.density)

        if self.inlet_pressure < constant.pressure_min:
            self.inlet_head = get_head(constant.pressure_min, self.density) + self.inlet_elevation

        return self.inlet_head

    @override
    def solve_outlet_temperature(self, flow_rate: float, inlet_temperature: float) -> float:
        self.inlet_temperature = inlet_temperature
        a = (math.pi * constant.heat_transfer * self.inner_diameter /
             (self.density * flow_rate * constant.heat_capacity))

        i = (self.inlet_head - self.outlet_head) / self.length
        self.outlet_temperature = (self.inlet_temperature
                                   - (a * (self.inlet_temperature - self.temperature_env)
                                      - constant.gravity * i / constant.heat_capacity) * self.length)

    def __get_lambda(self, flow_rate) -> float:
        re = 4 * flow_rate / (self.viscosity * math.pi * self.inner_diameter)
        epsilon = self.inner_diameter / self.roughness
        d1 = 10 / epsilon
        d2 = 500 / epsilon

        if re < d1:
            return 0.3164 / re ** 0.25
        elif re < d2:
            return 0.11 * (epsilon + 68 / re) ** 0.25
        else:
            return 0.11 * epsilon ** 0.25


class Pipeline:
    def __init__(self):
        self.pipeline: List[Pipe] = []
