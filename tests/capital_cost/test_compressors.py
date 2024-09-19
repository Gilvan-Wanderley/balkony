import pytest
from balkony.capital_cost import CompressorCost
from utils import calculate_purchased, calculate_bare_module_simple

TOLERANCE = 1e-6

@pytest.fixture
def centrifugal_carbon_steel():
    return (CompressorCost(CompressorCost.Type.Centrifugal, CompressorCost.Material.CarbonSteel),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.CarbonSteel.value[CompressorCost.Type.Centrifugal.name])

@pytest.fixture
def centrifugal_stainless_steel():
    return (CompressorCost(CompressorCost.Type.Centrifugal, CompressorCost.Material.StainlessSteel),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.StainlessSteel.value[CompressorCost.Type.Centrifugal.name])

@pytest.fixture
def centrifugal_nialloy():
    return (CompressorCost(CompressorCost.Type.Centrifugal, CompressorCost.Material.NiAlloy),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.NiAlloy.value[CompressorCost.Type.Centrifugal.name])

@pytest.fixture
def reciprocating_carbon_steel():
    return (CompressorCost(CompressorCost.Type.Reciprocating, CompressorCost.Material.CarbonSteel),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.CarbonSteel.value[CompressorCost.Type.Reciprocating.name])

@pytest.fixture
def reciprocating_stainless_steel():
    return (CompressorCost(CompressorCost.Type.Reciprocating, CompressorCost.Material.StainlessSteel),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.StainlessSteel.value[CompressorCost.Type.Reciprocating.name])

@pytest.fixture
def reciprocating_nialloy():
    return (CompressorCost(CompressorCost.Type.Reciprocating, CompressorCost.Material.NiAlloy),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.NiAlloy.value[CompressorCost.Type.Reciprocating.name])

@pytest.fixture
def axial_carbon_steel():
    return (CompressorCost(CompressorCost.Type.Axial, CompressorCost.Material.CarbonSteel),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.CarbonSteel.value[CompressorCost.Type.Axial.name])

@pytest.fixture
def axial_stainless_steel():
    return (CompressorCost(CompressorCost.Type.Axial, CompressorCost.Material.StainlessSteel),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.StainlessSteel.value[CompressorCost.Type.Axial.name])

@pytest.fixture
def axial_nialloy():
    return (CompressorCost(CompressorCost.Type.Axial, CompressorCost.Material.NiAlloy),
            (2.2897, 1.3604, -0.1027),
            CompressorCost.Material.NiAlloy.value[CompressorCost.Type.Axial.name])

@pytest.fixture
def rotary_carbon_steel():
    return (CompressorCost(CompressorCost.Type.Rotary, CompressorCost.Material.CarbonSteel),
            (5.0355, -1.8002, 0.8253),
            CompressorCost.Material.CarbonSteel.value[CompressorCost.Type.Rotary.name])

@pytest.fixture
def rotary_stainless_steel():
    return (CompressorCost(CompressorCost.Type.Rotary, CompressorCost.Material.StainlessSteel),
            (5.0355, -1.8002, 0.8253),
            CompressorCost.Material.StainlessSteel.value[CompressorCost.Type.Rotary.name])

@pytest.fixture
def rotary_nialloy():
    return (CompressorCost(CompressorCost.Type.Rotary, CompressorCost.Material.NiAlloy),
            (5.0355, -1.8002, 0.8253),
            CompressorCost.Material.NiAlloy.value[CompressorCost.Type.Rotary.name])

@pytest.mark.parametrize("fixture, size, CEPCI", [
    ("centrifugal_carbon_steel", 460.0, 397),
    ("centrifugal_stainless_steel", 460.0, 397),
    ("centrifugal_nialloy", 460.0, 397),
    ("reciprocating_carbon_steel", 600.0, 397),
    ("reciprocating_stainless_steel",600.0, 397),
    ("reciprocating_nialloy", 600.0, 397),
    ("axial_carbon_steel", 500.0, 397),
    ("axial_stainless_steel", 500.0, 397),
    ("axial_nialloy", 500.0, 397),
    ("rotary_carbon_steel", 50.0, 397),
    ("rotary_stainless_steel", 50.0, 397),
    ("rotary_nialloy", 50.0, 397),
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
    ("centrifugal_carbon_steel", 0.5, 397),
    ("centrifugal_stainless_steel", 0.7, 397),
    ("centrifugal_nialloy", 0.8, 397),
    ("reciprocating_carbon_steel", 1.0, 397),
    ("reciprocating_stainless_steel", 1.2, 397),
    ("reciprocating_nialloy", 1.5, 397),
    ("axial_carbon_steel", 2.0, 397),
    ("axial_stainless_steel", 2.5, 397),
    ("axial_nialloy", 3.0, 397),
    ("rotary_carbon_steel", 1.5, 397),
    ("rotary_stainless_steel", 1.8, 397),
    ("rotary_nialloy", 2.0, 397),
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
    ("centrifugal_carbon_steel", 3500.0, 397),
    ("centrifugal_stainless_steel", 3500.0, 397),
    ("centrifugal_nialloy", 3500.0, 397),
    ("reciprocating_carbon_steel", 3600.0, 397),
    ("reciprocating_stainless_steel", 3600.0, 397),
    ("reciprocating_nialloy", 3600.0, 397),
    ("axial_carbon_steel", 3200.0, 397),
    ("axial_stainless_steel", 3200.0, 397),
    ("axial_nialloy", 3200.0, 397),
    ("rotary_carbon_steel", 1000.0, 397),
    ("rotary_stainless_steel", 1000.0, 397),
    ("rotary_nialloy", 1000.0, 397),
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