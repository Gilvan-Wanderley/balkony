from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class PackingCost:
    class Material(Enum):
        SS304 = {'Towers': 7.14}
        Polyethylene = {'Towers': 1.03}
        Ceramic = {'Towers': 4.2}

    class Type(Enum):
        Towers = { 'min_size': 0.03, 'max_size': 628.0, 'data': (2.4493, 0.9744, 0.0055), 'unit': 'm3'}

    def __init__(self, type: Type = Type.Towers, material: Material = Material.Polyethylene) -> None:
        self._type = type
        self._material = material
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - volume of packing\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)      

    def bare_module(self, volume: float,CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - volume of packing\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._material.value[self._type.name]
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
