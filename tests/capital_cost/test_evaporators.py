import pytest
from balkony.capital_cost import EvaporatorCost
from balkony.capital_cost.pressure import EvaporatorPressure
from utils import calculate_bare_module_pressure, calculate_purchased

TOLERANCE = 1e-6

@pytest.fixture
def forced_circulation_carbon_steel():
    return (EvaporatorCost(EvaporatorCost.Type.ForcedCirculation, EvaporatorCost.Material.CarbonSteel),
            (5.0238, 0.3475, 0.0703),
            EvaporatorCost.Material.CarbonSteel.value[EvaporatorCost.Type.ForcedCirculation.name])

@pytest.fixture
def falling_film_carbon_steel():
    return (EvaporatorCost(EvaporatorCost.Type.FallingFilm, EvaporatorCost.Material.CarbonSteel),
            (3.9119, 0.8627, -0.0088),
            EvaporatorCost.Material.CarbonSteel.value[EvaporatorCost.Type.FallingFilm.name])

@pytest.fixture
def agitated_film_stainless_steel():
    return (EvaporatorCost(EvaporatorCost.Type.AgitatedFilm, EvaporatorCost.Material.StainlessSteel),
            (5.0000, 0.1490, -0.0134),
            EvaporatorCost.Material.StainlessSteel.value[EvaporatorCost.Type.AgitatedFilm.name])

@pytest.fixture
def short_tube_ni_alloy():
    return (EvaporatorCost(EvaporatorCost.Type.ShortTube, EvaporatorCost.Material.NiAlloy),
            (5.2366, -0.6572, 0.3500),
            EvaporatorCost.Material.NiAlloy.value[EvaporatorCost.Type.ShortTube.name])

@pytest.fixture
def long_tube_titanium():
    return (EvaporatorCost(EvaporatorCost.Type.LongTube, EvaporatorCost.Material.Titanium),
            (4.6420, 0.3698, 0.0025),
            EvaporatorCost.Material.Titanium.value[EvaporatorCost.Type.LongTube.name])


@pytest.mark.parametrize("fixture, size, CEPCI, pressure", [
    ("forced_circulation_carbon_steel", 100.0, 397, 100),
    ("falling_film_carbon_steel", 150.0, 397, 100),
    ("agitated_film_stainless_steel", 3.0, 397, 100),
    ("short_tube_ni_alloy", 50.0, 397, 100),
    ("long_tube_titanium", 500.0, 397, 100),
])
def test_within_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = EvaporatorPressure().factor(pressure).value
    bare_value = calculate_bare_module_pressure(purchased_value, Fbm, pressure_fac)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size, pressure)

    assert len(purchased.status) == 1
    assert len(bare.status) == 2
    assert purchased.status['size'][0] == "OK"
    assert bare.status['size'][0] == "OK"
    assert bare.status['pressure'][0] == "OK"
    assert purchased.status['size'][1]
    assert bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE


@pytest.mark.parametrize("fixture, size, CEPCI, pressure", [
    ("forced_circulation_carbon_steel", 4.0, 397, 100),
    ("falling_film_carbon_steel", 40.0, 397, 100),
    ("agitated_film_stainless_steel", 0.3, 397, 100),
    ("short_tube_ni_alloy", 5.0, 397, 100),
    ("long_tube_titanium", 80.0, 397, 100),
])
def test_below_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = EvaporatorPressure().factor(pressure).value
    bare_value = calculate_bare_module_pressure(purchased_value, Fbm, pressure_fac)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size, pressure)

    assert len(purchased.status) == 1
    assert len(bare.status) == 2
    assert purchased.status['size'][0] == "Warning - Below minimum size"
    assert bare.status['size'][0] == "Warning - Below minimum size"
    assert bare.status['pressure'][0] == "OK"
    assert not purchased.status['size'][1]
    assert not bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE


@pytest.mark.parametrize("fixture, size, CEPCI, pressure", [
    ("forced_circulation_carbon_steel", 1500.0, 397, 100),
    ("falling_film_carbon_steel", 600.0, 397, 100),
    ("agitated_film_stainless_steel", 6.0, 397, 100),
    ("short_tube_ni_alloy", 200.0, 397, 100),
    ("long_tube_titanium", 15000.0, 397, 100),
])
def test_above_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = EvaporatorPressure().factor(pressure).value
    bare_value = calculate_bare_module_pressure(purchased_value, Fbm, pressure_fac)

    purchased = equipment.purchased(size)
    bare = equipment.bare_module(size, pressure)

    assert len(purchased.status) == 1
    assert len(bare.status) == 2
    assert purchased.status['size'][0] == "Warning - Above maximum size"
    assert bare.status['size'][0] == "Warning - Above maximum size"
    assert bare.status['pressure'][0] == "OK"
    assert not purchased.status['size'][1]
    assert not bare.status['size'][1]
    assert abs(purchased.value - purchased_value) < TOLERANCE
    assert abs(bare.value - bare_value) < TOLERANCE
