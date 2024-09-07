from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, PressureFactor

class FanCost:
    class Material(Enum):
        CarbonSteel = {'CentrifugalRadial': 2.74, 'BackwardCurve': 2.74, 'AxialVane': 2.74, 'AxialTube': 2.74}
        Fiberglass = {'CentrifugalRadial': 5.03, 'BackwardCurve': 5.03, 'AxialVane': 5.03, 'AxialTube': 5.03}
        NiAlloy = {'CentrifugalRadial': 5.78, 'BackwardCurve': 5.78, 'AxialVane': 5.78, 'AxialTube': 5.78}
        StainlessSteel = {'CentrifugalRadial': 11.52, 'BackwardCurve': 11.52, 'AxialVane': 11.52, 'AxialTube': 11.52}

    class Type(Enum):
        CentrifugalRadial = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.5391, -0.3533, 0.4477), 'unit':'m3/s' }
        BackwardCurve = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.3471, -0.0734, 0.3090), 'unit':'m3/s' }
        AxialVane = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.1761, -0.1373, 0.3414), 'unit':'m3/s' }
        AxialTube = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.0414, -0.3375, 0.4722), 'unit':'m3/s' }

    def __init__(self, type: Type, material: Material = Material.CarbonSteel) -> None:
        if type.name == 'CentrifugalRadial' or type.name == 'BackwardCurve':
            self._pressure = PressureFactor([((None, 1), (0.0, 0.0, 0.0)), 
                                             ((1, 16), (0.0, 0.20899, -0.0328))])
        else:
            self._pressure = PressureFactor([((None, 1), (0.0, 0.0, 0.0)), 
                                             ((1, 4), (0.0, 0.20899, -0.0328))])
        self._type = type
        self._material = material
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, flowrate: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            flowrate (m3/s) - Gas flowrate of fans\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(flowrate, CEPCI)        

    def bare_module(self, flowrate: float, rise_pressure: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            flowrate (m3/s) - Gas flowrate of fans\n
            rise pressure (kPa) - Rise pressure\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._material.value[self._type.name]
        Fp = self._pressure.factor(rise_pressure)
        cp0 = self._equipment.cost(flowrate, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp)
