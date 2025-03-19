from .constants import get_constant

constant = get_constant()


def get_pressure(head: float, density: float) -> float:
    pressure = head * constant.gravity * density
    return pressure


def get_head(pressure: float, density: float) -> float:
    head = pressure / (constant.gravity * density)
    return head
