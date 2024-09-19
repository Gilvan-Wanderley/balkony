import pytest
from balkony.capital_cost import TurbineCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

# Fixtures para diferentes combinações de Turbine Type e Material

@pytest.fixture
def axial_gas_carbon_steel():
    return (TurbineCost(TurbineCost.Type.AxialGas, TurbineCost.Material.CarbonSteel),
            (2.7051, 1.4398, -0.1776),
            TurbineCost.Material.CarbonSteel.value[TurbineCost.Type.AxialGas.name])

@pytest.fixture
def axial_gas_stainless_steel():
    return (TurbineCost(TurbineCost.Type.AxialGas, TurbineCost.Material.StainlessSteel),
            (2.7051, 1.4398, -0.1776),
            TurbineCost.Material.StainlessSteel.value[TurbineCost.Type.AxialGas.name])

@pytest.fixture
def axial_gas_nialloy():
    return (TurbineCost(TurbineCost.Type.AxialGas, TurbineCost.Material.NiAlloy),
            (2.7051, 1.4398, -0.1776),
            TurbineCost.Material.NiAlloy.value[TurbineCost.Type.AxialGas.name])

@pytest.fixture
def radial_gas_carbon_steel():
    return (TurbineCost(TurbineCost.Type.RadialGas, TurbineCost.Material.CarbonSteel),
            (2.2476, 1.4965, -0.1618),
            TurbineCost.Material.CarbonSteel.value[TurbineCost.Type.RadialGas.name])

@pytest.fixture
def radial_gas_stainless_steel():
    return (TurbineCost(TurbineCost.Type.RadialGas, TurbineCost.Material.StainlessSteel),
            (2.2476, 1.4965, -0.1618),
            TurbineCost.Material.StainlessSteel.value[TurbineCost.Type.RadialGas.name])

@pytest.fixture
def radial_gas_nialloy():
    return (TurbineCost(TurbineCost.Type.RadialGas, TurbineCost.Material.NiAlloy),
            (2.2476, 1.4965, -0.1618),
            TurbineCost.Material.NiAlloy.value[TurbineCost.Type.RadialGas.name])

@pytest.fixture
def radial_liquid_carbon_steel():
    return (TurbineCost(TurbineCost.Type.RadialLiquid, TurbineCost.Material.CarbonSteel),
            (2.2476, 1.4965, -0.1618),
            TurbineCost.Material.CarbonSteel.value[TurbineCost.Type.RadialLiquid.name])

@pytest.fixture
def radial_liquid_stainless_steel():
    return (TurbineCost(TurbineCost.Type.RadialLiquid, TurbineCost.Material.StainlessSteel),
            (2.2476, 1.4965, -0.1618),
            TurbineCost.Material.StainlessSteel.value[TurbineCost.Type.RadialLiquid.name])

@pytest.fixture
def radial_liquid_nialloy():
    return (TurbineCost(TurbineCost.Type.RadialLiquid, TurbineCost.Material.NiAlloy),
            (2.2476, 1.4965, -0.1618),
            TurbineCost.Material.NiAlloy.value[TurbineCost.Type.RadialLiquid.name])


@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("axial_gas_carbon_steel", 110.0, 397),
    ("axial_gas_stainless_steel", 120.0, 397),
    ("axial_gas_nialloy", 150.0, 397),
    ("radial_gas_carbon_steel", 110.0, 397),
    ("radial_gas_stainless_steel", 120.0, 397),
    ("radial_gas_nialloy", 150.0, 397),
    ("radial_liquid_carbon_steel", 110.0, 397),
    ("radial_liquid_stainless_steel", 120.0, 397),
    ("radial_liquid_nialloy", 150.0, 397),
])
def test_within_limits(fixture, size, CEPCI, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    bare_value = calculate_bare_module_simple(purchased_value, Fbm)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size)

    assert len(purchased.status) == 1
    assert len(bare.status) == 1
    assert purchased.status['size'][0] == "OK"
    assert bare.status['size'][0] == "OK"
    assert purchased.status['size'][1]
    assert bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE


@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("axial_gas_carbon_steel", 0.5, 397),
    ("axial_gas_stainless_steel", 0.7, 397),
    ("axial_gas_nialloy", 1.0, 397),
    ("radial_gas_carbon_steel", 0.5, 397),
    ("radial_gas_stainless_steel", 0.7, 397),
    ("radial_gas_nialloy", 1.0, 397),
    ("radial_liquid_carbon_steel", 0.5, 397),
    ("radial_liquid_stainless_steel", 0.7, 397),
    ("radial_liquid_nialloy", 1.0, 397),
])
def test_below_limits(fixture, size, CEPCI, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    bare_value = calculate_bare_module_simple(purchased_value, Fbm)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size)

    assert len(purchased.status) == 1
    assert len(bare.status) == 1
    assert purchased.status['size'][0] == "Warning - Below minimum size"
    assert bare.status['size'][0] == "Warning - Below minimum size"
    assert not purchased.status['size'][1]
    assert not bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE


@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("axial_gas_carbon_steel", 5000.0, 397),
    ("axial_gas_stainless_steel", 6000.0, 397),
    ("axial_gas_nialloy", 7000.0, 397),
    ("radial_gas_carbon_steel", 5000.0, 397),
    ("radial_gas_stainless_steel", 6000.0, 397),
    ("radial_gas_nialloy", 7000.0, 397),
    ("radial_liquid_carbon_steel", 5000.0, 397),
    ("radial_liquid_stainless_steel", 6000.0, 397),
    ("radial_liquid_nialloy", 7000.0, 397),
])
def test_above_limits(fixture, size, CEPCI, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    bare_value = calculate_bare_module_simple(purchased_value, Fbm)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size)

    assert len(purchased.status) == 1
    assert len(bare.status) == 1
    assert purchased.status['size'][0] == "Warning - Above maximum size"
    assert bare.status['size'][0] == "Warning - Above maximum size"
    assert not purchased.status['size'][1]
    assert not bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE
