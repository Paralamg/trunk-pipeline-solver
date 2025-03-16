import numpy as np
import pytest

from src.interpolate import Interpolator
from src.models.pipeline import Pipe, Node
from src.schemas import PipeSchema


@pytest.fixture(name="interpolator")
def get_interpolator():
    points = np.array([(0, 100), (50e3, 300), (100e3, 150)])
    interpolator = Interpolator(points[:, 0], points[:, 1])
    return interpolator


@pytest.fixture(name="pipe")
def create_pipe(interpolator: Interpolator):
    schema = PipeSchema(
        outer_diameter=1.020,
        inner_diameter=0.992,
        roughness=0.2e-3,
        density=860,
        temperature_env=278.15,
    )

    inlet_node = Node(0, interpolator)
    outlet_node = Node(90e3, interpolator)
    pipe = Pipe(schema, inlet_node, outlet_node)
    return pipe

def test_solve_inlet_head(pipe: Pipe):
    flow_rate = 1.2
    pipe.outlet_node.head = 120
    inlet_head = pipe.solve_inlet_head(flow_rate)
    assert pipe.inlet_node.head > pipe.outlet_node.head + 10
    assert pipe.inlet_node.head < 1000


def test_solve_outlet_temperature(pipe: Pipe):
    flow_rate = 0.8
    pipe.inlet_node.temperature = 330
    outlet_temperature = pipe.solve_outlet_temperature(flow_rate)
    assert pipe.outlet_node.temperature < pipe.inlet_node.temperature - 10
    assert pipe.outlet_node.temperature > pipe.temperature_env
