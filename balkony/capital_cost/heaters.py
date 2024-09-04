from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, PressureFactor

class HeaterCost:
    class Type(Enum):
        Diphenyl = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (2.2628, 0.8581, 0.0003), 'unit': 'kW', 'Fbare': 2.19}
        MoltenSalt = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (1.1979, 1.4782, -0.0958), 'unit': 'kW', 'Fbare': 2.19}
        HotWater = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (2.0829, 0.9074, -0.0243), 'unit': 'kW', 'Fbare': 2.19}
        SteamBoiler = { 'min_size': 1200.0, 'max_size': 9400.0, 'data': (6.9617, -1.4800, 0.3161), 'unit': 'kW', 'Fbare': 2.19}

    def __init__(self, type: Type) -> None:
        if type.name == 'SteamBoiler':
            self._pressure = PressureFactor([((None, 20), (0.0, 0.0, 0.0)), 
                                             ((20, 40), (0.594072, -4.23476, 1.722404))])
        else:
            self._pressure = PressureFactor([((None, 2), (0.0, 0.0, 0.0)), 
                                             ((2, 200), (-0.01633, 0.056875, -0.00876))])         
        self._type = type
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, duty: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of heater\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(duty, CEPCI)        

    def bare_module(self, duty: float, pressure: float, deltaTemp: float = 0, CEPCI: float = 397) -> float:
        """
            duty (kW) - Duty of heater\n
            pressure (barg) - Operating pressure\n
            deltaTemp (°C) - Amount of superheat
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._type.value['Fbare']
        Ft = 1 + 0.00184*deltaTemp - 0.00000335*(deltaTemp**2)
        Fp = self._pressure.factor(pressure)
        cp0 = self._equipment.cost(duty, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp*Ft)
