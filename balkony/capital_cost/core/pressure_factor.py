import math
from typing import Tuple

class PressureFactor:
    def __init__(self, properties: list[Tuple[Tuple[float, float], Tuple[float, float, float]]]) -> None:
        self._properties = properties
        pass

    def factor(self, pressure: float) -> float:
        '''
        pressure (barg) - Operation pressure\n
        return (-) - Pressure factor
        '''
        for prop in self._properties:
            limit, values = prop
            lower = limit[0] if limit[0] != None else 0.0
            upper = limit[1] if limit[1] != None else math.inf
            if pressure >= lower and pressure < upper:
                C1, C2, C3 = values
                return 10**(C1 + C2*math.log(pressure,10) + C3*(math.log(pressure,10)**2))
        raise Exception("Invalid Pressure.")