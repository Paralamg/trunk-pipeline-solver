from collections import OrderedDict

import numpy as np
from pydantic import BaseModel, PositiveFloat, field_validator


class PipeSchema(BaseModel):
    outer_diameter: PositiveFloat
    inner_diameter: PositiveFloat
    roughness: PositiveFloat
    density: PositiveFloat
    temperature_env: PositiveFloat


class PipelineSchema(BaseModel):
    elevation_profile: object
    segment_length: PositiveFloat

    @field_validator('elevation_profile')
    def check_elevation_profile(cls, v):
        if not isinstance(v, np.ndarray):
            raise ValueError('elevation_profile must be a numpy array')
        if v.ndim != 2 or v.shape[1] != 2 or v.shape[0] < 2:
            raise ValueError('elevation_profile must be a 2D numpy array with 2 columns and at least 2 row')
        return v





