from pydantic import BaseModel, PositiveFloat, PositiveInt, Field


class HydraulicModelSchema(BaseModel):
    density: PositiveFloat
    inlet_coordinate: float
    outlet_coordinate: float


class PipeSchema(BaseModel):
    outer_diameter: PositiveFloat
    inner_diameter: PositiveFloat
    roughness: PositiveFloat
    density: PositiveFloat
    temperature_env: PositiveFloat
    heat_transfer: PositiveFloat


class PipelineSchema(HydraulicModelSchema, PipeSchema):
    segment_length: PositiveFloat


class PumpStationSchema(HydraulicModelSchema):
    a: PositiveFloat
    b: PositiveFloat
    pump_number: PositiveInt
    min_inlet_head: PositiveFloat
    preset_outlet_temperature: float = Field(ge=0)


class SolverSchema(BaseModel):
    upper_border: PositiveFloat
    lower_border: float = Field(ge=0)
    inlet_head: PositiveFloat
    outlet_head: PositiveFloat
    inlet_temperature: PositiveFloat
