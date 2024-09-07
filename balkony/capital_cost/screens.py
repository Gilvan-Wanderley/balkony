from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class ScreenCost:
    class Type(Enum):
        DSM = { 'min_size': 0.3, 'max_size': 6.0, 'data': (3.8050, 0.5856, 0.2120), 'unit':'m2', 'Fbare': 1.34 }
        Rotary = { 'min_size': 0.3, 'max_size': 15.0, 'data': (4.0485, 0.1118, 0.3260), 'unit':'m2', 'Fbare': 1.34 }
        Stationary = { 'min_size': 2.0, 'max_size': 11.0, 'data': (3.8219, 1.0368, -0.6050), 'unit':'m2', 'Fbare': 1.34 }
        Vibrating = { 'min_size': 0.3, 'max_size': 15.0, 'data': (4.0185, 0.1118, 0.3260), 'unit':'m2', 'Fbare': 1.34 }

    def __init__(self, type: Type) -> None:
        self._type = type
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of screen\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of screen\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
