
"""
Optik — Optical Dispersion
Version: 0.4.0

Wavelength-dependent refractive index calculations using
Cauchy's dispersion equation.

Features:
    - Cauchy's dispersion equation
    - Wavelength-dependent refractive index
    - Spectral refractive index calculations
    - Refractive index differences
    - Prism deviation across wavelengths
    - Input validation

Assumptions:
    - Wavelengths are specified in nanometers (nm)
    - Cauchy coefficients use micrometer-based units
    - Prism calculations assume surrounding air (n = 1.0)
    - The Cauchy model is used within its valid fitted range

Cauchy's equation:

    n(lambda) = A + B / lambda^2 + C / lambda^4

where lambda is measured in micrometers (um).
"""

from dataclasses import dataclass
import math

from optics.prisms import (
    calculate_prism_refraction,
    PrismError,
    TotalInternalReflectionError,
)


# ============================================================
# CONSTANTS
# ============================================================

NM_PER_UM = 1000.0

VISIBLE_MIN_NM = 380.0
VISIBLE_MAX_NM = 750.0

DEFAULT_SPECTRAL_SAMPLES = 50

MAX_SPECTRAL_SAMPLES = 10000


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass(frozen=True)
class CauchyCoefficients:
    """
    Cauchy dispersion coefficients.

    A : dimensionless
    B : um^2
    C : um^4
    """

    A: float
    B: float = 0.0
    C: float = 0.0


@dataclass(frozen=True)
class DispersionResult:
    """Refractive index at a specific wavelength."""

    wavelength_nm: float
    refractive_index: float


@dataclass(frozen=True)
class SpectralPrismResult:
    """Prism deviation at a specific wavelength."""

    wavelength_nm: float
    refractive_index: float
    deviation_angle: float
    emergent_angle: float


# ============================================================
# EXCEPTIONS
# ============================================================

class DispersionError(ValueError):
    """Raised when dispersion inputs or results are invalid."""


# ============================================================
# INPUT VALIDATION
# ============================================================

def _validate_finite(value: float, name: str) -> float:
    """Validate a finite numerical value."""

    if isinstance(value, bool):
        raise DispersionError(
            f"{name} must be a finite number."
        )

    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise DispersionError(
            f"{name} must be a finite number."
        ) from exc

    if not math.isfinite(number):
        raise DispersionError(
            f"{name} must be a finite number."
        )

    return number


def _validate_wavelength(wavelength_nm: float) -> float:
    """Validate a positive wavelength in nanometers."""

    wavelength = _validate_finite(
        wavelength_nm,
        "Wavelength",
    )

    if wavelength <= 0.0:
        raise DispersionError(
            "Wavelength must be greater than zero."
        )

    return wavelength


def _validate_coefficients(
    coefficients: CauchyCoefficients,
) -> CauchyCoefficients:
    """Validate the Cauchy coefficients."""

    if not isinstance(coefficients, CauchyCoefficients):
        raise DispersionError(
            "Coefficients must be a CauchyCoefficients instance."
        )

    A = _validate_finite(coefficients.A, "Coefficient A")
    B = _validate_finite(coefficients.B, "Coefficient B")
    C = _validate_finite(coefficients.C, "Coefficient C")

    return CauchyCoefficients(A=A, B=B, C=C)


def _validate_sample_count(samples: int) -> int:
    """Validate the requested spectral sample count."""

    if isinstance(samples, bool) or not isinstance(samples, int):
        raise DispersionError(
            "Sample count must be an integer."
        )

    if not 2 <= samples <= MAX_SPECTRAL_SAMPLES:
        raise DispersionError(
            f"Sample count must be between 2 and "
            f"{MAX_SPECTRAL_SAMPLES}."
        )

    return samples


# ============================================================
# WAVELENGTH CONVERSION
# ============================================================

def nanometers_to_micrometers(
    wavelength_nm: float,
) -> float:
    """
    Convert wavelength from nanometers to micrometers.

    Parameters
    ----------
    wavelength_nm : float
        Wavelength in nanometers.

    Returns
    -------
    float
        Wavelength in micrometers.
    """

    wavelength_nm = _validate_wavelength(wavelength_nm)

    return wavelength_nm / NM_PER_UM


# ============================================================
# CAUCHY DISPERSION
# ============================================================

def calculate_cauchy_index(
    wavelength_nm: float,
    coefficients: CauchyCoefficients,
) -> float:
    """
    Calculate refractive index using Cauchy's equation.

    Parameters
    ----------
    wavelength_nm : float
        Wavelength in nanometers.

    coefficients : CauchyCoefficients
        Cauchy dispersion coefficients.

    Returns
    -------
    float
        Calculated refractive index.

    Raises
    ------
    DispersionError
        If inputs or calculated index are invalid.

    Notes
    -----
    Wavelength is converted to micrometers before
    applying Cauchy's equation:

        n = A + B / lambda^2 + C / lambda^4
    """

    wavelength_um = nanometers_to_micrometers(
        wavelength_nm
    )

    coefficients = _validate_coefficients(coefficients)

    try:
        wavelength_squared = wavelength_um ** 2
        wavelength_fourth = wavelength_squared ** 2

        refractive_index = (
            coefficients.A
            + coefficients.B / wavelength_squared
            + coefficients.C / wavelength_fourth
        )

    except (OverflowError, ZeroDivisionError) as exc:
        raise DispersionError(
            "Unable to calculate refractive index "
            "for the supplied wavelength."
        ) from exc

    if not math.isfinite(refractive_index):
        raise DispersionError(
            "Calculated refractive index is not finite."
        )

    if refractive_index <= 1.0:
        raise DispersionError(
            "Calculated refractive index must be greater "
            "than 1.0 for the current prism model."
        )

    return refractive_index


