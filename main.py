import numpy as np

from src.interpolator import Interpolator
from src.models import Hookup, PumpStation, Pipeline
from src.plotter import Plotter
from src.schemas import SolverSchema, HookupSchema, PumpStationSchema, PipelineSchema
from src.solver import Solver


def main():
    interpolator = get_interpolator()
    pipe1 = get_pipeline(interpolator, 0, 40e3)
    pipe2 = get_pipeline(interpolator, 40e3, 100e3)
    pump_station = get_pump_station(interpolator, 0)
    hookup = get_hookup(interpolator, 40e3, -0.5)
    schema = SolverSchema(
        upper_border=20,
        lower_border=0,
        inlet_head=150,
        outlet_head=120,
        inlet_temperature=300,
    )
    models = [pump_station, pipe1, hookup, pipe2]
    solver = Solver(models, schema)
    solver.solve()
    plotter = Plotter(models, solver.inlet_head)
    plot = plotter.plot()
    plot.show()



def get_interpolator():
    points = np.array([(0, 100),
                       (20e3, 90),
                       (50e3, 50),
                       (77e3, 150),
                       (120e3, 170),
                       (150e3, 300),
                       (170e3, 150),
                       (200e3, 100)])
    interpolator = Interpolator(points[:, 0], points[:, 1])
    return interpolator


def get_pipeline(interpolator: Interpolator, inlet_coordinate: float, outlet_coordinate: float):
    schema = PipelineSchema(
        outer_diameter=1.020,
        inner_diameter=0.992,
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


def get_pump_station(interpolator: Interpolator, coordinate: float):
    schema = PumpStationSchema(
        density=860,
        inlet_coordinate=coordinate,
        outlet_coordinate=coordinate,
        a=273.0074080570295,
        b=1.2519107926468433e-06,
        pump_number=3,
        min_inlet_head=40,
        preset_outlet_temperature=300,
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


if __name__ == '__main__':
    main()
