from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult
from .pressure import VaporizerPressure

class VaporizerCost:
    class Material(Enum):
        CarbonSteel = {'InternalCoils': 3.04, 'JacketedVessels': 2.73}
        Copper = {'InternalCoils': 3.83, 'JacketedVessels': 3.45}
        GlassSS = {'InternalCoils': 5.19, 'JacketedVessels': 4.67}
        GlassNi = {'InternalCoils': 5.49, 'JacketedVessels': 4.95}
        StainlessSteel = {'InternalCoils': 5.19, 'JacketedVessels': 4.81}
        StainlessSteelClad = {'InternalCoils': 4.16, 'JacketedVessels': 3.83}
        NiAlloy = {'InternalCoils': 10.14, 'JacketedVessels': 9.15}
        NiAlloyClad = {'InternalCoils': 6.64, 'JacketedVessels': 6.00}
        Titanium = {'InternalCoils': 15.23, 'JacketedVessels': 13.78}
        TitaniumClad = {'InternalCoils': 10.66, 'JacketedVessels': 9.69}

    class Type(Enum):
        InternalCoils = { 'min_size': 1.0, 'max_size': 100.0, 'data': (4.0000, 0.4321, 0.1700), 'unit':'m3'}
        JacketedVessels = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.8751, 0.3328, 0.1901), 'unit':'m3'}

    def __init__(self, type: Type, material: Material = Material.CarbonSteel) -> None:
        if type.name not in material.value.keys():
            raise Exception(f"Invalid material ({material.name}) for this equipment type ({type.name})")
        self._type, self._material = type, material
        self._pressure = VaporizerPressure()           
        self._equipment = EquipmentPurchased(EquipmentProperties(data=type.value['data'],
                                                                 unit=type.value['unit'],
                                                                 min_size=type.value['min_size'],
                                                                 max_size=type.value['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Gas volume of vaporizer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, pressure: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of vaporizer\n
            pressure (barg) - Operating pressure\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._material.value[self._type.name]
        Fp = self._pressure.factor(pressure)
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp.value)
