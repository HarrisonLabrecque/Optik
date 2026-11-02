import pytest

from optics.refraction import calculate_refraction


@pytest.mark.parametrize(
    "n1, n2, incident_angle, expected",
    [
        (1.0, 1.5, 0, 0),
        (1.0, 1.5, 30, 19.4712),
        (1.5, 1.0, 30, 48.5904),
    ],
)
def test_refraction(n1, n2, incident_angle, expected):
    result = calculate_refraction(n1, n2, incident_angle)
    assert result == pytest.approx(expected, abs=0.01)


def test_invalid_refraction():
    with pytest.raises(ValueError):
        calculate_refraction(1.5, 1.0, 50)