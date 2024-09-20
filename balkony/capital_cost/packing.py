from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class PackingCost:
    class Material(Enum):
        SS304 = {'Tower': 7.14}
        Polyethylene = {'Tower': 1.00}
        Ceramic = {'Tower': 4.2}

    class Type(Enum):
        Tower = { 'min_size': 0.03, 'max_size': 628.0, 'data': (2.4493, 0.9744, 0.0055), 'unit': 'm3'}

    def __init__(self, type: Type = Type.Tower, material: Material = Material.Polyethylene) -> None:
        if type.name not in material.value.keys():
            raise Exception(f"Invalid material ({material.name}) for this equipment type ({type.name})")
        self._type, self._material = type, material
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

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
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
