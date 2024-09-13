import pytest
from balkony.capital_cost import ReactorCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def autoclave_reactor():
    return (ReactorCost(type=ReactorCost.Type.Autoclave), 
            (4.5587, 0.2986, 0.0020),
            4.0)

@pytest.fixture
def fermenter_reactor():
    return (ReactorCost(type=ReactorCost.Type.Fermenter), 
            (4.1052, 0.5320, -0.0005),
            4.0)

@pytest.fixture
def inoculum_tank_reactor():
    return (ReactorCost(type=ReactorCost.Type.Inoculum_Tank), 
            (3.7957, 0.4593, 0.0160),
            4.0)

@pytest.fixture
def jacketed_agitated_reactor():
    return (ReactorCost(type=ReactorCost.Type.JacketedAgitated), 
            (4.1052, 0.5320, -0.0005),
            4.0)

@pytest.fixture
def jacketed_nonagitated_reactor():
    return (ReactorCost(type=ReactorCost.Type.JacketedNonagitated), 
            (3.3496, 0.7235, 0.0025),
            4.0)

@pytest.fixture
def mixer_reactor():
    return (ReactorCost(type=ReactorCost.Type.Mixer), 
            (4.7116, 0.4479, 0.0004),
            4.0)

@pytest.fixture
def settler_reactor():
    return (ReactorCost(type=ReactorCost.Type.Settler), 
            (4.7116, 0.4479, 0.0004),
            4.0)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("autoclave_reactor", 5.0, 397),
    ("fermenter_reactor", 10.0, 397),
    ("inoculum_tank_reactor", 0.5, 397),
    ("jacketed_agitated_reactor", 15.0, 397),
    ("jacketed_nonagitated_reactor", 10.0, 397),
    ("mixer_reactor", 20.0, 397),
    ("settler_reactor", 25.0, 397),
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
    ("autoclave_reactor", 0.5, 397),
    ("fermenter_reactor", 0.05, 397),
    ("inoculum_tank_reactor", 0.03, 397),
    ("jacketed_agitated_reactor", 0.05, 397),
    ("jacketed_nonagitated_reactor", 3.0, 397),
    ("mixer_reactor", 0.3, 397),
    ("settler_reactor", 0.3, 397),
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
    ("autoclave_reactor", 20.0, 397),
    ("fermenter_reactor", 40.0, 397),
    ("inoculum_tank_reactor", 2.0, 397),
    ("jacketed_agitated_reactor", 50.0, 397),
    ("jacketed_nonagitated_reactor", 60.0, 397),
    ("mixer_reactor", 70.0, 397),
    ("settler_reactor", 70.0, 397),
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
