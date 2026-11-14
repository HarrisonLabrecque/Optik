
"""
Optik — Prism Optics Unit Tests
Version: 0.4.0

Tests for optics/prisms.py.

Coverage:
    - Prism refraction calculations
    - PrismResult dataclass
    - Minimum deviation
    - Critical angle
    - Total internal reflection
    - Input validation
    - Special optical cases
"""

from dataclasses import FrozenInstanceError
import math

import pytest

from optics.prisms import (
    PrismResult,
    PrismError,
    TotalInternalReflectionError,
    calculate_prism_refraction,
    calculate_minimum_deviation,
    calculate_prism_critical_angle,
    is_total_internal_reflection,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def standard_prism():
    """A 60-degree glass prism with a 45-degree incident ray."""
    return calculate_prism_refraction(
        apex_angle=60.0,
        incident_angle=45.0,
        refractive_index=1.5,
    )


# ============================================================
# PRISM RESULT TESTS
# ============================================================

class TestPrismResult:

    def test_returns_prism_result(self, standard_prism):
        assert isinstance(standard_prism, PrismResult)

    def test_result_is_immutable(self, standard_prism):
        with pytest.raises(FrozenInstanceError):
            standard_prism.apex_angle = 45.0

    def test_input_values_are_preserved(self, standard_prism):
        assert standard_prism.apex_angle == 60.0
        assert standard_prism.incident_angle == 45.0
        assert standard_prism.refractive_index == 1.5


# ============================================================
# PRISM REFRACTION TESTS
# ============================================================

class TestPrismRefraction:

    def test_first_refracted_angle(self, standard_prism):
        assert standard_prism.first_refracted_angle == pytest.approx(
            28.1255,
            abs=1e-4,
        )

    def test_second_internal_angle(self, standard_prism):
        assert standard_prism.second_internal_angle == pytest.approx(
            31.8745,
            abs=1e-4,
        )

    def test_emergent_angle(self, standard_prism):
        expected = math.degrees(
            math.asin(
                1.5 * math.sin(
                    math.radians(
                        standard_prism.second_internal_angle
                    )
                )
            )
        )

        assert standard_prism.emergent_angle == pytest.approx(
            expected,
            abs=1e-10,
        )

    def test_deviation_angle(self, standard_prism):
        expected = (
            standard_prism.incident_angle
            + standard_prism.emergent_angle
            - standard_prism.apex_angle
        )

        assert standard_prism.deviation_angle == pytest.approx(
            expected,
            abs=1e-10,
        )

    @pytest.mark.parametrize(
        "apex, incident, index",
        [
            (30.0, 20.0, 1.5),
            (45.0, 30.0, 1.5),
            (60.0, 45.0, 1.5),
            (60.0, 60.0, 1.5),
            (40.0, 30.0, 1.33),
        ],
    )
    def test_valid_prism_configurations(
        self,
        apex,
        incident,
        index,
    ):
        result = calculate_prism_refraction(
            apex,
            incident,
            index,
        )

        assert isinstance(result, PrismResult)
        assert math.isfinite(result.deviation_angle)
        assert math.isfinite(result.emergent_angle)

    def test_snells_law_first_surface(self, standard_prism):
        left = math.sin(
            math.radians(standard_prism.incident_angle)
        )

        right = (
            standard_prism.refractive_index
            * math.sin(
                math.radians(
                    standard_prism.first_refracted_angle
                )
            )
        )

        assert left == pytest.approx(right, abs=1e-12)

    def test_snells_law_second_surface(self, standard_prism):
        left = (
            standard_prism.refractive_index
            * math.sin(
                math.radians(
                    standard_prism.second_internal_angle
                )
            )
        )

        right = math.sin(
            math.radians(standard_prism.emergent_angle)
        )

        assert left == pytest.approx(right, abs=1e-12)

    def test_internal_geometry(self, standard_prism):
        total = (
            standard_prism.first_refracted_angle
            + standard_prism.second_internal_angle
        )

        assert total == pytest.approx(
            standard_prism.apex_angle,
            abs=1e-12,
        )

    def test_symmetric_minimum_deviation(self):
        apex = 60.0
        index = 1.5

        incident = math.degrees(
            math.asin(index * math.sin(math.radians(apex / 2)))
        )

        result = calculate_prism_refraction(
            apex,
            incident,
            index,
        )

        assert result.first_refracted_angle == pytest.approx(30.0)
        assert result.second_internal_angle == pytest.approx(30.0)
        assert result.emergent_angle == pytest.approx(incident)

        assert result.deviation_angle == pytest.approx(
            calculate_minimum_deviation(apex, index)
        )


# ============================================================
# MINIMUM DEVIATION TESTS
# ============================================================

class TestMinimumDeviation:

    @pytest.mark.parametrize(
    "apex, index, expected",
    [
        (60.0, 1.5, 37.1807558),
        (30.0, 1.5, 15.6886411),
    ],
)
    def test_minimum_deviation(
        self,
        apex,
        index,
        expected,
    ):
        result = calculate_minimum_deviation(apex, index)

        assert result == pytest.approx(expected, abs=1e-4)

    def test_minimum_deviation_positive(self):
        result = calculate_minimum_deviation(45.0, 1.5)
        assert result > 0.0

    def test_minimum_deviation_invalid_geometry(self):
        with pytest.raises(PrismError):
            calculate_minimum_deviation(90.0, 1.5)

    def test_minimum_deviation_invalid_index(self):
        with pytest.raises(PrismError):
            calculate_minimum_deviation(60.0, 1.0)


# ============================================================
# CRITICAL ANGLE TESTS
# ============================================================

class TestCriticalAngle:

    @pytest.mark.parametrize(
        "index, expected",
        [
            (1.5, 41.8103149),
            (2.0, 30.0),
            (1.33, 48.7534666),
        ],
    )
    def test_critical_angle(self, index, expected):
        result = calculate_prism_critical_angle(index)

        assert result == pytest.approx(expected, abs=1e-4)

    def test_critical_angle_range(self):
        result = calculate_prism_critical_angle(1.5)

        assert 0.0 < result < 90.0

    def test_critical_angle_invalid_index(self):
        with pytest.raises(PrismError):
            calculate_prism_critical_angle(1.0)


# ============================================================
# TOTAL INTERNAL REFLECTION TESTS
# ============================================================

class TestTotalInternalReflection:

    def test_tir_above_critical_angle(self):
        assert is_total_internal_reflection(50.0, 1.5) is True

    def test_no_tir_below_critical_angle(self):
        assert is_total_internal_reflection(30.0, 1.5) is False

    def test_no_tir_at_critical_angle(self):
        critical = calculate_prism_critical_angle(1.5)

        assert is_total_internal_reflection(
            critical,
            1.5,
        ) is False

    def test_prism_refraction_raises_tir(self):
        with pytest.raises(TotalInternalReflectionError):
            calculate_prism_refraction(
                apex_angle=70.0,
                incident_angle=20.0,
                refractive_index=1.5,
            )

    def test_tir_exception_is_prism_error(self):
        assert issubclass(
            TotalInternalReflectionError,
            PrismError,
        )


# ============================================================
# INPUT VALIDATION TESTS
# ============================================================

class TestInputValidation:

    @pytest.mark.parametrize(
        "apex",
        [
            -10.0,
            0.0,
            180.0,
            200.0,
        ],
    )
    def test_invalid_apex_angles(self, apex):
        with pytest.raises(PrismError):
            calculate_prism_refraction(apex, 45.0, 1.5)

    @pytest.mark.parametrize(
        "incident",
        [
            -1.0,
            90.0,
            100.0,
        ],
    )
    def test_invalid_incident_angles(self, incident):
        with pytest.raises(PrismError):
            calculate_prism_refraction(60.0, incident, 1.5)

    @pytest.mark.parametrize(
        "index",
        [
            -1.5,
            0.0,
            1.0,
        ],
    )
    def test_invalid_refractive_indices(self, index):
        with pytest.raises(PrismError):
            calculate_prism_refraction(60.0, 45.0, index)

    @pytest.mark.parametrize(
        "invalid",
        [
            float("nan"),
            float("inf"),
            float("-inf"),
            None,
            "invalid",
            True,
        ],
    )
    def test_invalid_apex_types(self, invalid):
        with pytest.raises(PrismError):
            calculate_prism_refraction(invalid, 45.0, 1.5)

    @pytest.mark.parametrize(
        "invalid",
        [
            float("nan"),
            float("inf"),
            None,
            "invalid",
            True,
        ],
    )
    def test_invalid_incident_types(self, invalid):
        with pytest.raises(PrismError):
            calculate_prism_refraction(60.0, invalid, 1.5)

    @pytest.mark.parametrize(
        "invalid",
        [
            float("nan"),
            float("inf"),
            None,
            "invalid",
            True,
        ],
    )
    def test_invalid_index_types(self, invalid):
        with pytest.raises(PrismError):
            calculate_prism_refraction(60.0, 45.0, invalid)

    @pytest.mark.parametrize(
        "angle",
        [
            -1.0,
            90.0,
            100.0,
            float("nan"),
            float("inf"),
        ],
    )
    def test_invalid_internal_angles(self, angle):
        with pytest.raises(PrismError):
            is_total_internal_reflection(angle, 1.5)


# ============================================================
# SPECIAL CASES
# ============================================================

class TestSpecialCases:

    def test_zero_incident_angle(self):
        result = calculate_prism_refraction(
            apex_angle=30.0,
            incident_angle=0.0,
            refractive_index=1.5,
        )

        assert result.first_refracted_angle == pytest.approx(0.0)
        assert result.second_internal_angle == pytest.approx(30.0)

    def test_zero_second_internal_angle(self):
        apex = 30.0
        index = 1.5

        incident = math.degrees(
            math.asin(index * math.sin(math.radians(apex)))
        )

        result = calculate_prism_refraction(
            apex,
            incident,
            index,
        )

        assert result.second_internal_angle == pytest.approx(
            0.0,
            abs=1e-10,
        )
        assert result.emergent_angle == pytest.approx(
            0.0,
            abs=1e-10,
        )

    def test_invalid_second_surface_geometry(self):
        with pytest.raises(PrismError):
            calculate_prism_refraction(
                apex_angle=10.0,
                incident_angle=80.0,
                refractive_index=1.5,
            )


# ============================================================
# TEST MODULE EXECUTION
# ============================================================

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
