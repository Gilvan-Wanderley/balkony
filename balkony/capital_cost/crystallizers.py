from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class CrystallizerCost:
    class Type(Enum):
        Batch = {'min_size':  1.5, 'max_size': 30.0, 'data': (4.5097, 0.1731, 0.1344), 'unit':'m3', 'Fbare': 1.60}

    def __init__(self, type: Type) -> None:
        self._type = type
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of crystallizer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of crystallizer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)