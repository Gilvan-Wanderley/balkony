from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class TurbineCost:
    class Material(Enum):
        CarbonSteel = {'AxialGas': 3.54, 'RadialGas': 3.54, 'RadialLiquid': 3.54}
        StainlessSteel = {'AxialGas': 6.16, 'RadialGas': 6.16, 'RadialLiquid': 6.16}
        NiAlloy = {'AxialGas': 11.71, 'RadialGas': 11.71, 'RadialLiquid': 11.71}

    class Type(Enum):
        AxialGas = { 'min_size': 100.0, 'max_size': 4000.0, 'data': (2.7051, 1.4398, -0.1776), 'unit':'kW'}
        RadialGas = { 'min_size': 100.0, 'max_size': 1500.0, 'data': (2.2476, 1.4965, -0.1618), 'unit':'kW'}
        RadialLiquid = { 'min_size': 100.0, 'max_size': 1500.0, 'data': (2.2476, 1.4965, -0.1618), 'unit':'kW'}

    def __init__(self, type: Type, material: Material = Material.CarbonSteel) -> None:
        self._type, self._material = type, material
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of turbine\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(power, CEPCI)        

    def bare_module(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of turbine\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._material.value[self._type.name]
        cp0 = self._equipment.cost(power, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
