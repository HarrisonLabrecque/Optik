import math
import pytest

from optics.snells_law import calculate_snells_law


@pytest.mark.parametrize(
    "n1, n2, incident_angle, expected",
    [
        (1.0, 1.5, 0, 0),
        (1.0, 1.5, 30, 19.4712),
        (1.0, 1.33, 45, 32.117),
        (1.5, 1.0, 30, 48.5904),
    ],
)
def test_valid_snells_law(n1, n2, incident_angle, expected):
    result = calculate_snells_law(n1, n2, incident_angle)
    assert result == pytest.approx(expected, abs=0.01)


@pytest.mark.parametrize(
    "n1, n2, angle",
    [
        (0, 1.5, 30),
        (1.0, -1.5, 30),
        (math.inf, 1.5, 30),
        (1.0, math.nan, 30),
        (1.0, 1.5, -10),
        (1.0, 1.5, 100),
    ],
)
def test_invalid_snells_law(n1, n2, angle):
    with pytest.raises(ValueError):
        calculate_snells_law(n1, n2, angle)


def test_total_internal_reflection():
    with pytest.raises(ValueError):
        calculate_snells_law(1.5, 1.0, 50)