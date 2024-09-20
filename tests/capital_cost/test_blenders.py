import pytest
from balkony.capital_cost import BlenderCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def kneader_blender():
    return (BlenderCost(type=BlenderCost.Type.Kneader), 
            (5.0141, 0.5867, 0.3224),
            1.12)

@pytest.fixture
def ribbon_blender():
    return (BlenderCost(type=BlenderCost.Type.Ribbon), 
            (4.1366, 0.5072, 0.0070),
            1.12)

@pytest.fixture
def rotary_blender():
    return (BlenderCost(type=BlenderCost.Type.Rotary), 
            (4.1366, 0.5072, 0.0070),
            1.12)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("kneader_blender", 1.0, 397),
    ("ribbon_blender", 2.0, 397),
    ("rotary_blender", 3.0, 397),
])
def test_within_limits(fixture, size, CEPCI, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    bare_value = calculate_bare_module_simple(purchased_value, Fbm)

    purchased =  equipment.purchased(size)
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
    ("kneader_blender", 0.1, 397),
    ("ribbon_blender", 0.5, 397),
    ("rotary_blender", 0.5, 397),
])
def test_below_limits(fixture, size, CEPCI, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    bare_value = calculate_bare_module_simple(purchased_value, Fbm)

    purchased =  equipment.purchased(size)
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
    ("kneader_blender", 5.0, 397),
    ("ribbon_blender", 15.0, 397),
    ("rotary_blender", 15.0, 397),
])
def test_above_limits(fixture, size, CEPCI, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    bare_value = calculate_bare_module_simple(purchased_value, Fbm)

    purchased =  equipment.purchased(size)
    bare = equipment.bare_module(size)

    assert len(purchased.status) == 1
    assert len(bare.status) == 1
    assert purchased.status['size'][0] == "Warning - Above maximum size"
    assert bare.status['size'][0] == "Warning - Above maximum size"
    assert not purchased.status['size'][1]
    assert not bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE