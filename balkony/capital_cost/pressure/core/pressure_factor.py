import math
from .pressure_result import PressureResult
from .pressure_properties import PressureProperties

class PressureFactor:
    def __init__(self, properties: list[PressureProperties]) -> None:
        self._properties = properties
        self._max: PressureProperties = PressureProperties((math.inf, math.inf), (None, None, None))
        self._min: PressureProperties = PressureProperties((0.0, 0.0), (None, None, None))
        for prop in self._properties:
            self._min = prop if prop.lower < self._min.lower else self._min
            self._max = prop if prop.upper > self._max.upper else self._max

    def factor(self, pressure: float) -> PressureResult:
        '''
        pressure (barg) - Operation pressure\n
        return (-) - Pressure factor
        '''
        for prop in self._properties:            
            if prop.is_valid_range(pressure):
                C1, C2, C3 = prop.parameters
                fp = 10**(C1 + C2*math.log(pressure,10) + C3*(math.log(pressure,10)**2))
                return PressureResult(value=fp, status=('OK', True))
            
        if pressure > self._max.upper:
            C1, C2, C3 = self._max.parameters
            fp = 10**(C1 + C2*math.log(pressure,10) + C3*(math.log(pressure,10)**2))
            return PressureResult(value=fp, status=('Warning - Upper pressure limit.', False))
        else:
            C1, C2, C3 = self._min.parameters
            fp = 10**(C1 + C2*math.log(pressure,10) + C3*(math.log(pressure,10)**2))
            return PressureResult(value=fp, status=('Warning - Lower pressure limit.', False))