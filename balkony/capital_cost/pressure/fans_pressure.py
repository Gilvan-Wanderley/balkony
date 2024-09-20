from .core import PressureFactor, PressureProperties, PressureResult

class FanPressure:
    def __init__(self, type: str) -> None:
        if type == 'CentrifugalRadial' or type == 'BackwardCurve':
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 1), (0.0, 0.0, 0.0)),
                PressureProperties((1, 16), (0.0, 0.20899, -0.0328)) ])
        else:
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 1), (0.0, 0.0, 0.0)),
                PressureProperties((1, 4), (0.0, 0.20899, -0.0328)) ])

    def factor(self, pressure: float) -> PressureResult:
        return self._pressure.factor(pressure)