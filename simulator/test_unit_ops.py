# test_simulator.py
import pytest
from models import stream
from unit_ops import heat_exchanger, pump

def test_pump_water_1_to_5_bar():
    feed = stream(
        name="feed",
        flow=100,         # kg/hr
        z={"water": 1.0},
        T=298.15,         # K
        P=1.0,            # bar
    )
    feed.calculate_properties()

    p = pump(name="p1", feed=feed, P_out=5.0, efficiency=0.8)
    p.calculate()

    assert p.power == pytest.approx(13.9, rel=0.02)   # within 2%
    assert p.outlet_stream.P == 5.0
    assert p.outlet_stream.flow == 100

def test_pump_roundtrip():
    """If we compute power from P_out, then P_out from that power, we should get back the same P_out."""
    feed = stream(name="f", flow=100, z={"water": 1.0}, T=298.15, P=1.0)
    feed.calculate_properties()

    # forward
    p1 = pump(name="p1", feed=feed, P_out=5.0, efficiency=0.8)
    p1.calculate()
    computed_power = p1.power

    # backward
    p2 = pump(name="p2", feed=feed, power=computed_power, efficiency=0.8)
    p2.calculate()

    assert p2.P_out == pytest.approx(5.0, rel=1e-6)

def test_pump_rejects_vapor():
    feed = stream(name="f", flow=100, z={"methane": 1.0}, T=300, P=1.0)
    feed.calculate_properties()

    p = pump(name="p", feed=feed, P_out=5.0)
    with pytest.raises(ValueError):
        p.calculate()

def test_heat_exchanger_benzene():
    feed = stream(name="f", flow=100, z={"benzene": 1.0}, T=300, P=1.5)
    feed.calculate_properties()

    hx = heat_exchanger(name="hx1", feed=feed, T_out=350, efficiency=0.9)
    hx.calculate()

    # 100/78.11 * 135.42 * 50 = 8667 kJ/hr
    assert hx.Q == pytest.approx(8667, rel=0.02)