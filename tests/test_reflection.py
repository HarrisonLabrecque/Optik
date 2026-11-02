import math
import pytest

from optics.reflection import calculate_reflection


@pytest.mark.parametrize(
    "incident_angle, expected",
    [
        (0, 0),
        (15, 15),
        (30, 30),
        (45, 45),
        (60, 60),
        (90, 90),
    ],
)
def test_valid_reflection(incident_angle, expected):
    result = calculate_reflection(incident_angle)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "incident_angle",
    [-10, 100, math.inf, -math.inf, math.nan],
)
def test_invalid_reflection(incident_angle):
    with pytest.raises(ValueError):
        calculate_reflection(incident_angle)