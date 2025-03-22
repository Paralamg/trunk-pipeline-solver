import abc

from src.interpolator import Interpolator
from src.tools import get_pressure
from src.schemas import HydraulicModelSchema


class HydraulicModelBase(abc.ABC):
    def __init__(self, data: HydraulicModelSchema, interpolator: Interpolator):
        self.inlet_head: float | None = None
        self.inlet_temperature: float | None = None
        self.inlet_coordinate: float = data.inlet_coordinate

        self.outlet_head: float | None = None
        self.outlet_temperature: float | None = None
        self.outlet_coordinate: float = data.outlet_coordinate

        self.interpolator = interpolator
        self.density: float = data.density
        self.flow_rate: float | None = None

    @property
    def inlet_pressure(self):
        return get_pressure(self.inlet_head - self.inlet_elevation, self.density)

    @property
    def outlet_pressure(self):
        return get_pressure(self.outlet_head - self.outlet_elevation, self.density)

    @property
    def inlet_elevation(self):
        return self.interpolator(self.inlet_coordinate)

    @property
    def outlet_elevation(self):
        return self.interpolator(self.outlet_coordinate)


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
    def solve_outlet_temperature(self, inlet_temperature: float) -> float:
        """
        Рассчитывает температуру в конечной точке объекта по известной температуре в начальной точке
        и расходу нефти.
        :param inlet_temperature:
        :return: Температура в конечной точке, К.
        """
        pass

    def get_plot_data(self):
        coordinate_data = [self.inlet_coordinate, self.outlet_coordinate]
        head_data = [self.inlet_head, self.outlet_head]
        elevation_data = [self.inlet_elevation, self.outlet_elevation]
        temperature_data = [self.inlet_temperature, self.outlet_temperature]

        return coordinate_data, head_data, elevation_data, temperature_data

