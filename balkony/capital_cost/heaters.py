from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult
from .pressure import HeaterPressure

class HeaterCost:
    class Type(Enum):
        Diphenyl = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (2.2628, 0.8581, 0.0003), 'unit': 'kW', 'Fbare': 2.19}
        MoltenSalt = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (1.1979, 1.4782, -0.0958), 'unit': 'kW', 'Fbare': 2.19}
        HotWater = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (2.0829, 0.9074, -0.0243), 'unit': 'kW', 'Fbare': 2.19}
        SteamBoiler = { 'min_size': 1200.0, 'max_size': 9400.0, 'data': (6.9617, -1.4800, 0.3161), 'unit': 'kW', 'Fbare': 2.19}

    def __init__(self, type: Type) -> None:       
        self._type = type
        self._pressure = HeaterPressure(type.name)
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, duty: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of heater\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(duty, CEPCI)        

    def bare_module(self, duty: float, pressure: float, deltaTemp: float = 0, CEPCI: float = 397) -> EquipmentCostResult:
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
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp.value*Ft)
