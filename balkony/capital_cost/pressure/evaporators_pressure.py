from .core import PressureFactor, PressureProperties, PressureResult

class EvaporatorPressure:
    def __init__(self) -> None:
        self._pressure: PressureFactor = PressureFactor([ 
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 150), (0.1578, -0.2992, 0.1413)) ])
        
    def factor(self, pressure: float) -> PressureResult:
        return self._pressure.factor(pressure)
