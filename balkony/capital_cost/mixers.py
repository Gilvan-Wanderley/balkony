from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class MixerCost:
    class Type(Enum):
        Impeller = { 'min_size': 5.0, 'max_size': 150.0, 'data': (3.8511, 0.7009, -0.0003), 'unit':'kW', 'Fbare': 1.38 }
        Propeller = { 'min_size': 5.0, 'max_size': 500.0, 'data': (4.3207, 0.0359, 0.1346), 'unit':'kW', 'Fbare': 1.38 }
        Turbine = { 'min_size': 5.0, 'max_size': 150.0, 'data': (3.4092, 0.4896, 0.0030), 'unit':'kW', 'Fbare': 1.38 }

    def __init__(self, type: Type) -> None:
        self._type = type
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of mixer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(power, CEPCI)        

    def bare_module(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of mixer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(power, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
