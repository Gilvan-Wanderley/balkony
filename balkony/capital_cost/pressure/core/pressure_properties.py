import math
from typing import Tuple

class PressureProperties:
    def __init__(self, bounds: Tuple[float, float], parameters: Tuple[float, float, float]) -> None:
        lower = bounds[0] if bounds[0] != None else 0.0
        upper = bounds[1] if bounds[1] != None else math.inf
        self._bounds = (lower, upper)
        self._parameters = parameters

    @property
    def lower(self)-> float:
        return self._bounds[0]
    
    @property
    def upper(self)-> float:
        return self._bounds[1]
    
    @property
    def parameters(self) -> tuple[float, float, float]:
        return self._parameters
    
    def is_valid_range(self, value: float) -> bool:
        return True if value >= self.lower and value <= self.upper else False

    