import math
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class TrayCost:
    class Material(Enum):
        CarbonSteel = {'Sieve': 1.05, 'Valve': 1.05, 'Demisters': 1.05}
        StainlessSteel = {'Sieve': 1.89, 'Valve': 1.89, 'Demisters': 1.05}
        NiAlloy = {'Sieve': 5.6, 'Valve': 5.6, 'Demisters': 5.6}
        Fluorocarbon = {'Sieve': 1.84, 'Valve': 1.84, 'Demisters': 1.84}

    class Type(Enum):
        Sieve = { 'min_size': 0.07, 'max_size': 12.3, 'data': (2.9949, 0.4465, 0.3961), 'unit': 'm2'}
        Valve = { 'min_size': 0.7, 'max_size': 10.5, 'data': (3.3322, 0.4838, 0.3434), 'unit': 'm2'}
        Demisters = { 'min_size': 0.7, 'max_size': 10.5, 'data': (3.2353, 0.4838, 0.3434), 'unit': 'm2'}

    def __init__(self, type: Type, material: Material = Material.CarbonSteel) -> None:
        self._type, self._material = type, material
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, area: float, num_trays: int,  CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of tray\n
            num_trays (-) - number of trays\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*num_trays)       

    def bare_module(self, area: float, num_trays: int,CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of tray\n
            num_trays (-) - number of trays\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        if num_trays >= 20:
            Fq = 1
        else:
            Fq = 0.4771 + 0.08516*(math.log10(num_trays)) - 0.3473*(math.log10(num_trays)**2)
        FBM = self._material.value[self._type.name]
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fq*num_trays)
