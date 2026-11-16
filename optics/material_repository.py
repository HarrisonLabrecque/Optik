
"""
Optik - Optical Material Repository
Version: 0.5.0

Provides in-memory storage and management of
optical material definitions.

Features:
    - Register optical materials
    - Retrieve materials by name
    - Filter by dispersion model
    - Filter by supported wavelength
    - Update material definitions
    - Remove materials
    - Export material data as dictionaries

Dependencies:
    optics.optical_material

This module contains no GUI dependencies.
"""

from collections.abc import Iterable

from optics.optical_material import (
    OpticalMaterial,
    OpticalMaterialError,
)


class MaterialRepositoryError(ValueError):
    """Raised when a material repository operation fails."""


class MaterialRepository:
    """
    In-memory repository for optical materials.

    Material names are treated as case-insensitive
    identifiers.

    Example:
        repository = MaterialRepository()
        repository.add_material(material)

        result = repository.get_material_by_name(
            "N-BK7"
        )
    """

    def __init__(
        self,
        materials: Iterable[OpticalMaterial] | None = None,
    ) -> None:
        """Initialize the repository."""

        self._materials: dict[str, OpticalMaterial] = {}

        if materials is not None:
            for material in materials:
                self.add_material(material)

    @staticmethod
    def _normalize_name(name: str) -> str:
        """
        Normalize a material name for lookup.

        Names are case-insensitive and surrounding
        whitespace is ignored.
        """

        if not isinstance(name, str):
            raise MaterialRepositoryError(
                "Material name must be a string."
            )

        normalized = name.strip().casefold()

        if not normalized:
            raise MaterialRepositoryError(
                "Material name cannot be empty."
            )

        return normalized

    @staticmethod
    def _validate_material(
        material: OpticalMaterial,
    ) -> None:
        """Validate the material object type."""

        if not isinstance(material, OpticalMaterial):
            raise MaterialRepositoryError(
                "Expected an OpticalMaterial instance."
            )

    def add_material(
        self,
        material: OpticalMaterial,
    ) -> None:
        """
        Add a material to the repository.

        Raises:
            MaterialRepositoryError:
                If the material already exists.
        """

        self._validate_material(material)

        key = self._normalize_name(material.name)

        if key in self._materials:
            raise MaterialRepositoryError(
                f"Material '{material.name}' already exists."
            )

        self._materials[key] = material

    def get_material_by_name(
        self,
        name: str,
    ) -> OpticalMaterial | None:
        """
        Retrieve a material by name.

        Returns None if the material is not found.
        """

        key = self._normalize_name(name)

        return self._materials.get(key)

    def get_all_materials(
        self,
    ) -> list[OpticalMaterial]:
        """
        Return all materials sorted alphabetically.
        """

        return sorted(
            self._materials.values(),
            key=lambda material: material.name.casefold(),
        )

    def get_materials_by_model(
        self,
        model: str,
    ) -> list[OpticalMaterial]:
        """
        Retrieve materials using a dispersion model.

        Supported models:
            - cauchy
            - sellmeier
        """

        if not isinstance(model, str):
            raise MaterialRepositoryError(
                "Dispersion model must be a string."
            )

        normalized_model = model.strip().casefold()

        if normalized_model not in (
            "cauchy",
            "sellmeier",
        ):
            raise MaterialRepositoryError(
                f"Unsupported dispersion model: {model!r}"
            )

        return [
            material
            for material in self.get_all_materials()
            if material.formula == normalized_model
        ]

    def get_materials_by_wavelength(
        self,
        wavelength_nm: float,
    ) -> list[OpticalMaterial]:
        """
        Retrieve materials supporting a wavelength.

        Args:
            wavelength_nm:
                Wavelength in nanometers.

        Returns:
            Materials whose documented wavelength
            ranges contain the requested value.
        """

        return [
            material
            for material in self.get_all_materials()
            if material.supports_wavelength(wavelength_nm)
        ]

    def contains(
        self,
        name: str,
    ) -> bool:
        """Check whether a material exists."""

        key = self._normalize_name(name)

        return key in self._materials

    def update_material(
        self,
        material: OpticalMaterial,
    ) -> None:
        """
        Replace an existing material definition.

        The material must already exist under
        the same name.
        """

        self._validate_material(material)

        key = self._normalize_name(material.name)

        if key not in self._materials:
            raise MaterialRepositoryError(
                f"Material '{material.name}' does not exist."
            )

        self._materials[key] = material

    def remove_material(
        self,
        name: str,
    ) -> OpticalMaterial:
        """
        Remove a material by name.

        Returns:
            The removed OpticalMaterial instance.
        """

        key = self._normalize_name(name)

        if key not in self._materials:
            raise MaterialRepositoryError(
                f"Material '{name}' does not exist."
            )

        return self._materials.pop(key)

    def clear(self) -> None:
        """Remove all materials from the repository."""

        self._materials.clear()

    def count(self) -> int:
        """Return the number of stored materials."""

        return len(self._materials)

    def to_dict_list(self) -> list[dict]:
        """
        Export all materials as dictionaries.

        Useful for future JSON serialization.
        """

        return [
            material.to_dict()
            for material in self.get_all_materials()
        ]

    @classmethod
    def from_dict_list(
        cls,
        data: list[dict],
    ) -> "MaterialRepository":
        """
        Create a repository from material dictionaries.

        Raises:
            MaterialRepositoryError:
                If the input is invalid.
            OpticalMaterialError:
                If a material definition is invalid.
        """

        if not isinstance(data, list):
            raise MaterialRepositoryError(
                "Material data must be a list."
            )

        materials = [
            OpticalMaterial.from_dict(item)
            for item in data
        ]

        return cls(materials)
