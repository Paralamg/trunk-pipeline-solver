import numpy as np
import pytest

from src.interpolate import Interpolator


@pytest.fixture(name="interpolator")
def get_interpolator():
    points = np.array([(0, 100),
                       (20e3, 100),
                       (50e3, 100),
                       (77e3, 100),
                       (100e3, 100)])
    interpolator = Interpolator(points[:, 0], points[:, 1])
    return interpolator
