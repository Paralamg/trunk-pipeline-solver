from src.models.pipeline import Pipeline


def test_constructor(pipeline: Pipeline):
    assert isinstance(pipeline, Pipeline)


def test_solve_inlet_head(pipeline: Pipeline):
    flow_rate = 1.2
    outlet_head = 120
    inlet_head = pipeline.solve_inlet_head(flow_rate, outlet_head)
    assert inlet_head > outlet_head + 10
    assert inlet_head < 1000


def test_solve_outlet_temperature(pipeline: Pipeline):
    flow_rate = 1.2
    outlet_head = 120
    inlet_temperature = 300
    inlet_head = pipeline.solve_inlet_head(flow_rate, outlet_head)
    outlet_temperature = pipeline.solve_outlet_temperature(inlet_temperature)
    assert outlet_temperature < inlet_temperature - 2
    assert outlet_temperature > 270
