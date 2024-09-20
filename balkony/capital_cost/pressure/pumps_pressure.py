from .core import PressureFactor, PressureProperties, PressureResult

class PumpPressure:
    def __init__(self, type: str) -> None:
        if type == 'Centrifugal':            
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 100), (0.1347, -0.2368, 0.1021))])
        else:
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 100), (-0.3935, 0.3957, -0.00226))]) 
            
    def factor(self, pressure: float) -> PressureResult:
        return self._pressure.factor(pressure)