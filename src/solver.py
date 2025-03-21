import math
from typing import List

from src.constants import get_constant
from src.models import HydraulicModelBase, Pipeline, Hookup
from src.schemas import SolverSchema

settings = get_constant()


class Solver:
    def __init__(self, models: List[HydraulicModelBase], data: SolverSchema):
        self.upper_border = data.upper_border
        self.lower_border = data.lower_border
        self.inlet_head = data.inlet_head
        self.inlet_temperature = data.inlet_temperature
        self.outlet_head = data.outlet_head
        self.models = models
        self._sum_hookup_flow_rate = sum(model.hookup_flow_rate for model in self.models if isinstance(model, Hookup))

    def solve(self):

        previous_flow_rate = math.inf
        flow_rate = -self._sum_hookup_flow_rate
        while abs(previous_flow_rate - flow_rate) > settings.ACCURACY:
            previous_flow_rate = flow_rate

            flow_rate = (self.upper_border + self.lower_border) / 2
            calc_inlet_head = self._solve_step(flow_rate)

            # Здесь спрятана проверка на то, работает ли НПС без кавитации или нет
            if calc_inlet_head and calc_inlet_head > self.inlet_head:
                self.upper_border = flow_rate
            else:
                self.lower_border = flow_rate

    def _solve_step(self, flow_rate: float) -> float | None:
        end_point_flow_rate = flow_rate + self._sum_hookup_flow_rate
        for i in range(3):
            inlet_head = self._solve_hydraulic(end_point_flow_rate)
            if inlet_head is None:
                break
            self._solve_thermal()
        return inlet_head

    def _solve_hydraulic(self, flow_rate) -> float | None:
        model_outlet_head = self.outlet_head
        for model in self.models[::-1]:
            if isinstance(model, Hookup):
                flow_rate -= model.hookup_flow_rate

            model_outlet_head = model.solve_inlet_head(flow_rate, model_outlet_head)
        return model_outlet_head

    def _solve_thermal(self):
        model_inlet_temperature = self.inlet_temperature
        for model in self.models:
            model_inlet_temperature = model.solve_outlet_temperature(model_inlet_temperature)
