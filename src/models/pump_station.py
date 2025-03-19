from typing import override

from .model_base import HydraulicModelBase
from ..interpolate import Interpolator
from ..schemas import PumpStationSchema


class PumpStation(HydraulicModelBase):
    def __init__(self, data: PumpStationSchema, interpolator: Interpolator):
        super().__init__(data, interpolator)

        self.a = data.a
        self.b = data.b
        self.pump_number = data.pump_number
        self.min_inlet_head = data.min_inlet_head
        self.preset_outlet_temperature = data.preset_outlet_temperature

    @override
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float | None:
        self.outlet_head = outlet_head
        self.flow_rate = flow_rate

        delta_head = self.pump_number * (self.a - self.b * (flow_rate * 3600) ** 2)
        self.inlet_head = outlet_head - delta_head

        if self.inlet_head > self.min_inlet_head:
            return self.inlet_head
        return None

    @override
    def solve_outlet_temperature(self, flow_rate: float, inlet_temperature: float) -> float:
        self.flow_rate = flow_rate
        self.inlet_temperature = inlet_temperature

        if self.preset_outlet_temperature:
            return self.preset_outlet_temperature
        return inlet_temperature

