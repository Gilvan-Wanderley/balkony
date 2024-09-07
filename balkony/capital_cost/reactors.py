from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class ReactorCost:
    class Type(Enum):
        Autoclave = { 'min_size': 1.0, 'max_size': 15.0, 'data': (4.5587, 0.2986, 0.0020), 'unit':'m3', 'Fbare': 4.0 }
        Fermenter = { 'min_size': 0.1, 'max_size': 35.0, 'data': (4.1052, 0.5320, -0.0005), 'unit':'m3', 'Fbare': 4.0 }
        Inoculum_Tank = { 'min_size': 0.07, 'max_size': 1.0, 'data': (3.7957, 0.4593, 0.0160), 'unit':'m3', 'Fbare': 4.0 }
        JacketedAgitated = { 'min_size': 0.1, 'max_size': 35.0, 'data': (4.1052, 0.5320, -0.0005), 'unit':'m3', 'Fbare': 4.0 }
        JacketedNonagitated = { 'min_size': 5.0, 'max_size': 45.0, 'data': (3.3496, 0.7235, 0.0025), 'unit':'m3', 'Fbare': 4.0 }
        Mixer = { 'min_size': 0.4, 'max_size': 60.0, 'data': (4.7116, 0.4479, 0.0004), 'unit':'m3', 'Fbare': 4.0 }
        Settler = { 'min_size': 0.4, 'max_size': 60.0, 'data': (4.7116, 0.4479, 0.0004), 'unit':'m3', 'Fbare': 4.0 }

    def __init__(self, type: Type) -> None:
        self._type = type
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of reactor\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of reactor\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
