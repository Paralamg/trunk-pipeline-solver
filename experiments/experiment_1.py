import numpy as np
from matplotlib import pyplot as plt

from experiments.model_factory import *
from src.interpolator import Interpolator
from src.plotter import Plotter
from src.schemas import SolverSchema
from src.solver import Solver


def main():
    interpolator = get_interpolator()
    schema = SolverSchema(
        upper_border=20,
        lower_border=0,
        inlet_head=150,
        outlet_head=120,
        inlet_temperature=310,
    )

    models = [
        get_pump_station(interpolator, 0, 2),
        get_pipeline(interpolator, 0, 80e3),
        get_hookup(interpolator, 80e3, 0.5),
        get_pipeline(interpolator, 80e3, 100e3),
        get_pump_station(interpolator, 100e3, 2),
        get_pipeline(interpolator, 100e3, 200e3),
    ]
    solver = Solver(models, schema)
    solver.solve()
    plotter = Plotter(models, solver.inlet_head)
    plot = plotter.plot()
    for model in models:
        print(model)
    plt.show()


def get_interpolator():
    points = np.array([(0, 100),
                       (20e3, 90),
                       (50e3, 100),
                       (77e3, 150),
                       (120e3, 170),
                       (150e3, 500),
                       (170e3, 150),
                       (180e3, 300),
                       (185e3, 100),
                       (200e3, 100)])

    interpolator = Interpolator(points[:, 0], points[:, 1])
    return interpolator


if __name__ == '__main__':
    main()
