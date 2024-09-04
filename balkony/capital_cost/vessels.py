from enum import Enum
from dataclasses import dataclass
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, PressureFactor

class VesselCost:
    @dataclass(frozen=True)
    class Structure:
        max_stress: float = 944
        min_thickness: float = 0.0063
        corrosion_allowance: float = 0.00315
        weld_efficiency: float = 0.9

        def pressure_factor(self, pressure: float, diameter: float):
            t = (pressure + 1)*diameter/(2*self.max_stress*self.weld_efficiency - 1.2*pressure) + self.corrosion_allowance
            if pressure < -0.5:
                return 1.25
            else:
                Fp = t/self.min_thickness
                if Fp < 1.0:
                    return 1.0
                return Fp

    class Material(Enum):
        CarbonSteel = 1.0
        StainlessSteelClad = 1.75
        StainlessSteel = 3.12
        NiAlloyClad = 3.63
        NiAlloy = 7.09
        TitaniumClad = 4.71
        Titanium = 9.43

    class Type(Enum):
        Horizontal = { 'min_size': 0.1, 'max_size': 628.0, 'data': (3.5565, 0.3776, 0.0905), 'unit': 'm3', 'B1': 1.49, 'B2': 1.52 }
        Vertical = { 'min_size': 0.3, 'max_size': 520.0, 'data': (3.4974, 0.4485, 0.1074), 'unit': 'm3', 'B1': 2.25, 'B2': 1.82 }

    def __init__(self, type: Type, material: Material = Material.CarbonSteel, struct: Structure = Structure()) -> None:
        self._type = type
        self._material = material
        self._structure = struct
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of vessel\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, pressure: float, diameter: float, CEPCI: float = 397) -> float:
        """
            volume (m3) - Volume of vessel\n
            pressure (barg) - Operating pressure\n
            diameter (m) - diameter of vessel\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        Fp = self._structure.pressure_factor(pressure, diameter)
        Fm = self._material.value
        B1 = self._type.value['B1']
        B2 = self._type.value['B1']
        FBM = B1 + B2*Fm*Fp
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
