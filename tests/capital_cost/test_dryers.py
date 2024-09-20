import pytest
from balkony.capital_cost import DryerCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def drum_dryer():
    return (DryerCost(type=DryerCost.Type.Drum), 
            (4.5472, 0.2731, 0.1340),
            1.60)

@pytest.fixture
def rotary_dryer():
    return (DryerCost(type=DryerCost.Type.Rotary), 
            (3.5645, 1.1118, -0.0777),
            1.25)

@pytest.fixture
def gasfired_dryer():
    return (DryerCost(type=DryerCost.Type.GasFired), 
            (3.5645, 1.1118, -0.0777),
            1.25)

@pytest.fixture
def tray_dryer():
    return (DryerCost(type=DryerCost.Type.Tray), 
            (3.6951, 0.5442, -0.1248),
            1.25)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("drum_dryer", 20.0, 397),
    ("rotary_dryer", 50.0, 397),
    ("gasfired_dryer", 10.0, 397),
    ("tray_dryer", 15.0, 397),
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
    ("drum_dryer", 0.2, 397),
    ("rotary_dryer", 1.0, 397),
    ("gasfired_dryer", 2.0, 397),
    ("tray_dryer", 1.5, 397),
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
    ("drum_dryer", 60.0, 397),
    ("rotary_dryer", 120.0, 397),
    ("gasfired_dryer", 110.0, 397),
    ("tray_dryer", 25.0, 397),
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
