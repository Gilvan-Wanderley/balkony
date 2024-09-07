from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, PressureFactor

class FurnanceCost:
    class Material(Enum):
        CarbonSteel = {'ReformerFurnace': 2.14, 'PyrolysisFurnace': 2.14, 'NonreactiveFiredHeater': 2.19}
        StainlessSteel = {'ReformerFurnace': 2.54, 'PyrolysisFurnace': 2.54, 'NonreactiveFiredHeater': 2.19}
        AlloySteel = {'ReformerFurnace': 2.82, 'PyrolysisFurnace': 2.82, 'NonreactiveFiredHeater': 2.19}

    class Type(Enum):
        ReformerFurnace = { 'min_size': 3000.0, 'max_size': 100000.0, 'data': (3.0680, 0.6597, 0.0194), 'unit':'kW' }
        PyrolysisFurnace = { 'min_size': 3000.0, 'max_size': 100000.0, 'data': (2.3859, 0.9721, -0.0206), 'unit':'kW' }
        NonreactiveFiredHeater = { 'min_size': 1000.0, 'max_size': 100000.0, 'data': (7.3488, -1.1666, 0.2028), 'unit':'kW' }

    def __init__(self, type: Type, material: Material = Material.CarbonSteel) -> None:
        if type.name == 'ReformerFurnace':
            self._pressure = PressureFactor([((None, 10), (0.0, 0.0, 0.0)), 
                                             ((10, 200), (0.1405,-0.2698, 0.1293))])
        elif type.name == 'PyrolysisFurnace':
            self._pressure = PressureFactor([((None, 10), (0.0, 0.0, 0.0)), 
                                             ((10, 200), (0.1017, -0.1957, 0.09403))])
        else:
            self._pressure = PressureFactor([((None, 10), (0.0, 0.0, 0.0)), 
                                             ((10, 200), (0.1347, -0.2368, 0.1021))])         
        self._type = type
        self._material = material
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, duty: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of furnace\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(duty, CEPCI)        

    def bare_module(self, duty: float, pressure: float, deltaTemp: float = 0, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of furnace\n
            pressure (barg) - Operating pressure\n
            deltaTemp (°C) - Amount of superheat
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._material.value[self._type.name]
        Ft = 1 + 0.00184*deltaTemp - 0.00000335*(deltaTemp**2)
        Fp = self._pressure.factor(pressure)
        cp0 = self._equipment.cost(duty, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp*Ft)
