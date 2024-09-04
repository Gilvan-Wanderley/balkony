from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, PressureFactor

class TankCost:
    class Material(Enum):
        CarbonSteel = {'APIFixedRoof': 1.0, 'APIFloatingRoof': 1.0}
        StainlessSteelClad = {'APIFixedRoof': 1.75, 'APIFloatingRoof': 1.75}
        StainlessSteel = {'APIFixedRoof': 3.12, 'APIFloatingRoof': 3.12}
        NiAlloyClad = {'APIFixedRoof': 3.63, 'APIFloatingRoof': 3.63}
        NiAlloy = {'APIFixedRoof': 7.09, 'APIFloatingRoof': 7.09}
        TitaniumClad = {'APIFixedRoof': 4.71, 'APIFloatingRoof': 4.71}
        Titanium = {'APIFixedRoof': 9.43, 'APIFloatingRoof': 9.73}

    class Type(Enum):
        APIFixedRoof = { 'min_size': 90.0, 'max_size': 30000.0, 'data': (4.8509, -0.3973, 0.1445), 'unit': 'm3', 'B1': 2.25, 'B2': 1.82 }
        APIFloatingRoof = { 'min_size': 1000.0, 'max_size': 40000.0, 'data': (5.9567, -0.7585, 0.1749), 'unit': 'm3', 'B1': 2.25, 'B2': 1.82 }

    def __init__(self, type: Type, material: Material = Material.CarbonSteel) -> None:
        self._pressure = PressureFactor([((None, 10), (0.0, 0.0, 0.0)), 
                                         ((10, 150), (0.1578, -0.2992, 0.1413))])
        self._type = type
        self._material = material
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of tank\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, pressure: float, CEPCI: float = 397) -> float:
        """
            volume (m3) - Volume of tank\n
            pressure (barg) - Operating pressure\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        Fm = self._material.value[self._type.name]
        Fp = self._pressure.factor(pressure)
        B1 = self._type.value['B1']
        B2 = self._type.value['B1']
        FBM = B1 + B2*Fm*Fp
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
