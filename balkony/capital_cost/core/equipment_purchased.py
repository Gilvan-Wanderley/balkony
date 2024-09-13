import math
from .equipment_properties import EquipmentProperties
from .equipment_result import EquipmentCostResult

class EquipmentPurchased():
    def __init__(self, properties) -> None:
        self._properties: EquipmentProperties = properties

    @property
    def properties(self) -> EquipmentProperties:
        return self._properties
    
    def cost(self, size: float, CEPCI: float = 397) -> EquipmentCostResult:
        K1, K2, K3 = self.properties.data
        log_size = math.log(size,10)
        cp0 = 10**(K1 + K2*log_size + K3*(log_size**2))
        return EquipmentCostResult(status= {'size': self.check_range(size)},
                                   CEPCI= CEPCI,
                                   value= (CEPCI/397.0)*cp0)
    
    def check_range(self, size: float) -> str:
        if size >= self.properties.min_size and size <= self.properties.max_size:
            return ("OK", True)
        elif size < self.properties.min_size:
            return ("Warning - Below minimum size", False)
        else:
            return ("Warning - Above maximum size", False)
