
"""
Optik - Sellmeier Dispersion Calculations
Version: 0.5.0

Implements the three-term Sellmeier dispersion equation
for wavelength-dependent refractive index calculations.

Equation:
    n² = 1 + Σ[B_i * λ² / (λ² - C_i)]

Units:
    Input wavelength: nanometers (nm)
    Internal wavelength: micrometers (µm)
    B coefficients: dimensionless
    C coefficients: µm²

Coefficient order:
    (B1, B2, B3, C1, C2, C3)

This module contains no GUI dependencies.
"""

from dataclasses import dataclass
from math import isfinite, sqrt
from collections.abc import Iterable

from optics.optical_material import OpticalMaterial


class SellmeierError(ValueError):
    """Raised when a Sellmeier calculation is invalid."""


@dataclass(frozen=True)
class SellmeierResult:
    """Result of a Sellmeier refractive index calculation."""

    wavelength_nm: float
    refractive_index: float


def _validate_wavelength(wavelength_nm: float) -> float:
    """Validate a positive, finite wavelength."""

    if (
        isinstance(wavelength_nm, bool)
        or not isinstance(wavelength_nm, (int, float))
    ):
        raise SellmeierError(
            "Wavelength must be a numeric value."
        )

    wavelength = float(wavelength_nm)

    if not isfinite(wavelength) or wavelength <= 0:
        raise SellmeierError(
            "Wavelength must be positive and finite."
        )

    return wavelength


def _validate_material(
    material: OpticalMaterial,
) -> None:
    """Ensure the material uses the Sellmeier model."""

    if not isinstance(material, OpticalMaterial):
        raise SellmeierError(
            "Expected an OpticalMaterial instance."
        )

    if material.formula != "sellmeier":
        raise SellmeierError(
            "Material must use the Sellmeier model."
        )


def calculate_sellmeier_index(
    wavelength_nm: float,
    coefficients: tuple[float, ...],
) -> float:
    """
    Calculate refractive index using the Sellmeier equation.

    Args:
        wavelength_nm:
            Vacuum wavelength in nanometers.

        coefficients:
            Six coefficients ordered as:
            (B1, B2, B3, C1, C2, C3)

    Returns:
        Refractive index as a float.

    Raises:
        SellmeierError:
            If the inputs or calculated result are invalid.

    Note:
        This function does not enforce a material-specific
        wavelength validity range. Use
        calculate_material_index() for that.
    """

    wavelength = _validate_wavelength(wavelength_nm)

    if not isinstance(coefficients, (tuple, list)):
        raise SellmeierError(
            "Coefficients must be a tuple or list."
        )

    if len(coefficients) != 6:
        raise SellmeierError(
            "Sellmeier requires exactly six coefficients."
        )

    validated = []

    for index, coefficient in enumerate(coefficients):
        if (
            isinstance(coefficient, bool)
            or not isinstance(coefficient, (int, float))
        ):
            raise SellmeierError(
                f"Coefficient {index + 1} must be numeric."
            )

        value = float(coefficient)

        if not isfinite(value):
            raise SellmeierError(
                f"Coefficient {index + 1} must be finite."
            )

        validated.append(value)

    b1, b2, b3, c1, c2, c3 = validated

    wavelength_um = wavelength / 1000.0
    wavelength_squared = wavelength_um ** 2

    refractive_index_squared = 1.0

    for b, c in (
        (b1, c1),
        (b2, c2),
        (b3, c3),
    ):
        denominator = wavelength_squared - c

        if denominator == 0.0:
            raise SellmeierError(
                "Wavelength coincides with a "
                "Sellmeier resonance."
            )

        term = b * wavelength_squared / denominator

        refractive_index_squared += term

    if (
        not isfinite(refractive_index_squared)
        or refractive_index_squared <= 0
    ):
        raise SellmeierError(
            "Sellmeier equation produced an invalid "
            "squared refractive index."
        )

    refractive_index = sqrt(refractive_index_squared)

    if not isfinite(refractive_index):
        raise SellmeierError(
            "Calculated refractive index is not finite."
        )

    return refractive_index


def calculate_material_index(
    material: OpticalMaterial,
    wavelength_nm: float,
) -> SellmeierResult:
    """
    Calculate refractive index for an optical material.

    Enforces the material's documented wavelength range.
    """

    _validate_material(material)

    wavelength = _validate_wavelength(wavelength_nm)

    if not material.supports_wavelength(wavelength):
        raise SellmeierError(
            f"Wavelength {wavelength} nm is outside "
            f"the valid range for {material.name}: "
            f"{material.wavelength_min_nm} - "
            f"{material.wavelength_max_nm} nm."
        )

    refractive_index = calculate_sellmeier_index(
        wavelength,
        material.coefficients,
    )

    return SellmeierResult(
        wavelength_nm=wavelength,
        refractive_index=refractive_index,
    )


def calculate_sellmeier_spectrum(
    material: OpticalMaterial,
    wavelengths_nm: Iterable[float],
) -> list[SellmeierResult]:
    """
    Calculate refractive indices at multiple wavelengths.

    All wavelengths must fall within the material's
    documented valid range.

    Returns:
        List of SellmeierResult objects.
    """

    _validate_material(material)

    results = []

    for wavelength in wavelengths_nm:
        result = calculate_material_index(
            material,
            wavelength,
        )

        results.append(result)

    return results


def calculate_sellmeier_curve(
    material: OpticalMaterial,
    wavelength_start_nm: float,
    wavelength_end_nm: float,
    points: int = 100,
) -> list[SellmeierResult]:
    """
    Generate a refractive index curve over a wavelength range.

    Args:
        material:
            Sellmeier optical material.

        wavelength_start_nm:
            Starting wavelength in nanometers.

        wavelength_end_nm:
            Ending wavelength in nanometers.

        points:
            Number of wavelength samples (minimum 2).
    """

    _validate_material(material)

    start = _validate_wavelength(wavelength_start_nm)
    end = _validate_wavelength(wavelength_end_nm)

    if start >= end:
        raise SellmeierError(
            "Starting wavelength must be less than "
            "ending wavelength."
        )

    if (
        isinstance(points, bool)
        or not isinstance(points, int)
        or points < 2
    ):
        raise SellmeierError(
            "Points must be an integer greater than 1."
        )

    step = (end - start) / (points - 1)

    wavelengths = [
        start + index * step
        for index in range(points)
    ]

    wavelengths[-1] = end

    return calculate_sellmeier_spectrum(
        material,
        wavelengths,
    )
