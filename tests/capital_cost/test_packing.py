import pytest
from balkony.capital_cost import PackingCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def tower_ss304():
    return (PackingCost(PackingCost.Type.Tower, PackingCost.Material.SS304),
            (2.4493, 0.9744, 0.0055),
            PackingCost.Material.SS304.value[PackingCost.Type.Tower.name])

@pytest.fixture
def tower_polyethylene():
    return (PackingCost(PackingCost.Type.Tower, PackingCost.Material.Polyethylene),
            (2.4493, 0.9744, 0.0055),
            PackingCost.Material.Polyethylene.value[PackingCost.Type.Tower.name])

@pytest.fixture
def tower_ceramic():
    return (PackingCost(PackingCost.Type.Tower, PackingCost.Material.Ceramic),
            (2.4493, 0.9744, 0.0055),
            PackingCost.Material.Ceramic.value[PackingCost.Type.Tower.name])


@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("tower_ss304", 100.0, 397),
    ("tower_polyethylene", 120.0, 397),
    ("tower_ceramic", 150.0, 397),
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
    ("tower_ss304", 0.02, 397),
    ("tower_polyethylene", 0.02, 397),
    ("tower_ceramic", 0.02, 397),
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
    ("tower_ss304", 700.0, 397),
    ("tower_polyethylene", 700.0, 397),
    ("tower_ceramic", 700.0, 397),
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
