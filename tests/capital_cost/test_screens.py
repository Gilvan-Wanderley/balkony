import pytest
from balkony.capital_cost import ScreenCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def dsm_screen():
    return (ScreenCost(type=ScreenCost.Type.DSM), 
            (3.8050, 0.5856, 0.2120),
            1.34)

@pytest.fixture
def rotary_screen():
    return (ScreenCost(type=ScreenCost.Type.Rotary), 
            (4.0485, 0.1118, 0.3260),
            1.34)

@pytest.fixture
def stationary_screen():
    return (ScreenCost(type=ScreenCost.Type.Stationary), 
            (3.8219, 1.0368, -0.6050),
            1.34)

@pytest.fixture
def vibrating_screen():
    return (ScreenCost(type=ScreenCost.Type.Vibrating), 
            (4.0185, 0.1118, 0.3260),
            1.34)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("dsm_screen", 1.0, 397),
    ("rotary_screen", 3.0, 397),
    ("stationary_screen", 5.0, 397),
    ("vibrating_screen", 4.0, 397),
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
    ("dsm_screen", 0.2, 397),
    ("rotary_screen", 0.2, 397),
    ("stationary_screen", 1.5, 397),
    ("vibrating_screen", 0.2, 397),
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
    ("dsm_screen", 7.0, 397),
    ("rotary_screen", 16.0, 397),
    ("stationary_screen", 12.0, 397),
    ("vibrating_screen", 16.0, 397),
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