import math
from typing import List, override

from .model_base import HydraulicModelBase
from ..constants import get_constant
from ..interpolator import Interpolator
from ..schemas import PipeSchema, PipelineSchema
from ..tools import get_head, get_pressure

constant = get_constant()


class Node():
    def __init__(self, x: float, interpolator: Interpolator):
        self.x = x
        self.head: float | None = None
        self.temperature: float | None = None
        self.interpolator = interpolator
        self.is_self_flow: bool = False

    @property
    def elevation(self) -> float:
        return self.interpolator(self.x)

class SelfFlow():
    start_coordinate: float | None
    end_coordinate: float | None
    start_elevation: float | None
    end_elevation: float | None
    filling_degree: float | None

    @property
    def length(self) -> float:
        return abs(self.end_coordinate - self.start_coordinate)

class Pipe():
    def __init__(self, data: PipeSchema, inlet_node: Node, outlet_node: Node):
        self.outer_diameter = data.outer_diameter
        self.inner_diameter = data.inner_diameter
        self.roughness = data.roughness
        self.density = data.density
        self.temperature_env = data.temperature_env
        self.heat_transfer = data.heat_transfer

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
        return abs(self.outlet_node.x - self.inlet_node.x)



    def solve_inlet_head(self, flow_rate: float) -> float:
        self.flow_rate = flow_rate
        calc_lambda = self.__get_lambda(self.flow_rate)
        head_loss = (1.02 * calc_lambda * self.length * 8 * self.flow_rate ** 2
                     / (self.inner_diameter ** 5 * math.pi ** 2 * constant.gravity))
        self.inlet_node.head = self.outlet_node.head + head_loss
        

        # Проверка на самотечные участки
        if self.inlet_pressure < constant.saturated_vapour_pressure:
            if not self.outlet_node.is_self_flow:
                i = (self.inlet_node.head - self.outlet_node.head) / self.length
                devider = (self.outlet_node.elevation - self.inlet_node.elevation + i * (self.outlet_node.x - self.inlet_node.x))
                
                self.inlet_node.x = self.outlet_node.x + ((self.outlet_node.head - self.outlet_node.elevation - get_head(constant.saturated_vapour_pressure, self.density)) 
                   / devider * (self.outlet_node.x - self.inlet_node.x)) 
            
            self.inlet_node.is_self_flow = True
            self.inlet_node.head = get_head(constant.saturated_vapour_pressure,
                                            self.density) + self.inlet_node.elevation

        return self.inlet_node.head

    def solve_outlet_temperature(self) -> float:
        a = (math.pi * self.heat_transfer * self.inner_diameter /
             (self.density * self.flow_rate * constant.heat_capacity))

        self.outlet_node.temperature = self.inlet_node.temperature - a * (
                self.inlet_node.temperature - self.temperature_env) * self.length

        # Прибавка по трению
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
    def __init__(self, data: PipelineSchema, interpolator: Interpolator):
        super().__init__(data, interpolator)

        self.pipes: List[Pipe] = []
        self.nodes: List[Node] = []
        self.self_flows: List[SelfFlow] = []
        self.segment_length: float = data.segment_length
        self.temperature_env = data.temperature_env
        self.inner_diameter = data.inner_diameter
        self.outer_diameter = data.outer_diameter
        self.thickness = (self.outer_diameter - self.inner_diameter) / 2

        self.length: float = abs(self.outlet_coordinate - self.inlet_coordinate)
        pipes_number = math.ceil(self.length / self.segment_length)

        next_coordinate = self.inlet_coordinate
        for i in range(pipes_number):
            node = Node(next_coordinate, self.interpolator)
            next_coordinate += self.segment_length
            self.nodes.append(node)
        last_node = Node(self.outlet_coordinate, self.interpolator)
        self.nodes.append(last_node)

        for j in range(pipes_number):
            start_node = self.nodes[j]
            end_node = self.nodes[j + 1]
            pipe = Pipe(data, start_node, end_node)
            self.pipes.append(pipe)

    @property
    def pressure_max(self):
        pressure_max = constant.R1 * 2 * self.thickness / constant.n / self.inner_diameter
        return pressure_max

    @property
    def head_max(self):
        return get_head(self.pressure_max, self.density)

    @override
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float:
        self.outlet_head = outlet_head
        self.flow_rate = flow_rate

        self._reset_grid()

        self.nodes[-1].head = outlet_head
        for pipe in self.pipes[::-1]:
            pipe.solve_inlet_head(flow_rate)

        self.inlet_head = self.nodes[0].head
        return self.inlet_head

    @override
    def solve_outlet_temperature(self, inlet_temperature: float) -> float:

        self.inlet_temperature = inlet_temperature

        self.nodes[0].temperature = inlet_temperature
        for pipe in self.pipes:
            pipe.solve_outlet_temperature()

        self.outlet_temperature = self.nodes[-1].temperature
        return self.outlet_temperature

    @override
    def get_plot_data(self):
        coordinate_data = []
        head_data = []
        temperature_data = []
        elevation_data = []
        head_max_data = []
        self._find_self_flows()

        head_max = self.head_max
        for node in self.nodes:
            coordinate_data.append(node.x)
            head_data.append(node.head)
            temperature_data.append(node.temperature)
            elevation_data.append(node.elevation)
            head_max_data.append(head_max + node.elevation)
        return coordinate_data, head_data, elevation_data, temperature_data, head_max_data
    
    def _reset_grid(self):
        next_coordinate = self.inlet_coordinate
        for node in self.nodes:
            node.is_self_flow = False
            node.x = next_coordinate
            next_coordinate += self.segment_length

    def _find_self_flows(self):
        current_status = False
        self_flow: SelfFlow | None = None
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            if node.is_self_flow and not current_status:
                self_flow = SelfFlow()
                self_flow.start_coordinate = node.x
                self_flow.start_elevation = node.elevation
                self.self_flows.append(self_flow)
                current_status = True

            if current_status and not node.is_self_flow:
                end_node = self.nodes[i - 1]
                self.self_flows[-1].end_coordinate = end_node.x
                self.self_flows[-1].end_elevation = end_node.elevation
                self.self_flows[-1].filling_degree = self._get_filling_degree(self.self_flows[-1])
                current_status = False

    def _get_filling_degree(self, self_flow: SelfFlow):
        sin_alpha = (self_flow.start_elevation - self_flow.end_elevation) / (self_flow.length)
        upper_border = 360
        lower_border = 0
        while upper_border - lower_border > 0.01:
            phi = (upper_border + lower_border) / 2
            factor = (phi - math.sin(phi)) ** (5 / 3) / phi ** (2 / 3) - 0.2419 * self.flow_rate / self.inner_diameter ** (8 / 3) / math.sqrt(abs(sin_alpha))
            if factor > 0:
                upper_border = phi
            else:
                lower_border = phi
        
        phi = upper_border
        filling_degree = (phi - math.sin(phi)) / 2 / math.pi
        return filling_degree
                
