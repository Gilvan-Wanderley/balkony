from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class CentrifugeCost:
    class Type(Enum):
        Apron = {'min_size':  1.0, 'max_size': 15.0, 'data': (3.9255, 0.5039, 0.1506), 'unit':'m2', 'Fbare': 1.20}
        Belt = {'min_size': 0.5, 'max_size': 325.0, 'data': (4.0637, 0.2584, 0.1550), 'unit':'m2', 'Fbare': 1.25}
        Pneumatic = {'min_size': 0.75, 'max_size': 65.0, 'data': (4.6616, 0.3205, 0.0638), 'unit':'m2', 'Fbare': 1.25}
        Screw = {'min_size': 0.5, 'max_size': 30.0, 'data': (3.6062, 0.2659, 0.1982), 'unit':'m2', 'Fbare': 1.10}

    def __init__(self, type: Type) -> None:
        self._type = type
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of centrifuge\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of centrifuge\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)