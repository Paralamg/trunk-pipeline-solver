import pytest

from src.models import Pipe
from src.schemas import PipeSchema


@pytest.fixture(name="pipe")
def create_pipe():
    schema = PipeSchema(
        outer_diameter=1.020,
        inner_diameter=0.992,
        length=100e3,
        roughness=0.2e-3,
        density=860,
        temperature_env=278.15,
        inlet_elevation=0,
        outlet_elevation=100,
    )
    pipe = Pipe(schema)
    return pipe

def test_pipe_solve_inlet_head(pipe: Pipe):
    flow_rate = 0.8
    outlet_head = 120
    inlet_head = pipe.solve_inlet_head(flow_rate, outlet_head)
    assert inlet_head > outlet_head + 10
    assert inlet_head < 1000

def test_pipe_solve_outlet_temperature(pipe: Pipe):
    flow_rate = 0.8
    inlet_temperature = 330
    outlet_temperature = pipe.solve_outlet_temperature(flow_rate, inlet_temperature)
    assert outlet_temperature < inlet_temperature - 10

