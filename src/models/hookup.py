from typing import override

from src.interpolator import Interpolator
from src.models import HydraulicModelBase
from src.schemas import HookupSchema


class Hookup(HydraulicModelBase):
    def __init__(self, data: HookupSchema, interpolator: Interpolator):
        super().__init__(data, interpolator)
        self.hookup_flow_rate = data.flow_rate

    def __str__(self):
        line = '-' * 95 + '\n'
        object_name = "Подкачка\n" if self.hookup_flow_rate >= 0 else "Отбор\n"
        info = (
            f"{'Координата':<31}{self.inlet_coordinate / 1000:10.3f} км\n"
            f"{'Расход':<31}{abs(self.hookup_flow_rate):10.3f} м3/с\n"
            f"{'Давление':<31}{abs(self.inlet_pressure) / 1e6:10.3f} МПа\n"
            f"{'Температура':<31}{abs(self.inlet_temperature) - 273.15:10.3f} С\n"
        )
        return line + object_name + line + info

    @override
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float:
        self.flow_rate = flow_rate
        self.outlet_head = self.inlet_head = outlet_head
        return outlet_head

    @override
    def solve_outlet_temperature(self, inlet_temperature: float) -> float:
        self.inlet_temperature = self.outlet_temperature = inlet_temperature
        return inlet_temperature


