import pytest
from balkony.capital_cost import VaporizerCost
from balkony.capital_cost.pressure import VaporizerPressure
from utils import calculate_bare_module_pressure, calculate_purchased

TOLERANCE = 1e-6

@pytest.fixture
def internal_coils_carbon_steel():
    return (VaporizerCost(VaporizerCost.Type.InternalCoils, VaporizerCost.Material.CarbonSteel),
            (4.0000, 0.4321, 0.1700),
            VaporizerCost.Material.CarbonSteel.value[VaporizerCost.Type.InternalCoils.name])

@pytest.fixture
def jacketed_vessels_carbon_steel():
    return (VaporizerCost(VaporizerCost.Type.JacketedVessels, VaporizerCost.Material.CarbonSteel),
            (3.8751, 0.3328, 0.1901),
            VaporizerCost.Material.CarbonSteel.value[VaporizerCost.Type.JacketedVessels.name])

@pytest.fixture
def internal_coils_copper():
    return (VaporizerCost(VaporizerCost.Type.InternalCoils, VaporizerCost.Material.Copper),
            (4.0000, 0.4321, 0.1700),
            VaporizerCost.Material.Copper.value[VaporizerCost.Type.InternalCoils.name])

@pytest.fixture
def jacketed_vessels_copper():
    return (VaporizerCost(VaporizerCost.Type.JacketedVessels, VaporizerCost.Material.Copper),
            (3.8751, 0.3328, 0.1901),
            VaporizerCost.Material.Copper.value[VaporizerCost.Type.JacketedVessels.name])

@pytest.fixture
def internal_coils_glass_ss():
    return (VaporizerCost(VaporizerCost.Type.InternalCoils, VaporizerCost.Material.GlassSS),
            (4.0000, 0.4321, 0.1700),
            VaporizerCost.Material.GlassSS.value[VaporizerCost.Type.InternalCoils.name])

@pytest.fixture
def jacketed_vessels_glass_ss():
    return (VaporizerCost(VaporizerCost.Type.JacketedVessels, VaporizerCost.Material.GlassSS),
            (3.8751, 0.3328, 0.1901),
            VaporizerCost.Material.GlassSS.value[VaporizerCost.Type.JacketedVessels.name])

@pytest.mark.parametrize("fixture, size, CEPCI, pressure", [
    ("internal_coils_carbon_steel", 10.0, 397, 100),
    ("jacketed_vessels_carbon_steel", 12.0, 397, 100),
    ("internal_coils_copper", 15.0, 397, 100),
    ("jacketed_vessels_copper", 20.0, 397, 100),
    ("internal_coils_glass_ss", 25.0, 397, 100),
    ("jacketed_vessels_glass_ss", 30.0, 397, 100),
])
def test_within_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = VaporizerPressure().factor(pressure).value
    bare_value = calculate_bare_module_pressure(purchased_value, Fbm, pressure_fac)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size, pressure)

    assert len(purchased.status) == 1
    assert len(bare.status) == 2
    assert purchased.status['size'][0] == "OK"
    assert bare.status['size'][0] == "OK"
    assert bare.status['pressure'][0] == "OK"
    assert purchased.status['size'][1]
    assert bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE

@pytest.mark.parametrize("fixture, size, CEPCI, pressure", [
    ("internal_coils_carbon_steel", 0.5, 397, 100),
    ("jacketed_vessels_carbon_steel", 0.7, 397, 100),
    ("internal_coils_copper", 0.8, 397, 100),
    ("jacketed_vessels_copper", 0.8, 397, 100),
    ("internal_coils_glass_ss", 0.9, 397, 100),
    ("jacketed_vessels_glass_ss", 0.6, 397, 100),
])
def test_below_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = VaporizerPressure().factor(pressure).value
    bare_value = calculate_bare_module_pressure(purchased_value, Fbm, pressure_fac)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size, pressure)

    assert len(purchased.status) == 1
    assert len(bare.status) == 2
    assert purchased.status['size'][0] == "Warning - Below minimum size"
    assert bare.status['size'][0] == "Warning - Below minimum size"
    assert bare.status['pressure'][0] == "OK"
    assert not purchased.status['size'][1]
    assert not bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE

@pytest.mark.parametrize("fixture, size, CEPCI, pressure", [
    ("internal_coils_carbon_steel", 150.0, 397, 100),
    ("jacketed_vessels_carbon_steel", 160.0, 397, 100),
    ("internal_coils_copper", 170.0, 397, 100),
    ("jacketed_vessels_copper", 180.0, 397, 100),
    ("internal_coils_glass_ss", 190.0, 397, 100),
    ("jacketed_vessels_glass_ss", 200.0, 397, 100),
])
def test_above_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = VaporizerPressure().factor(pressure).value
    bare_value = calculate_bare_module_pressure(purchased_value, Fbm, pressure_fac)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size, pressure)

    assert len(purchased.status) == 1
    assert len(bare.status) == 2
    assert purchased.status['size'][0] == "Warning - Above maximum size"
    assert bare.status['size'][0] == "Warning - Above maximum size"
    assert bare.status['pressure'][0] == "OK"
    assert not purchased.status['size'][1]
    assert not bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE
