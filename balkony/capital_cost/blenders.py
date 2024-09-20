from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class BlenderCost:
    class Type(Enum):
        Kneader = { 'min_size': 0.14, 'max_size': 3.0, 'data': (5.0141, 0.5867, 0.3224), 'unit':'m3', 'Fbare': 1.12}
        Ribbon =  { 'min_size': 0.7, 'max_size': 11.0, 'data': (4.1366, 0.5072, 0.0070), 'unit':'m3', 'Fbare': 1.12 }
        Rotary = { 'min_size': 0.7, 'max_size': 11.0, 'data': (4.1366, 0.5072, 0.0070), 'unit':'m3', 'Fbare': 1.12 }

    def __init__(self, type: Type) -> None:
        self._type = type
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of blender\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of blender\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
