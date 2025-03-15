from pydantic import BaseModel, PositiveFloat


class PipeSchema(BaseModel):
    outer_diameter: PositiveFloat
    inner_diameter: PositiveFloat
    length: PositiveFloat
    roughness: PositiveFloat
    viscosity: PositiveFloat
    density: PositiveFloat
    temperature_env: PositiveFloat

