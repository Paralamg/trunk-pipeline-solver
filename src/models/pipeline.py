import math
from typing import List, override

from .model_base import ModelBase
from ..constants import get_constant
from ..schemas import PipeSchema

constant = get_constant()


def get_pressure(head: float, density: float) -> float:
    pressure = head / (constant.gravity * density)
    return pressure


def get_head(pressure: float, density: float) -> float:
    head = pressure * constant.gravity * density
    return pressure


class Pipe(ModelBase):
    def __init__(self, data: PipeSchema):
        self.outer_diameter = data.outer_diameter
        self.inner_diameter = data.inner_diameter
        self.length = data.length
        self.roughness = data.roughness
        self.viscosity = data.viscosity
        self.density = data.density
        self.temperature_env = data.temperature_env

        self.flow_rate: float | None = None

        self.inlet_head: float | None = None
        self.inlet_temperature: float | None = None
        self.inlet_elevation: float | None = None

        self.outlet_head: float | None = None
        self.outlet_temperature: float | None = None
        self.outlet_elevation: float | None = None

        self._temperature_mean = constant.temperature_st

    @property
    def inlet_pressure(self):
        return get_pressure(self.inlet_head - self.inlet_elevation, self.density)

    @property
    def outlet_pressure(self):
        return get_pressure(self.outlet_head - self.outlet_elevation, self.density)

    @property
    def temperature_mean(self):
        return self._temperature_mean

    @override
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float:
        self.flow_rate = flow_rate
        self.outlet_head = outlet_head

        self.viscosity = self.__get_visconsity(self.temperature_mean)
        calc_lambda = self.__get_lambda(self.flow_rate)
        head_loss = (1.02 * calc_lambda * self.length * 8 * self.flow_rate ** 2 /
                     (self.inner_diameter ** 5 * math.pi ** 2 * constant.gravity))
        self.inlet_head = self.outlet_head + head_loss

        # Проверка на самотечные участки
        if self.inlet_pressure < constant.saturated_vapour_pressure:
            self.inlet_head = get_head(constant.saturated_vapour_pressure, self.density) + self.inlet_elevation

        return self.inlet_head

    @override
    def solve_outlet_temperature(self, flow_rate: float, inlet_temperature: float) -> float:
        self.inlet_temperature = inlet_temperature
        a = (math.pi * constant.heat_transfer * self.inner_diameter /
             (self.density * flow_rate * constant.heat_capacity))

        self.outlet_temperature = self.inlet_temperature - a * (
                self.inlet_temperature - self.temperature_env) * self.length

        # Прибавка по гидравлическому уклону
        if self.inlet_head and self.outlet_head:
            i = (self.inlet_head - self.outlet_head) / self.length
            self.outlet_temperature += constant.gravity * i / constant.heat_capacity * self.length

        return self.outlet_temperature

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

    def __get_visconsity(self, temperature):
        return constant.viscosity_base * math.exp(
            -constant.delta_viscosity * (temperature - constant.temperature_viscosity_base))


class Pipeline:
    def __init__(self):
        self.pipeline: List[PipeSchema] = []
