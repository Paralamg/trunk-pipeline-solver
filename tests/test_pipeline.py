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
        segment_length=10e3,
        start_coordinate=0,
        end_coordinate=95e3,
    )
    pipeline = Pipeline(schema, interpolator)
    return pipeline


def test_constructor(pipeline: Pipeline):
    assert isinstance(pipeline, Pipeline)


