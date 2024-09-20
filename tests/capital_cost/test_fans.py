import pytest
from balkony.capital_cost import FanCost
from balkony.capital_cost.pressure import FanPressure
from utils import calculate_bare_module_pressure, calculate_purchased

TOLERANCE = 1e-6

@pytest.fixture
def centrifugal_radial_carbon_steel():
    return (FanCost(FanCost.Type.CentrifugalRadial, FanCost.Material.CarbonSteel),
            (3.5391, -0.3533, 0.4477),
            FanCost.Material.CarbonSteel.value[FanCost.Type.CentrifugalRadial.name])

@pytest.fixture
def backward_curve_fiberglass():
    return (FanCost(FanCost.Type.BackwardCurve, FanCost.Material.Fiberglass),
            (3.3471, -0.0734, 0.3090),
            FanCost.Material.Fiberglass.value[FanCost.Type.BackwardCurve.name])

@pytest.fixture
def axial_vane_nialloy():
    return (FanCost(FanCost.Type.AxialVane, FanCost.Material.NiAlloy),
            (3.1761, -0.1373, 0.3414),
            FanCost.Material.NiAlloy.value[FanCost.Type.AxialVane.name])

@pytest.fixture
def axial_tube_stainless_steel():
    return (FanCost(FanCost.Type.AxialTube, FanCost.Material.StainlessSteel),
            (3.0414, -0.3375, 0.4722),
            FanCost.Material.StainlessSteel.value[FanCost.Type.AxialTube.name])


@pytest.mark.parametrize("fixture, size, CEPCI, pressure", [
    ("centrifugal_radial_carbon_steel", 50.0, 397, 2),
    ("backward_curve_fiberglass", 70.0, 397, 2),
    ("axial_vane_nialloy", 60.0, 397, 2),
    ("axial_tube_stainless_steel", 90.0, 397, 2),
])
def test_within_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = FanPressure(equipment._type).factor(pressure).value
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
    ("centrifugal_radial_carbon_steel", 0.5, 397, 2),
    ("backward_curve_fiberglass", 0.8, 397, 2),
    ("axial_vane_nialloy", 0.6, 397, 2),
    ("axial_tube_stainless_steel", 0.7, 397, 2),
])
def test_below_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = FanPressure(equipment._type).factor(pressure).value
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
    ("centrifugal_radial_carbon_steel", 150.0, 397, 2),
    ("backward_curve_fiberglass", 200.0, 397, 2),
    ("axial_vane_nialloy", 250.0, 397, 2),
    ("axial_tube_stainless_steel", 300.0, 397, 2),
])
def test_above_limits(fixture, size, CEPCI, pressure, request):
    equipment, parameters, Fbm = request.getfixturevalue(fixture)
    K1, K2, K3 = parameters
    purchased_value = calculate_purchased(K1, K2, K3, size, CEPCI)
    pressure_fac = FanPressure(equipment._type).factor(pressure).value
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
