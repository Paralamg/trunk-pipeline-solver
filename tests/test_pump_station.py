from src.models.pump_station import PumpStation


def test_constructor(pump_station: PumpStation):
    assert isinstance(pump_station, PumpStation)


def test_solve_inlet_head(pump_station: PumpStation):
    flow_rate = 0.5
    outlet_head = 600
    inlet_head = pump_station.solve_inlet_head(flow_rate, outlet_head)
    assert inlet_head < outlet_head - 100
    assert inlet_head > 100


def test_solve_outlet_temperature(pump_station: PumpStation):
    flow_rate = 1.2
    inlet_temperature = 330
    outlet_temperature = pump_station.solve_outlet_temperature(flow_rate, inlet_temperature)
    assert outlet_temperature == 300
