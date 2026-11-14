
"""
Optik — Optical Dispersion Unit Tests
Version: 0.4.0

Tests for optics/dispersion.py.

Coverage:
    - CauchyCoefficients dataclass
    - DispersionResult and SpectralPrismResult
    - Wavelength conversion
    - Cauchy's dispersion equation
    - Single-wavelength dispersion
    - Refractive index differences
    - Spectral dispersion and sampling
    - Visible-spectrum calculations
    - Prism spectral deviation integration
    - Input validation and error handling
"""

from dataclasses import FrozenInstanceError
import math

import pytest

from optics.dispersion import (
    CauchyCoefficients,
    DispersionResult,
    SpectralPrismResult,
    DispersionError,
    nanometers_to_micrometers,
    calculate_cauchy_index,
    calculate_dispersion,
    calculate_index_difference,
    calculate_spectral_dispersion,
    calculate_spectral_prism_deviation,
    calculate_visible_dispersion,
)

from optics.prisms import calculate_prism_refraction


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def glass_coefficients():
    """Illustrative Cauchy coefficients for dispersive glass."""
    return CauchyCoefficients(
        A=1.5046,
        B=0.00420,
        C=0.00012,
    )


@pytest.fixture
def constant_coefficients():
    """Non-dispersive material with a constant index of 1.5."""
    return CauchyCoefficients(
        A=1.5,
        B=0.0,
        C=0.0,
    )


@pytest.fixture
def visible_spectrum(glass_coefficients):
    """Five samples across the visible wavelength range."""
    return calculate_visible_dispersion(
        glass_coefficients,
        samples=5,
    )


# ============================================================
# DATA STRUCTURE TESTS
# ============================================================

class TestDataStructures:

    def test_cauchy_coefficients_creation(self, glass_coefficients):
        assert glass_coefficients.A == pytest.approx(1.5046)
        assert glass_coefficients.B == pytest.approx(0.00420)
        assert glass_coefficients.C == pytest.approx(0.00012)

    def test_default_coefficients(self):
        coefficients = CauchyCoefficients(A=1.5)

        assert coefficients.B == 0.0
        assert coefficients.C == 0.0

    def test_coefficients_are_immutable(self, glass_coefficients):
        with pytest.raises(FrozenInstanceError):
            glass_coefficients.A = 1.6

    def test_dispersion_result_is_immutable(self):
        result = DispersionResult(
            wavelength_nm=550.0,
            refractive_index=1.52,
        )

        with pytest.raises(FrozenInstanceError):
            result.refractive_index = 1.6

    def test_spectral_prism_result_is_immutable(self):
        result = SpectralPrismResult(
            wavelength_nm=550.0,
            refractive_index=1.52,
            deviation_angle=40.0,
            emergent_angle=50.0,
        )

        with pytest.raises(FrozenInstanceError):
            result.deviation_angle = 45.0


# ============================================================
# WAVELENGTH CONVERSION TESTS
# ============================================================

class TestWavelengthConversion:

    @pytest.mark.parametrize(
        "wavelength_nm, expected_um",
        [
            (380.0, 0.380),
            (400.0, 0.400),
            (550.0, 0.550),
            (750.0, 0.750),
            (1000.0, 1.000),
        ],
    )
    def test_nanometers_to_micrometers(
        self,
        wavelength_nm,
        expected_um,
    ):
        result = nanometers_to_micrometers(wavelength_nm)

        assert result == pytest.approx(expected_um)

    @pytest.mark.parametrize(
        "wavelength",
        [
            0.0,
            -100.0,
            float("nan"),
            float("inf"),
            float("-inf"),
            None,
            "invalid",
            True,
        ],
    )
    def test_invalid_wavelength(self, wavelength):
        with pytest.raises(DispersionError):
            nanometers_to_micrometers(wavelength)


# ============================================================
# CAUCHY EQUATION TESTS
# ============================================================

