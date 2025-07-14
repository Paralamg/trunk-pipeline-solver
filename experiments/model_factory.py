from src.interpolator import Interpolator
from src.models import Pipeline, PumpStation, Hookup
from src.schemas import PipelineSchema, PumpStationSchema, HookupSchema


def get_pipeline(
        interpolator: Interpolator,
        inlet_coordinate: float,
        outlet_coordinate: float,
        inner_diameter: float = 0.992,
        outer_diameter: float = 1.020,
):
    schema = PipelineSchema(
        outer_diameter=outer_diameter,
        inner_diameter=inner_diameter,
        roughness=0.2e-3,
        density=860,
        temperature_env=278.15,
        segment_length=100,
        inlet_coordinate=inlet_coordinate,
        outlet_coordinate=outlet_coordinate,
        heat_transfer=1.3
    )
    pipeline = Pipeline(schema, interpolator)
    return pipeline


def get_pump_station(
        interpolator: Interpolator,
        coordinate: float,
        pump_number: float,
        preset_outlet_temperature: float = 0,
):
    schema = PumpStationSchema(
        density=860,
        inlet_coordinate=coordinate,
        outlet_coordinate=coordinate,
        a=273.0074080570295,
        b=1.2519107926468433e-06,
        pump_number=pump_number,
        min_inlet_head=40,
        preset_outlet_temperature=preset_outlet_temperature,
    )
    pump_station = PumpStation(schema, interpolator)
    return pump_station


def get_hookup(interpolator: Interpolator, coordinate: float, flow_rate: float):
    schema = HookupSchema(
        density=860,
        inlet_coordinate=coordinate,
        outlet_coordinate=coordinate,
        flow_rate=flow_rate,
    )
    hookup = Hookup(schema, interpolator)
    return hookup
