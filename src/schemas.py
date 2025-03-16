from collections import OrderedDict

import numpy as np
from pydantic import BaseModel, PositiveFloat, field_validator


class PipeSchema(BaseModel):
    outer_diameter: PositiveFloat
    inner_diameter: PositiveFloat
    roughness: PositiveFloat
    density: PositiveFloat
    temperature_env: PositiveFloat
    heat_transfer: PositiveFloat


class PipelineSchema(PipeSchema):
    segment_length: PositiveFloat
    start_coordinate: float
    end_coordinate: float






