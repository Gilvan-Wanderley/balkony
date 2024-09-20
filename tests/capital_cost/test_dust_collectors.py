import pytest
from balkony.capital_cost import DustCollectorCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def baghouse_dust_collector():
    return (DustCollectorCost(type=DustCollectorCost.Type.Baghouse), 
            (4.5007, 0.4182, 0.0813),
            2.86)

@pytest.fixture
def cyclone_scrubber_dust_collector():
    return (DustCollectorCost(type=DustCollectorCost.Type.CycloneScrubbers), 
            (3.6298, 0.5009, 0.0411),
            2.86)

@pytest.fixture
def electrostatic_precipitator_dust_collector():
    return (DustCollectorCost(type=DustCollectorCost.Type.ElectrostaticPrecipitator), 
            (3.6298, 0.5009, 0.0411),
            2.86)

@pytest.fixture
def venturi_scrubber_dust_collector():
    return (DustCollectorCost(type=DustCollectorCost.Type.VenturiScrubber), 
            (3.6298, 0.5009, 0.0411),
            2.86)

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("baghouse_dust_collector", 100.0, 397),
    ("cyclone_scrubber_dust_collector", 50.0, 397),
    ("electrostatic_precipitator_dust_collector", 150.0, 397),
    ("venturi_scrubber_dust_collector", 100.0, 397),
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
    ("baghouse_dust_collector", 0.05, 397),
    ("cyclone_scrubber_dust_collector", 0.05, 397),
    ("electrostatic_precipitator_dust_collector", 0.05, 397),
    ("venturi_scrubber_dust_collector", 0.05, 397),
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
    ("baghouse_dust_collector", 400.0, 397),
    ("cyclone_scrubber_dust_collector", 300.0, 397),
    ("electrostatic_precipitator_dust_collector", 300.0, 397),
    ("venturi_scrubber_dust_collector", 300.0, 397),
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
