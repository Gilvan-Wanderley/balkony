import pytest
from balkony.capital_cost import DriveCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def gas_turbine():
    return (DriveCost(type=DriveCost.Type.GasTurbine), 
            (-21.7702, 13.2175, -1.5279),
            3.51)

@pytest.fixture
def internal_combustion():
    return (DriveCost(type=DriveCost.Type.InternalCombustion), 
            (2.7635, 0.8574, -0.0098),
            2.02)

@pytest.fixture
def steam_turbine():
    return (DriveCost(type=DriveCost.Type.SteamTurbine), 
            (2.6259, 1.4398, -0.1776),
            3.54)

@pytest.fixture
def electric_explosion_proof():
    return (DriveCost(type=DriveCost.Type.ElectricExplosionProof), 
            (2.4604, 1.4191, -0.1798),
            1.50)

@pytest.fixture
def electric_totally_enclosed():
    return (DriveCost(type=DriveCost.Type.ElectricTotallyEnclosed), 
            (1.9560, 1.7142, -0.2282),
            1.5)

@pytest.fixture
def electric_drip_proof():
    return (DriveCost(type=DriveCost.Type.ElectricDripProof), 
            (2.9508, 1.0688, -0.1315),
            1.5)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("gas_turbine", 8000.0, 397),
    ("internal_combustion", 50.0, 397),
    ("steam_turbine", 100.0, 397),
    ("electric_explosion_proof", 100.0, 397),
    ("electric_totally_enclosed", 100.0, 397),
    ("electric_drip_proof", 100.0, 397),
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
    ("gas_turbine", 0.2, 397),
    ("internal_combustion", 1.0, 397),
    ("steam_turbine", 2.0, 397),
    ("electric_explosion_proof", 1.5, 397),
    ("electric_totally_enclosed", 15.0, 397),
    ("electric_drip_proof", 15.0, 397),
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
    ("gas_turbine", 50000.0, 397),
    ("internal_combustion", 20000.0, 397),
    ("steam_turbine", 8000.0, 397),
    ("electric_explosion_proof", 3000.0, 397),
    ("electric_totally_enclosed", 3000.0, 397),
    ("electric_drip_proof", 3000.0, 397),
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
