import numpy as np
import pytest

from src.interpolator import Interpolator
from src.models.pipeline import Node, Pipe, Pipeline
from src.models.pump_station import PumpStation
from src.schemas import PipeSchema, PipelineSchema, PumpStationSchema


@pytest.fixture(name="interpolator")
def get_interpolator():
    points = np.array([(0, 100),
                       (20e3, 100),
                       (50e3, 100),
                       (77e3, 100),
                       (100e3, 100)])
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
        heat_transfer=1.3
    )

    inlet_node = Node(0, interpolator)
    outlet_node = Node(100e3, interpolator)
    pipe = Pipe(schema, inlet_node, outlet_node)
    return pipe


@pytest.fixture(name="pipeline")
def get_pipeline(interpolator: Interpolator):
    schema = PipelineSchema(
        outer_diameter=1.020,
        inner_diameter=0.992,
        roughness=0.2e-3,
        density=860,
        temperature_env=278.15,
        segment_length=0.1e3,
        inlet_coordinate=0,
        outlet_coordinate=100e3,
        heat_transfer=1.3
    )
    pipeline = Pipeline(schema, interpolator)
    return pipeline

@pytest.fixture(name="pump_station")
def get_pump_station(interpolator: Interpolator):
    schema = PumpStationSchema(
        density=860,
        inlet_coordinate=0,
        outlet_coordinate=100e3,
        a=273.0074080570295,
        b=1.2519107926468433e-05,
        pump_number=1,
        min_inlet_head=100,
        preset_outlet_temperature=300,
    )
    pump_station = PumpStation(schema, interpolator)
    return pump_station