class TestCauchyEquation:

    def test_cauchy_index_at_550_nm(self, glass_coefficients):
        wavelength_um = 0.550

        expected = (
            1.5046
            + 0.00420 / wavelength_um**2
            + 0.00012 / wavelength_um**4
        )

        result = calculate_cauchy_index(
            550.0,
            glass_coefficients,
        )

        assert result == pytest.approx(expected, abs=1e-12)

    def test_constant_refractive_index(self, constant_coefficients):
        for wavelength in (380.0, 450.0, 550.0, 750.0):
            result = calculate_cauchy_index(
                wavelength,
                constant_coefficients,
            )

            assert result == pytest.approx(1.5)

    def test_normal_dispersion(self, glass_coefficients):
        """Shorter wavelengths have a higher refractive index."""
        blue = calculate_cauchy_index(
            450.0,
            glass_coefficients,
        )

        red = calculate_cauchy_index(
            650.0,
            glass_coefficients,
        )

        assert blue > red

    def test_index_greater_than_one(self, glass_coefficients):
        result = calculate_cauchy_index(
            550.0,
            glass_coefficients,
        )

        assert result > 1.0

    def test_invalid_coefficients_type(self):
        with pytest.raises(DispersionError):
            calculate_cauchy_index(
                550.0,
                (1.5, 0.004, 0.0001),
            )

    @pytest.mark.parametrize(
        "coefficients",
        [
            CauchyCoefficients(float("nan"), 0.0, 0.0),
            CauchyCoefficients(1.5, float("inf"), 0.0),
            CauchyCoefficients(1.5, 0.0, float("-inf")),
            CauchyCoefficients(True, 0.0, 0.0),
        ],
    )
    def test_invalid_coefficients(self, coefficients):
        with pytest.raises(DispersionError):
            calculate_cauchy_index(550.0, coefficients)

    def test_index_not_greater_than_one(self):
        coefficients = CauchyCoefficients(A=0.9)

        with pytest.raises(DispersionError):
            calculate_cauchy_index(550.0, coefficients)

    def test_extremely_small_wavelength(self, glass_coefficients):
        with pytest.raises(DispersionError):
            calculate_cauchy_index(
                1e-200,
                glass_coefficients,
            )


# ============================================================
# SINGLE-WAVELENGTH DISPERSION TESTS
# ============================================================

class TestSingleWavelengthDispersion:

    def test_returns_dispersion_result(self, glass_coefficients):
        result = calculate_dispersion(
            550.0,
            glass_coefficients,
        )

        assert isinstance(result, DispersionResult)

    def test_wavelength_preserved(self, glass_coefficients):
        result = calculate_dispersion(
            550.0,
            glass_coefficients,
        )

        assert result.wavelength_nm == 550.0

    def test_refractive_index_matches_cauchy(self, glass_coefficients):
        result = calculate_dispersion(
            550.0,
            glass_coefficients,
        )

        expected = calculate_cauchy_index(
            550.0,
            glass_coefficients,
        )

        assert result.refractive_index == pytest.approx(expected)


# ============================================================
# REFRACTIVE INDEX DIFFERENCE TESTS
# ============================================================

class TestIndexDifference:

    def test_index_difference(self, glass_coefficients):
        result = calculate_index_difference(
            450.0,
            650.0,
            glass_coefficients,
        )

        assert result > 0.0

    def test_reverse_wavelength_order(self, glass_coefficients):
        forward = calculate_index_difference(
            450.0,
            650.0,
            glass_coefficients,
        )

        reverse = calculate_index_difference(
            650.0,
            450.0,
            glass_coefficients,
        )

        assert forward == pytest.approx(-reverse)

    def test_same_wavelength(self, glass_coefficients):
        result = calculate_index_difference(
            550.0,
            550.0,
            glass_coefficients,
        )

        assert result == pytest.approx(0.0)

    def test_constant_index_difference(self, constant_coefficients):
        result = calculate_index_difference(
            400.0,
            700.0,
            constant_coefficients,
        )

        assert result == pytest.approx(0.0)


# ============================================================
# SPECTRAL DISPERSION TESTS
# ============================================================

class TestSpectralDispersion:

    def test_sample_count(self, glass_coefficients):
        results = calculate_spectral_dispersion(
            400.0,
            700.0,
            glass_coefficients,
            samples=10,
        )

        assert len(results) == 10

    def test_includes_endpoints(self, glass_coefficients):
        results = calculate_spectral_dispersion(
            400.0,
            700.0,
            glass_coefficients,
            samples=5,
        )

        assert results[0].wavelength_nm == pytest.approx(400.0)
        assert results[-1].wavelength_nm == pytest.approx(700.0)

    def test_linear_spacing(self, glass_coefficients):
        results = calculate_spectral_dispersion(
            400.0,
            700.0,
            glass_coefficients,
            samples=4,
        )

        wavelengths = [
            result.wavelength_nm for result in results
        ]

        assert wavelengths == pytest.approx(
            [400.0, 500.0, 600.0, 700.0]
        )

    def test_returns_dispersion_results(self, glass_coefficients):
        results = calculate_spectral_dispersion(
            400.0,
            700.0,
            glass_coefficients,
            samples=5,
        )

        assert all(
            isinstance(result, DispersionResult)
            for result in results
        )

    def test_refractive_index_decreases(self, glass_coefficients):
        results = calculate_spectral_dispersion(
            400.0,
            700.0,
            glass_coefficients,
            samples=10,
        )

        indices = [
            result.refractive_index for result in results
        ]

        assert all(
            indices[i] > indices[i + 1]
            for i in range(len(indices) - 1)
        )

    @pytest.mark.parametrize(
        "samples",
        [
            0,
            1,
            -5,
            1.5,
            "10",
            None,
            True,
            10001,
        ],
    )
    def test_invalid_sample_count(
        self,
        glass_coefficients,
        samples,
    ):
        with pytest.raises(DispersionError):
            calculate_spectral_dispersion(
                400.0,
                700.0,
                glass_coefficients,
                samples=samples,
            )

    def test_equal_wavelength_range(self, glass_coefficients):
        with pytest.raises(DispersionError):
            calculate_spectral_dispersion(
                550.0,
                550.0,
                glass_coefficients,
            )

    def test_reversed_wavelength_range(self, glass_coefficients):
        with pytest.raises(DispersionError):
            calculate_spectral_dispersion(
                700.0,
                400.0,
                glass_coefficients,
            )

    def test_minimum_sample_count(self, glass_coefficients):
        results = calculate_spectral_dispersion(
            400.0,
            700.0,
            glass_coefficients,
            samples=2,
        )

        assert len(results) == 2

    def test_maximum_sample_count(self, constant_coefficients):
        results = calculate_spectral_dispersion(
            400.0,
            700.0,
            constant_coefficients,
            samples=10000,
        )

        assert len(results) == 10000


