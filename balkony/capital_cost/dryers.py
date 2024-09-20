from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class DryerCost:
    class Type(Enum):
        Drum = { 'min_size': 0.5, 'max_size': 50.0, 'data': (4.5472, 0.2731, 0.1340), 'unit':'m2', 'Fbare': 1.60}
        Rotary =  { 'min_size': 5.0, 'max_size': 100.0, 'data': (3.5645, 1.1118, -0.0777), 'unit':'m2', 'Fbare': 1.25 }
        GasFired = { 'min_size': 5.0, 'max_size': 100.0, 'data': (3.5645, 1.1118, -0.0777), 'unit':'m2', 'Fbare': 1.25 }
        Tray = { 'min_size': 1.8, 'max_size': 20.0, 'data': (3.6951, 0.5442, -0.1248), 'unit':'m2', 'Fbare': 1.25 }

    def __init__(self, type: Type) -> None:
        self._type = type
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of dryers\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of dryers\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
