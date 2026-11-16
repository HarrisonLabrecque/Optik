
"""
Optik - Optical Material Comparison
Version: 0.5.0

Compare optical materials using wavelength-dependent
refractive index calculations.

Supported models:
    - Sellmeier
    - Cauchy

Features:
    - Calculate refractive indices at a wavelength
    - Compare multiple optical materials
    - Calculate refractive index differences
    - Calculate dispersion over a wavelength interval
    - Generate comparison datasets

Units:
    Public wavelength inputs: nanometers (nm)
    Refractive index: dimensionless

No GUI dependencies.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from math import isfinite

from optics.optical_material import OpticalMaterial
from optics.sellmeier import (
    SellmeierError,
    calculate_material_index,
)


class MaterialComparisonError(ValueError):
    """Raised when a material comparison fails."""


@dataclass(frozen=True)
class MaterialIndexResult:
    """Refractive index for a single material."""

    material_name: str
    wavelength_nm: float
    refractive_index: float


@dataclass(frozen=True)
class MaterialDifferenceResult:
    """Refractive index difference between two materials."""

    material_1: str
    material_2: str
    wavelength_nm: float
    index_1: float
    index_2: float
    index_difference: float


@dataclass(frozen=True)
class MaterialDispersionResult:
    """Refractive index variation over a wavelength interval."""

    material_name: str
    wavelength_min_nm: float
    wavelength_max_nm: float
    index_at_min: float
    index_at_max: float
    index_difference: float


def _validate_wavelength(
    wavelength_nm: float,
) -> float:
    """Validate a positive, finite wavelength."""

    if (
        isinstance(wavelength_nm, bool)
        or not isinstance(wavelength_nm, (int, float))
    ):
        raise MaterialComparisonError(
            "Wavelength must be numeric."
        )

    value = float(wavelength_nm)

    if not isfinite(value) or value <= 0:
        raise MaterialComparisonError(
            "Wavelength must be positive and finite."
        )

    return value


def _validate_material(
    material: OpticalMaterial,
) -> None:
    """Validate an optical material instance."""

    if not isinstance(material, OpticalMaterial):
        raise MaterialComparisonError(
            "Expected an OpticalMaterial instance."
        )


def _calculate_cauchy_index(
    wavelength_nm: float,
    coefficients: tuple[float, ...],
) -> float:
    """
    Calculate the Cauchy refractive index.

    Equation:
        n = A + B / lambda² + C / lambda⁴

    lambda is expressed in micrometers.
    """

    a, b, c = coefficients

    wavelength_um = wavelength_nm / 1000.0

    index = (
        a
        + b / wavelength_um**2
        + c / wavelength_um**4
    )

    if not isfinite(index) or index <= 0:
        raise MaterialComparisonError(
            "Cauchy calculation produced an invalid "
            "refractive index."
        )

    return index


def calculate_refractive_index(
    material: OpticalMaterial,
    wavelength_nm: float,
) -> MaterialIndexResult:
    """
    Calculate refractive index for an optical material.

    Supports both Sellmeier and Cauchy models.
    Enforces the material's wavelength range.
    """

    _validate_material(material)

    wavelength = _validate_wavelength(wavelength_nm)

    if not material.supports_wavelength(wavelength):
        raise MaterialComparisonError(
            f"{wavelength} nm is outside the valid "
            f"range for {material.name}."
        )

    if material.formula == "sellmeier":
        try:
            index = calculate_material_index(
                material,
                wavelength,
            ).refractive_index
        except SellmeierError as error:
            raise MaterialComparisonError(
                str(error)
            ) from error

    elif material.formula == "cauchy":
        index = _calculate_cauchy_index(
            wavelength,
            material.coefficients,
        )

    else:
        raise MaterialComparisonError(
            f"Unsupported dispersion model: "
            f"{material.formula}"
        )

    return MaterialIndexResult(
        material_name=material.name,
        wavelength_nm=wavelength,
        refractive_index=index,
    )


def compare_materials(
    materials: Iterable[OpticalMaterial],
    wavelength_nm: float,
) -> list[MaterialIndexResult]:
    """
    Compare multiple materials at a single wavelength.

    Results are sorted by refractive index,
    from lowest to highest.
    """

    wavelength = _validate_wavelength(wavelength_nm)

    results = [
        calculate_refractive_index(
            material,
            wavelength,
        )
        for material in materials
    ]

    return sorted(
        results,
        key=lambda result: result.refractive_index,
    )


def calculate_index_difference(
    material_1: OpticalMaterial,
    material_2: OpticalMaterial,
    wavelength_nm: float,
) -> MaterialDifferenceResult:
    """
    Calculate the refractive index difference.

    Difference:
        n(material_1) - n(material_2)
    """

    first = calculate_refractive_index(
        material_1,
        wavelength_nm,
    )

    second = calculate_refractive_index(
        material_2,
        wavelength_nm,
    )

    return MaterialDifferenceResult(
        material_1=first.material_name,
        material_2=second.material_name,
        wavelength_nm=first.wavelength_nm,
        index_1=first.refractive_index,
        index_2=second.refractive_index,
        index_difference=(
            first.refractive_index
            - second.refractive_index
        ),
    )


def calculate_material_dispersion(
    material: OpticalMaterial,
    wavelength_min_nm: float,
    wavelength_max_nm: float,
) -> MaterialDispersionResult:
    """
    Calculate refractive index variation
    across a wavelength interval.

    Dispersion measure:
        n(lambda_min) - n(lambda_max)
    """

    start = _validate_wavelength(wavelength_min_nm)
    end = _validate_wavelength(wavelength_max_nm)

    if start >= end:
        raise MaterialComparisonError(
            "Minimum wavelength must be less "
            "than maximum wavelength."
        )

    first = calculate_refractive_index(
        material,
        start,
    )

    second = calculate_refractive_index(
        material,
        end,
    )

    return MaterialDispersionResult(
        material_name=material.name,
        wavelength_min_nm=start,
        wavelength_max_nm=end,
        index_at_min=first.refractive_index,
        index_at_max=second.refractive_index,
        index_difference=(
            first.refractive_index
            - second.refractive_index
        ),
    )


def generate_comparison_dataset(
    materials: Iterable[OpticalMaterial],
    wavelength_start_nm: float,
    wavelength_end_nm: float,
    points: int = 100,
) -> dict[str, list[MaterialIndexResult]]:
    """
    Generate refractive index datasets for plotting.

    Each material is evaluated over the same
    wavelength interval.

    Returns:
        Dictionary mapping material names to
        ordered MaterialIndexResult lists.
    """

    start = _validate_wavelength(wavelength_start_nm)
    end = _validate_wavelength(wavelength_end_nm)

    if start >= end:
        raise MaterialComparisonError(
            "Starting wavelength must be less "
            "than ending wavelength."
        )

    if (
        isinstance(points, bool)
        or not isinstance(points, int)
        or points < 2
    ):
        raise MaterialComparisonError(
            "Points must be an integer >= 2."
        )

    step = (end - start) / (points - 1)

    wavelengths = [
        start + index * step
        for index in range(points)
    ]

    wavelengths[-1] = end

    dataset = {}

    for material in materials:
        _validate_material(material)

        if material.name in dataset:
            raise MaterialComparisonError(
                f"Duplicate material name: {material.name}"
            )

        dataset[material.name] = [
            calculate_refractive_index(
                material,
                wavelength,
            )
            for wavelength in wavelengths
        ]

    return dataset