# ============================================================
# VISIBLE SPECTRUM TESTS
# ============================================================

class TestVisibleDispersion:

    def test_visible_spectrum_range(self, visible_spectrum):
        assert visible_spectrum[0].wavelength_nm == pytest.approx(
            380.0
        )

        assert visible_spectrum[-1].wavelength_nm == pytest.approx(
            750.0
        )

    def test_visible_spectrum_sample_count(self, visible_spectrum):
        assert len(visible_spectrum) == 5

    def test_default_visible_samples(self, glass_coefficients):
        results = calculate_visible_dispersion(
            glass_coefficients
        )

        assert len(results) == 50


# ============================================================
# PRISM INTEGRATION TESTS
# ============================================================

class TestSpectralPrismDeviation:

    def test_returns_spectral_prism_results(
        self,
        glass_coefficients,
    ):
        results = calculate_spectral_prism_deviation(
            apex_angle=60.0,
            incident_angle=50.0,
            coefficients=glass_coefficients,
            samples=5,
        )

        assert len(results) == 5

        assert all(
            isinstance(result, SpectralPrismResult)
            for result in results
        )

    def test_spectral_prism_wavelengths(
        self,
        glass_coefficients,
    ):
        results = calculate_spectral_prism_deviation(
            apex_angle=60.0,
            incident_angle=50.0,
            coefficients=glass_coefficients,
            samples=5,
        )

        assert results[0].wavelength_nm == pytest.approx(380.0)
        assert results[-1].wavelength_nm == pytest.approx(750.0)

    def test_spectral_prism_matches_prism_module(
        self,
        glass_coefficients,
    ):
        results = calculate_spectral_prism_deviation(
            apex_angle=60.0,
            incident_angle=50.0,
            coefficients=glass_coefficients,
            samples=5,
        )

        for result in results:
            expected = calculate_prism_refraction(
                apex_angle=60.0,
                incident_angle=50.0,
                refractive_index=result.refractive_index,
            )

            assert result.deviation_angle == pytest.approx(
                expected.deviation_angle
            )

            assert result.emergent_angle == pytest.approx(
                expected.emergent_angle
            )

    def test_shorter_wavelength_has_greater_deviation(
        self,
        glass_coefficients,
    ):
        results = calculate_spectral_prism_deviation(
            apex_angle=60.0,
            incident_angle=50.0,
            coefficients=glass_coefficients,
            samples=10,
        )

        assert (
            results[0].deviation_angle
            > results[-1].deviation_angle
        )

    def test_constant_index_constant_deviation(
        self,
        constant_coefficients,
    ):
        results = calculate_spectral_prism_deviation(
            apex_angle=60.0,
            incident_angle=50.0,
            coefficients=constant_coefficients,
            samples=5,
        )

        deviations = [
            result.deviation_angle for result in results
        ]

        assert deviations == pytest.approx(
            [deviations[0]] * len(deviations)
        )

    def test_invalid_prism_geometry(
        self,
        glass_coefficients,
    ):
        with pytest.raises(DispersionError):
            calculate_spectral_prism_deviation(
                apex_angle=90.0,
                incident_angle=20.0,
                coefficients=glass_coefficients,
                samples=5,
            )

    def test_invalid_prism_incident_angle(
        self,
        glass_coefficients,
    ):
        with pytest.raises(DispersionError):
            calculate_spectral_prism_deviation(
                apex_angle=60.0,
                incident_angle=-10.0,
                coefficients=glass_coefficients,
                samples=5,
            )


# ============================================================
# TEST MODULE EXECUTION
# ============================================================

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
