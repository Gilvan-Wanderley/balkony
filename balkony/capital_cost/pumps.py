from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, PressureFactor

class PumpCost:
    class Material(Enum):
        CastIron = {'Reciprocating': 1.00, 'PositiveDisplacement': 1.00, 'Centrifugal': 1.0}
        CarbonSteel = {'Reciprocating': 1.45, 'PositiveDisplacement': 1.42, 'Centrifugal': 1.54}
        CuAlloy = {'Reciprocating': 1.29, 'PositiveDisplacement': 1.29}
        StainlessSteel = {'Reciprocating': 2.35, 'PositiveDisplacement': 2.66, 'Centrifugal': 2.31}
        NiAlloy = {'Reciprocating': 3.96, 'PositiveDisplacement': 4.75, 'Centrifugal': 4.36}
        Titanium = {'Reciprocating': 6.45, 'PositiveDisplacement': 10.68}

    class Type(Enum):
        Reciprocating = { 'min_size': 0.1, 'max_size': 200.0, 'data': (3.8696, 0.3161, 0.1220), 'unit': 'kW', 'B1':1.89, 'B2': 1.35 }
        PositiveDisplacement = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.4771, 0.1350, 0.1438), 'unit': 'kW', 'B1':1.89, 'B2': 1.35 }
        Centrifugal = { 'min_size': 1.0, 'max_size': 300.0, 'data': (3.3892, 0.0536, 0.1538), 'unit': 'kW', 'B1':1.89, 'B2': 1.35 }

    def __init__(self, type: Type, material: Material = Material.CarbonSteel) -> None:
        if type.name == 'Centrifugal':            
            self._pressure = PressureFactor([((None, 10), (0.0, 0.0, 0.0)), 
                                             ((10, 100), (0.1347, -0.2368, 0.1021))])
        else:
            self._pressure = PressureFactor([((None, 10), (0.0, 0.0, 0.0)), 
                                             ((10, 100), (-0.3935, 0.3957, -0.00226))])      
        self._type = type
        self._material = material
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - power of pump\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(power, CEPCI)        

    def bare_module(self, power: float, pressure: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - power of pump\n
            pressure (barg) - Operating pressure\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        Fm = self._material.value[self._type.name]
        Fp = self._pressure.factor(pressure)
        B1 = self._type.value['B1']
        B2 = self._type.value['B1']
        FBM = B1 + B2*Fm*Fp
        cp0 = self._equipment.cost(power, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
