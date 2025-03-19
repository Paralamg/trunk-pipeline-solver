import pytest

from src.interpolate import Interpolator
from src.models.pipeline import Pipe, Node
from src.schemas import PipeSchema




def test_solve_inlet_head(pipe: Pipe):
    flow_rate = 1.2
    pipe.outlet_node.head = 120
    inlet_head = pipe.solve_inlet_head(flow_rate)
    assert pipe.inlet_node.head > pipe.outlet_node.head + 10
    assert pipe.inlet_node.head < 1000


def test_solve_outlet_temperature(pipe: Pipe):
    flow_rate = 1.2
    pipe.inlet_node.temperature = 330
    outlet_temperature = pipe.solve_outlet_temperature(flow_rate)
    assert pipe.outlet_node.temperature < pipe.inlet_node.temperature - 10
    assert pipe.outlet_node.temperature > pipe.temperature_env
