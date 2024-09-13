import pytest
from balkony.capital_cost import FilterCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def bent_filter():
    return (FilterCost(type=FilterCost.Type.Bent), 
            (5.1055, 0.4999, 0.0001),
            1.65)

@pytest.fixture
def cartridge_filter():
    return (FilterCost(type=FilterCost.Type.Cartridge), 
            (3.2107, 0.7597, 0.0027),
            1.65)

@pytest.fixture
def disc_filter():
    return (FilterCost(type=FilterCost.Type.Disc), 
            (4.8123, 0.2858, 0.0420),
            1.65)

@pytest.fixture
def drum_filter():
    return (FilterCost(type=FilterCost.Type.Drum), 
            (4.8123, 0.2858, 0.0420),
            1.65)

@pytest.fixture
def gravity_filter():
    return (FilterCost(type=FilterCost.Type.Gravity), 
            (4.2756, 0.3520, 0.0714),
            1.65)

@pytest.fixture
def leaf_filter():
    return (FilterCost(type=FilterCost.Type.Leaf), 
            (3.8187, 0.6235, 0.0176),
            1.65)

@pytest.fixture
def pan_filter():
    return (FilterCost(type=FilterCost.Type.Pan), 
            (4.8123, 0.2858, 0.0420),
            1.65)

@pytest.fixture
def plate_filter():
    return (FilterCost(type=FilterCost.Type.Plate), 
            (4.2756, 0.3520, 0.0714),
            1.80)

@pytest.fixture
def frame_filter():
    return (FilterCost(type=FilterCost.Type.Frame), 
            (4.2756, 0.3520, 0.0714),
            1.80)

@pytest.fixture
def table_filter():
    return (FilterCost(type=FilterCost.Type.Table), 
            (5.1055, 0.4999, 0.0001),
            1.65)

@pytest.fixture
def tube_filter():
    return (FilterCost(type=FilterCost.Type.Tube), 
            (5.1055, 0.4999, 0.0001),
            1.65)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("bent_filter", 10.0, 397),
    ("cartridge_filter", 20.0, 397),
    ("disc_filter", 30.0, 397),
    ("drum_filter", 30.0, 397),
    ("gravity_filter", 10.0, 397),
    ("leaf_filter", 15.0, 397),
    ("pan_filter", 25.0, 397),
    ("plate_filter", 20.0, 397),
    ("frame_filter", 20.0, 397),
    ("table_filter", 30.0, 397),
    ("tube_filter", 25.0, 397),
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
    ("bent_filter", 0.1, 397),
    ("cartridge_filter", 5.0, 397),
    ("disc_filter", 0.8, 397),
    ("drum_filter", 0.8, 397),
    ("gravity_filter", 0.2, 397),
    ("leaf_filter", 0.5, 397),
    ("pan_filter", 0.8, 397),
    ("plate_filter", 0.4, 397),
    ("frame_filter", 0.4, 397),
    ("table_filter", 0.8, 397),
    ("tube_filter", 0.8, 397),
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
    ("bent_filter", 200.0, 397),
    ("cartridge_filter", 250.0, 397),
    ("disc_filter", 350.0, 397),
    ("drum_filter", 350.0, 397),
    ("gravity_filter", 100.0, 397),
    ("leaf_filter", 300.0, 397),
    ("pan_filter", 350.0, 397),
    ("plate_filter", 90.0, 397),
    ("frame_filter", 90.0, 397),
    ("table_filter", 120.0, 397),
    ("tube_filter", 120.0, 397),
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
