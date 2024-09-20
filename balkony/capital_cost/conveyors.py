from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class ConveyorCost:
    class Type(Enum):
        AutoBatch = {'min_size': 0.5, 'max_size': 1.7, 'data': (4.7681, 0.9740, 0.0240), 'unit':'m', 'Fbare': 1.20}
        Centrifugal = {'min_size': 0.5, 'max_size': 1.0, 'data': ( 4.3657,  0.8764,  -0.0049), 'unit':'m', 'Fbare': 1.25}
        OscillatingScreen = {'min_size': 0.5, 'max_size': 1.1, 'data': (4.8600,  0.3340,  0.1063), 'unit':'m', 'Fbare': 1.25}
        SolidBowl = {'min_size': 0.3, 'max_size': 2, 'data': (4.9697, 1.1689, 0.0038), 'unit':'m', 'Fbare': 1.10}

    def __init__(self, type: Type) -> None:
        self._type = type
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, diameter: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            diameter (m) - Diameter of conveyors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(diameter, CEPCI)        

    def bare_module(self, diameter: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            diameter (m) - Diameter of conveyors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(diameter, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)