import math
import pytest

from optics.total_internal_reflection import (
    calculate_critical_angle,
    is_total_internal_reflection,
)


@pytest.mark.parametrize(
    "n1, n2, expected",
    [
        (1.5, 1.0, 41.8103),
        (1.33, 1.0, 48.7535),
        (2.0, 1.0, 30.0),
    ],
)
def test_critical_angle(n1, n2, expected):
    result = calculate_critical_angle(n1, n2)
    assert result == pytest.approx(expected, abs=0.01)


@pytest.mark.parametrize(
    "n1, n2",
    [
        (1.0, 1.5),
        (1.0, 1.0),
        (0, 1.0),
        (math.inf, 1.0),
    ],
)
def test_invalid_critical_angle(n1, n2):
    with pytest.raises(ValueError):
        calculate_critical_angle(n1, n2)


@pytest.mark.parametrize(
    "angle, expected",
    [
        (0, False),
        (30, False),
        (40, False),
        (45, True),
        (50, True),
        (90, True),
    ],
)
def test_total_internal_reflection(angle, expected):
    result = is_total_internal_reflection(1.5, 1.0, angle)
    assert result is expected


def test_no_total_internal_reflection():
    assert is_total_internal_reflection(1.0, 1.5, 60) is False


def test_exact_critical_angle():
    critical = calculate_critical_angle(1.5, 1.0)

    assert is_total_internal_reflection(
        1.5, 1.0, critical
    ) is False