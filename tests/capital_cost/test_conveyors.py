import pytest
from balkony.capital_cost import ConveyorCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def autobatch_conveyor():
    return (ConveyorCost(type=ConveyorCost.Type.AutoBatch), 
            (4.7681, 0.9740, 0.0240),
            1.20)

@pytest.fixture
def centrifugal_conveyor():
    return (ConveyorCost(type=ConveyorCost.Type.Centrifugal), 
            (4.3657, 0.8764, -0.0049),
            1.25)

@pytest.fixture
def oscillating_screen_conveyor():
    return (ConveyorCost(type=ConveyorCost.Type.OscillatingScreen), 
            (4.8600, 0.3340, 0.1063),
            1.25)

@pytest.fixture
def solid_bowl_conveyor():
    return (ConveyorCost(type=ConveyorCost.Type.SolidBowl), 
            (4.9697, 1.1689, 0.0038),
            1.10)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("autobatch_conveyor", 1.0, 397),
    ("centrifugal_conveyor", 0.7, 397),
    ("oscillating_screen_conveyor", 1.0, 397),
    ("solid_bowl_conveyor", 1.8, 397),
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
    ("autobatch_conveyor", 0.1, 397),
    ("centrifugal_conveyor", 0.4, 397),
    ("oscillating_screen_conveyor", 0.3, 397),
    ("solid_bowl_conveyor", 0.2, 397),
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
    ("autobatch_conveyor", 2.0, 397),
    ("centrifugal_conveyor", 2.0, 397),
    ("oscillating_screen_conveyor", 2.0, 397),
    ("solid_bowl_conveyor", 2.5, 397),
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
