import abc

from src.interpolator import Interpolator
from src.tools import get_pressure
from src.schemas import HydraulicModelSchema


class HydraulicModelBase(abc.ABC):
    def __init__(self, data: HydraulicModelSchema, interpolator: Interpolator):
        self.inlet_head: float | None = None
        self.inlet_temperature: float | None = None
        self.inlet_coordinate: float = data.inlet_coordinate
        self.inlet_elevation: float | None = None

        self.outlet_head: float | None = None
        self.outlet_temperature: float | None = None
        self.outlet_coordinate: float = data.outlet_coordinate
        self.outlet_elevation: float | None = None

        self.interpolator = interpolator
        self.density: float = data.density
        self.flow_rate: float | None = None

    @property
    def inlet_pressure(self):
        return get_pressure(self.inlet_head - self.inlet_elevation, self.density)

    @property
    def outlet_pressure(self):
        return get_pressure(self.outlet_head - self.outlet_elevation, self.density)


    @abc.abstractmethod
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float:
        """
        Рассчитывает напор в начальной точке объекта по напору в конечной точке и расходу нефти.
        :param outlet_head:
        :param flow_rate: Расход, m3/c.
        :return: Напор в начальной точке, м.
        """
        pass

    @abc.abstractmethod
    def solve_outlet_temperature(self, flow_rate: float, inlet_temperature: float) -> float:
        """
        Рассчитывает температуру в конечной точке объекта по известной температуре в начальной точке
        и расходу нефти.
        :param inlet_temperature:
        :param flow_rate: Расход, m3/c.
        :return: Температура в конечной точке, К.
        """
        pass

