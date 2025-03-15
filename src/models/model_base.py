import abc


class ModelBase(abc.ABC):
    @abc.abstractmethod
    def solve_inlet_head(self, flow_rate: float, outlet_head: float) -> float:
        """
        Рассчитывает напор в начальной точке объекта по напору в конечной точке и расходу нефти.
        :param flow_rate: Расход, m3/c.
        :param outlet_head: Напор в конечной точке, м.
        :return: Напор в начальной точке, м.
        """
        pass

    @abc.abstractmethod
    def solve_outlet_temperature(self, flow_rate: float, inlet_temperature: float) -> float:
        """
        Рассчитывает температуру в конечной точке объекта по известной температуре в начальной точке
        и расходу нефти.
        :param flow_rate: Расход, m3/c.
        :param inlet_temperature: Температура в начальной точке, К.
        :return: Температура в конечной точке, К.
        """
        pass
