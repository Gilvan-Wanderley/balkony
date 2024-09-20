from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class DriveCost:
    class Type(Enum):
        GasTurbine = { 'min_size': 7500.0, 'max_size': 23000.0, 'data': (-21.7702, 13.2175, -1.5279), 'unit':'kW', 'Fbare': 3.51 }
        InternalCombustion = { 'min_size': 10.0, 'max_size': 10000.0, 'data': (2.7635, 0.8574, -0.0098), 'unit':'kW', 'Fbare': 2.02 }
        SteamTurbine = { 'min_size': 70.0, 'max_size': 7500.0, 'data': (2.6259, 1.4398, -0.1776), 'unit':'kW', 'Fbare': 3.54 }
        ElectricExplosionProof = { 'min_size': 75.0, 'max_size': 2600.0, 'data': (2.4604, 1.4191, -0.1798), 'unit':'kW', 'Fbare': 1.50 }
        ElectricTotallyEnclosed = { 'min_size': 75.0, 'max_size': 2600.0, 'data': (1.9560, 1.7142, -0.2282), 'unit':'kW', 'Fbare': 1.5 }
        ElectricDripProof = { 'min_size': 75.0, 'max_size': 2600.0, 'data': (2.9508, 1.0688, -0.1315), 'unit':'kW', 'Fbare': 1.5 }

    def __init__(self, type: Type) -> None:
        self._type = type
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of drive\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(power, CEPCI)        

    def bare_module(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of drive\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._type.value['Fbare']
        cp0 = self._equipment.cost(power, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
