import pytest
from balkony.capital_cost import CentrifugeCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def apron_centrifuge():
    return (CentrifugeCost(type=CentrifugeCost.Type.Apron), 
            (3.9255, 0.5039, 0.1506),
            1.20)

@pytest.fixture
def belt_centrifuge():
    return (CentrifugeCost(type=CentrifugeCost.Type.Belt), 
            (4.0637, 0.2584, 0.1550),
            1.25)

@pytest.fixture
def pneumatic_centrifuge():
    return (CentrifugeCost(type=CentrifugeCost.Type.Pneumatic), 
            (4.6616, 0.3205, 0.0638),
            1.25)

@pytest.fixture
def screw_centrifuge():
    return (CentrifugeCost(type=CentrifugeCost.Type.Screw), 
            (3.6062, 0.2659, 0.1982),
            1.10)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("apron_centrifuge", 3.0, 397),
    ("belt_centrifuge", 2.0, 397),
    ("pneumatic_centrifuge", 3.0, 397),
    ("screw_centrifuge", 4.0, 397),
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
    ("apron_centrifuge", 0.5, 397),
    ("belt_centrifuge", 0.4, 397),
    ("pneumatic_centrifuge", 0.6, 397),
    ("screw_centrifuge", 0.3, 397),
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
    ("apron_centrifuge", 16.0, 397),
    ("belt_centrifuge", 350.0, 397),
    ("pneumatic_centrifuge", 70.0, 397),
    ("screw_centrifuge", 31.0, 397),
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
