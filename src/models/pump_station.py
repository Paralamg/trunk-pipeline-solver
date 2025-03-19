from .model_base import HydraulicModelBase
from ..schemas import PumpStationSchema


class PumpStation(HydraulicModelBase):
    def __init__(self, data: PumpStationSchema):
        self.a = data.a
        self.b = data.b
        self.pump_number = data.pump_number
        self.min_inlet_head = data.min_inlet_head

    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float | None:
        delta_head = self.pump_number * (self.a - self.b * flow_rate ** 2)
        outlet_head - delta_head
        return outlet_head - delta_head

    def solve_outlet_temperature(self, flow_rate: float, inlet_temperature: float) -> float:
        pass