# ============================================================
# SINGLE-WAVELENGTH DISPERSION
# ============================================================

def calculate_dispersion(
    wavelength_nm: float,
    coefficients: CauchyCoefficients,
) -> DispersionResult:
    """
    Calculate dispersion properties at one wavelength.

    Returns
    -------
    DispersionResult
        Wavelength and corresponding refractive index.
    """

    wavelength_nm = _validate_wavelength(wavelength_nm)

    refractive_index = calculate_cauchy_index(
        wavelength_nm,
        coefficients,
    )

    return DispersionResult(
        wavelength_nm=wavelength_nm,
        refractive_index=refractive_index,
    )


# ============================================================
# REFRACTIVE INDEX DIFFERENCE
# ============================================================

def calculate_index_difference(
    wavelength_1_nm: float,
    wavelength_2_nm: float,
    coefficients: CauchyCoefficients,
) -> float:
    """
    Calculate the refractive index difference.

    Returns
    -------
    float
        n(wavelength_1) - n(wavelength_2)
    """

    index_1 = calculate_cauchy_index(
        wavelength_1_nm,
        coefficients,
    )

    index_2 = calculate_cauchy_index(
        wavelength_2_nm,
        coefficients,
    )

    return index_1 - index_2


# ============================================================
# SPECTRAL DISPERSION
# ============================================================

def calculate_spectral_dispersion(
    start_wavelength_nm: float,
    end_wavelength_nm: float,
    coefficients: CauchyCoefficients,
    samples: int = DEFAULT_SPECTRAL_SAMPLES,
) -> list[DispersionResult]:
    """
    Calculate refractive indices over a wavelength range.

    Wavelengths are linearly spaced and include both
    endpoints.

    Returns
    -------
    list[DispersionResult]
        Spectral refractive index results.
    """

    start = _validate_wavelength(start_wavelength_nm)
    end = _validate_wavelength(end_wavelength_nm)

    samples = _validate_sample_count(samples)

    if start >= end:
        raise DispersionError(
            "Start wavelength must be less than "
            "end wavelength."
        )

    step = (end - start) / (samples - 1)

    results = []

    for index in range(samples):
        wavelength = (
            end if index == samples - 1
            else start + index * step
        )

        results.append(
            calculate_dispersion(
                wavelength,
                coefficients,
            )
        )

    return results


# ============================================================
# PRISM SPECTRAL DEVIATION
# ============================================================

def calculate_spectral_prism_deviation(
    apex_angle: float,
    incident_angle: float,
    coefficients: CauchyCoefficients,
    start_wavelength_nm: float = VISIBLE_MIN_NM,
    end_wavelength_nm: float = VISIBLE_MAX_NM,
    samples: int = DEFAULT_SPECTRAL_SAMPLES,
) -> list[SpectralPrismResult]:
    """
    Calculate prism deviation across a wavelength range.

    Uses the prism refraction module to calculate
    deviation for each wavelength.

    Raises
    ------
    DispersionError
        If any wavelength produces invalid prism geometry
        or total internal reflection.

    Returns
    -------
    list[SpectralPrismResult]
        Wavelength-dependent prism deviations.
    """

    spectral_results = calculate_spectral_dispersion(
        start_wavelength_nm,
        end_wavelength_nm,
        coefficients,
        samples,
    )

    results = []

    for spectral_result in spectral_results:
        wavelength = spectral_result.wavelength_nm
        refractive_index = spectral_result.refractive_index

        try:
            prism_result = calculate_prism_refraction(
                apex_angle=apex_angle,
                incident_angle=incident_angle,
                refractive_index=refractive_index,
            )

        except (
            PrismError,
            TotalInternalReflectionError,
        ) as exc:
            raise DispersionError(
                "Prism refraction failed at wavelength "
                f"{wavelength:.2f} nm: {exc}"
            ) from exc

        results.append(
            SpectralPrismResult(
                wavelength_nm=wavelength,
                refractive_index=refractive_index,
                deviation_angle=prism_result.deviation_angle,
                emergent_angle=prism_result.emergent_angle,
            )
        )

    return results


# ============================================================
# VISIBLE SPECTRUM
# ============================================================

def calculate_visible_dispersion(
    coefficients: CauchyCoefficients,
    samples: int = DEFAULT_SPECTRAL_SAMPLES,
) -> list[DispersionResult]:
    """
    Calculate refractive indices across the visible spectrum.

    Default range:
        380 nm to 750 nm
    """

    return calculate_spectral_dispersion(
        start_wavelength_nm=VISIBLE_MIN_NM,
        end_wavelength_nm=VISIBLE_MAX_NM,
        coefficients=coefficients,
        samples=samples,
    )


# ============================================================
# MODULE EXPORTS
# ============================================================

__all__ = [
    "CauchyCoefficients",
    "DispersionResult",
    "SpectralPrismResult",
    "DispersionError",
    "nanometers_to_micrometers",
    "calculate_cauchy_index",
    "calculate_dispersion",
    "calculate_index_difference",
    "calculate_spectral_dispersion",
    "calculate_spectral_prism_deviation",
    "calculate_visible_dispersion",
]
