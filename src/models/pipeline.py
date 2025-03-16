import math
from typing import List, override

import numpy as np

from .model_base import HydraulicModelBase
from ..constants import get_constant
from ..interpolate import Interpolator
from ..schemas import PipeSchema, PipelineSchema

constant = get_constant()


def get_pressure(head: float, density: float) -> float:
    pressure = head * constant.gravity * density
    return pressure


def get_head(pressure: float, density: float) -> float:
    head = pressure / (constant.gravity * density)
    return head


class Node():
    def __init__(self, x: float, interpolator: Interpolator):
        self.x = x
        self.head: float | None = None
        self.temperature: float | None = None
        self.interpolator = interpolator

    @property
    def elevation(self) -> float:
        return self.interpolator(self.x)


class Pipe(HydraulicModelBase):
    def __init__(self, data: PipeSchema, inlet_node: Node, outlet_node: Node):
        self.outer_diameter = data.outer_diameter
        self.inner_diameter = data.inner_diameter
        self.roughness = data.roughness
        self.density = data.density
        self.temperature_env = data.temperature_env

        self.flow_rate: float | None = None

        self.inlet_node = inlet_node
        self.outlet_node = outlet_node


    @property
    def inlet_pressure(self):
        return get_pressure(self.inlet_node.head - self.inlet_node.elevation, self.density)

    @property
    def outlet_pressure(self):
        return get_pressure(self.outlet_node.head - self.outlet_node.elevation, self.density)

    @property
    def temperature_mean(self):
        return self.outlet_node.temperature if self.outlet_node.temperature else constant.temperature_st

    @property
    def length(self):
        return self.outlet_node.x - self.inlet_node.x

    @override
    def solve_inlet_head(self, flow_rate: float) -> float:
        self.flow_rate = flow_rate

        calc_lambda = self.__get_lambda(self.flow_rate)
        head_loss = (1.02 * calc_lambda * self.length * 8 * self.flow_rate ** 2 /
                     (self.inner_diameter ** 5 * math.pi ** 2 * constant.gravity))
        self.inlet_node.head = self.outlet_node.head + head_loss

        # Проверка на самотечные участки
        if self.inlet_pressure < constant.saturated_vapour_pressure:
            self.inlet_node.head = get_head(constant.saturated_vapour_pressure,
                                            self.density) + self.inlet_node.elevation

        return self.inlet_node.head

    @override
    def solve_outlet_temperature(self, flow_rate: float) -> float:
        a = (math.pi * constant.heat_transfer * self.inner_diameter /
             (self.density * flow_rate * constant.heat_capacity))

        self.outlet_node.temperature = self.inlet_node.temperature - a * (
                self.inlet_node.temperature - self.temperature_env) * self.length

        # Прибавка по гидравлическому уклону
        if self.inlet_node.head and self.outlet_node.head:
            i = (self.inlet_node.head - self.outlet_node.head) / self.length
            self.outlet_node.temperature += constant.gravity * i / constant.heat_capacity * self.length

        return self.outlet_node.temperature

    def __get_lambda(self, flow_rate) -> float:
        viscosity = self.__get_visconsity(self.temperature_mean)
        re = 4 * flow_rate / (viscosity * math.pi * self.inner_diameter)
        epsilon = self.roughness / self.inner_diameter
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


class Pipeline(HydraulicModelBase):
    def __init__(self, data: PipelineSchema):
        self.pipeline: List[Pipe] = []
        self.elevation_profile: np.ndarray = data.elevation_profile
        self.segment_length: float = data.segment_length

        # Сортировка по координате value
        sorted_indices = np.argsort(self.elevation_profile[:, 0])
        self.elevation_profile = self.elevation_profile[sorted_indices]

        self.length: float = self.elevation_profile[-1, 0] - self.elevation_profile[0, 0]
        pipe_schema = PipeSchema(

        )

    @override
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float:
        pass

    @override
    def solve_outlet_temperature(self, flow_rate: float, inlet_temperature: float) -> float:
        pass
