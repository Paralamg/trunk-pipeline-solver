from typing import override

from ..tools import get_pressure
from .model_base import HydraulicModelBase
from ..interpolator import Interpolator
from ..schemas import PumpStationSchema


class PumpStation(HydraulicModelBase):
    def __init__(self, data: PumpStationSchema, interpolator: Interpolator):
        super().__init__(data, interpolator)

        self.a = data.a
        self.b = data.b
        self.pump_number = data.pump_number
        self.min_inlet_head = data.min_inlet_head
        self.preset_outlet_temperature = data.preset_outlet_temperature
        if self.preset_outlet_temperature != 0:
            self.outlet_temperature

    def __str__(self):
        line = '-' * 97 + '\n'
        object_name = "Насосная станция\n"
        heater_info = '' if self.preset_outlet_temperature == 0 else f"Уставка температуры: {self.preset_outlet_temperature}\n"
        info = (
            f"Координата:\t\t\t{self.inlet_coordinate / 1000:.3f} км\n"
            f"Коэффициент a:\t\t{self.a:.2f}\n"
            f"Коэффициент b:\t\t{self.b}\n"
            f"Количество насосов в работе: {self.pump_number}\n"
            f"Давление в линии всасывания: {self.inlet_pressure / 1e6:.3f} МПа\n"
            f"Давление в линии нагнетания: {self.outlet_pressure / 1e6:.3f} МПа\n"
            + heater_info

        )
        return line + object_name + line + info
    @override
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float | None:
        self.outlet_head = outlet_head
        self.flow_rate = flow_rate

        delta_head = self.pump_number * (self.a - self.b * (flow_rate * 3600) ** 2)
        self.inlet_head = outlet_head - delta_head

        if self.inlet_head - self.inlet_elevation > self.min_inlet_head:
            return self.inlet_head
        return None

    @override
    def solve_outlet_temperature(self, inlet_temperature: float) -> float:
        self.inlet_temperature = inlet_temperature

        if self.preset_outlet_temperature:
            return self.preset_outlet_temperature
        return inlet_temperature

