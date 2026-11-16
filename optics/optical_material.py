
"""
Optik - Optical Material Model
Version: 0.5.0

Defines optical material properties and validates
dispersion model parameters.

Supported dispersion models:
    - Cauchy
    - Sellmeier

Scientific conventions:
    - Wavelength limits are stored in nanometers (nm).
    - Cauchy coefficients are ordered (A, B, C).
    - Sellmeier coefficients are ordered
      (B1, B2, B3, C1, C2, C3).
    - Sellmeier C coefficients have units of µm²
      when wavelength is expressed in micrometers.

This module contains no GUI dependencies.
"""

from dataclasses import dataclass
from math import isfinite
from typing import Literal


DispersionModel = Literal["cauchy", "sellmeier"]


class OpticalMaterialError(ValueError):
    """Raised when optical material data is invalid."""


@dataclass(frozen=True)
class OpticalMaterial:
    """
    Represents an optical material and its dispersion data.

    Attributes:
        name:
            Material name.

        formula:
            Supported dispersion model.

        coefficients:
            Model coefficients.

            Cauchy:
                (A, B, C)

            Sellmeier:
                (B1, B2, B3, C1, C2, C3)

        wavelength_min_nm:
            Minimum valid wavelength in nanometers.

        wavelength_max_nm:
            Maximum valid wavelength in nanometers.

        description:
            Optional material description.

        source:
            Reference for the material coefficients.
    """

    name: str
    formula: DispersionModel
    coefficients: tuple[float, ...]
    wavelength_min_nm: float
    wavelength_max_nm: float
    description: str = ""
    source: str = ""

    def __post_init__(self) -> None:
        """Validate and normalize material properties."""

        self._validate_name()
        self._validate_formula()
        self._validate_coefficients()
        self._validate_wavelength_range()
        self._validate_metadata()

    def _validate_name(self) -> None:
        """Validate the material name."""

        if not isinstance(self.name, str):
            raise OpticalMaterialError(
                "Material name must be a string."
            )

        name = self.name.strip()

        if not name:
            raise OpticalMaterialError(
                "Material name cannot be empty."
            )

        object.__setattr__(self, "name", name)

    def _validate_formula(self) -> None:
        """Validate the selected dispersion model."""

        if self.formula not in ("cauchy", "sellmeier"):
            raise OpticalMaterialError(
                f"Unsupported dispersion model: {self.formula!r}"
            )

    def _validate_coefficients(self) -> None:
        """Validate dispersion coefficients."""

        if not isinstance(
            self.coefficients, (tuple, list)
        ):
            raise OpticalMaterialError(
                "Coefficients must be a tuple or list."
            )

        expected_count = {
            "cauchy": 3,
            "sellmeier": 6,
        }[self.formula]

        if len(self.coefficients) != expected_count:
            raise OpticalMaterialError(
                f"{self.formula.capitalize()} requires "
                f"{expected_count} coefficients."
            )

        validated = []

        for index, coefficient in enumerate(
            self.coefficients
        ):
            if (
                isinstance(coefficient, bool)
                or not isinstance(
                    coefficient, (int, float)
                )
            ):
                raise OpticalMaterialError(
                    f"Coefficient {index + 1} "
                    "must be numeric."
                )

            value = float(coefficient)

            if not isfinite(value):
                raise OpticalMaterialError(
                    f"Coefficient {index + 1} "
                    "must be finite."
                )

            validated.append(value)

        object.__setattr__(
            self,
            "coefficients",
            tuple(validated),
        )

    def _validate_wavelength_range(self) -> None:
        """Validate the wavelength interval."""

        for attribute in (
            "wavelength_min_nm",
            "wavelength_max_nm",
        ):
            value = getattr(self, attribute)

            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
            ):
                raise OpticalMaterialError(
                    f"{attribute} must be numeric."
                )

            value = float(value)

            if not isfinite(value) or value <= 0:
                raise OpticalMaterialError(
                    f"{attribute} must be "
                    "positive and finite."
                )

            object.__setattr__(
                self,
                attribute,
                value,
            )

        if (
            self.wavelength_min_nm
            >= self.wavelength_max_nm
        ):
            raise OpticalMaterialError(
                "Minimum wavelength must be "
                "less than maximum wavelength."
            )

    def _validate_metadata(self) -> None:
        """Validate optional descriptive metadata."""

        for attribute in ("description", "source"):
            value = getattr(self, attribute)

            if not isinstance(value, str):
                raise OpticalMaterialError(
                    f"{attribute} must be a string."
                )

            object.__setattr__(
                self,
                attribute,
                value.strip(),
            )

    @property
    def wavelength_min_um(self) -> float:
        """Return minimum wavelength in micrometers."""

        return self.wavelength_min_nm / 1000.0

    @property
    def wavelength_max_um(self) -> float:
        """Return maximum wavelength in micrometers."""

        return self.wavelength_max_nm / 1000.0

    @property
    def coefficient_count(self) -> int:
        """Return the number of dispersion coefficients."""

        return len(self.coefficients)

    def supports_wavelength(
        self,
        wavelength_nm: float,
    ) -> bool:
        """
        Check whether a wavelength is within
        the material's documented valid range.

        Args:
            wavelength_nm:
                Wavelength in nanometers.

        Returns:
            True if the wavelength is valid.
        """

        if (
            isinstance(wavelength_nm, bool)
            or not isinstance(
                wavelength_nm, (int, float)
            )
        ):
            return False

        wavelength = float(wavelength_nm)

        if not isfinite(wavelength):
            return False

        return (
            self.wavelength_min_nm
            <= wavelength
            <= self.wavelength_max_nm
        )

    def to_dict(self) -> dict:
        """
        Convert the material into a dictionary.

        Useful for JSON serialization and
        repository storage.
        """

        return {
            "name": self.name,
            "formula": self.formula,
            "coefficients": list(self.coefficients),
            "wavelength_min_nm": (
                self.wavelength_min_nm
            ),
            "wavelength_max_nm": (
                self.wavelength_max_nm
            ),
            "description": self.description,
            "source": self.source,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OpticalMaterial":
        """Create an OpticalMaterial from a dictionary."""

        if not isinstance(data, dict):
            raise OpticalMaterialError(
                "Material data must be a dictionary."
            )

        try:
            return cls(
                name=data["name"],
                formula=data["formula"],
                coefficients=data["coefficients"],
                wavelength_min_nm=(
                    data["wavelength_min_nm"]
                ),
                wavelength_max_nm=(
                    data["wavelength_max_nm"]
                ),
                description=data.get(
                    "description", ""
                ),
                source=data.get("source", ""),
            )

        except KeyError as error:
            raise OpticalMaterialError(
                f"Missing required material field: "
                f"{error.args[0]}"
            ) from error
