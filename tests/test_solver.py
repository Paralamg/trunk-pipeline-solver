from src.models import Pipeline, PumpStation
from src.schemas import SolverSchema
from src.solver import Solver


def test_solve_one_pipe(pipeline: Pipeline):
    schema = SolverSchema(
        upper_border=20,
        lower_border=0,
        inlet_head=500,
        outlet_head=120,
        inlet_temperature=300,
    )
    models = [pipeline]
    solver = Solver(models, schema)
    solver.solve()
    assert 1 < models[0].flow_rate < 1.5
    assert abs(models[0].inlet_head - schema.inlet_head) < 0.5
    assert abs(models[0].outlet_head - schema.outlet_head) < 0.5


def test_solve_pump_and_pipe(pipeline: Pipeline, pump_station: PumpStation):
    schema = SolverSchema(
        upper_border=20,
        lower_border=0,
        inlet_head=120,
        outlet_head=120,
        inlet_temperature=300,
    )
    models = [pump_station, pipeline]
    solver = Solver(models, schema)
    solver.solve()
    assert 0.5 < models[0].flow_rate < 1
    assert abs(models[0].inlet_head - schema.inlet_head) < 0.5
    assert abs(models[1].outlet_head - schema.outlet_head) < 0.5
