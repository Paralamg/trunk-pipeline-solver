from pydantic import BaseModel, PositiveFloat


class PipeSchema(BaseModel):
    outer_diameter: PositiveFloat
    inner_diameter: PositiveFloat
    length: PositiveFloat
    roughness: PositiveFloat
    density: PositiveFloat
    temperature_env: PositiveFloat
    inlet_elevation: float
    outlet_elevation: float


