from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult

class DustCollectorCost:
    class Type(Enum):
        Baghouse = { 'min_size': 0.08, 'max_size': 350.0, 'data': (4.5007, 0.4182, 0.0813), 'unit':'m3', 'Fbare': 2.86}
        CycloneScrubbers =  { 'min_size': 0.06, 'max_size': 200.0, 'data': (3.6298, 0.5009, 0.0411), 'unit':'m3', 'Fbare': 2.86 }
        ElectrostaticPrecipitator = { 'min_size': 0.06, 'max_size':200.0, 'data': (3.6298, 0.5009, 0.0411), 'unit':'m3', 'Fbare': 2.86 }
        VenturiScrubber = { 'min_size': 0.06, 'max_size': 200.0, 'data': (3.6298, 0.5009, 0.0411), 'unit':'m3', 'Fbare': 2.86 }

    def __init__(self, type: Type) -> None:
        self._type = type
        values = type.value
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=values['data'],
                                                                                     unit=values['unit'],
                                                                                     min_size=values['min_size'],
                                                                                     max_size=values['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of dust collectors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of dust collectors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._type.value['Fbare']
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(range_status= cp0.range_status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
