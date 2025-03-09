import abc


class ModelBase(abc.ABC):
    @abc.abstractmethod
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float:
        pass

    @abc.abstractmethod
    def solve_outlet_temperature(self, flow_rate: float, inlet_temperature: float) -> float:
        pass
