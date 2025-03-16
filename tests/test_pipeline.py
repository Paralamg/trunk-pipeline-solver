import pytest

from src.interpolate import Interpolator
from src.models.pipeline import Pipeline
from src.schemas import PipelineSchema


@pytest.fixture(name="pipeline")
def get_pipeline(interpolator: Interpolator):
    schema = PipelineSchema(
        outer_diameter=1.020,
        inner_diameter=0.992,
        roughness=0.2e-3,
        density=860,
        temperature_env=278.15,
        segment_length=0.1e3,
        start_coordinate=0,
        end_coordinate=100e3,
        heat_transfer=1.3
    )
    pipeline = Pipeline(schema, interpolator)
    return pipeline


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
    inlet_temperature = 330
    inlet_head = pipeline.solve_inlet_head(flow_rate, outlet_head)
    outlet_temperature = pipeline.solve_outlet_temperature(flow_rate, inlet_temperature)
    assert outlet_temperature < inlet_temperature - 2
    assert outlet_temperature > 270
