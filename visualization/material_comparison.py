
"""
Optik - Optical Material Comparison Visualization
Version: 0.5.0

Matplotlib visualizations for optical material
comparison and dispersion analysis.

Supported plots:
    - Refractive index vs wavelength
    - Refractive index difference vs wavelength
    - Dispersion comparison
    - Refractive index at a selected wavelength

Scientific conventions:
    Wavelength: nanometers (nm)
    Refractive index: dimensionless

No PySide6 dependencies.
"""

from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from optics.optical_material import OpticalMaterial
from optics.material_comparison import (
    calculate_material_dispersion,
    compare_materials,
    generate_comparison_dataset,
)


class MaterialVisualizationError(ValueError):
    """Raised when a material visualization fails."""


class MaterialComparisonVisualizer:
    """
    Generate Matplotlib figures for optical
    material comparison.

    Figures can be embedded into PySide6
    through FigureCanvasQTAgg.
    """

    def __init__(self, theme: str = "light") -> None:
        self.set_theme(theme)

    def set_theme(self, theme: str) -> None:
        """Set the visualization theme."""

        if theme not in ("light", "dark"):
            raise MaterialVisualizationError(
                "Theme must be 'light' or 'dark'."
            )

        self.theme = theme

    def _create_figure(
        self,
        title: str,
        xlabel: str,
        ylabel: str,
    ) -> tuple[Figure, Axes]:
        """Create a themed Matplotlib figure."""

        figure = Figure(figsize=(9, 5.5), dpi=100)
        axes = figure.add_subplot(111)

        if self.theme == "dark":
            background = "#20242b"
            foreground = "#f1f3f5"
            grid_color = "#5b626b"
        else:
            background = "#ffffff"
            foreground = "#202124"
            grid_color = "#c9cdd2"

        figure.patch.set_facecolor(background)
        axes.set_facecolor(background)

        axes.set_title(title, color=foreground, pad=15)
        axes.set_xlabel(xlabel, color=foreground)
        axes.set_ylabel(ylabel, color=foreground)

        axes.tick_params(
            axis="both",
            colors=foreground,
        )

        for spine in axes.spines.values():
            spine.set_color(foreground)

        axes.grid(
            True,
            linestyle="--",
            linewidth=0.6,
            alpha=0.45,
            color=grid_color,
        )

        figure.tight_layout()

        return figure, axes

    @staticmethod
    def _validate_materials(
        materials: Iterable[OpticalMaterial],
        minimum: int = 1,
    ) -> list[OpticalMaterial]:
        """Validate and materialize a material collection."""

        try:
            material_list = list(materials)
        except TypeError as error:
            raise MaterialVisualizationError(
                "Materials must be iterable."
            ) from error

        if len(material_list) < minimum:
            raise MaterialVisualizationError(
                f"At least {minimum} material(s) required."
            )

        for material in material_list:
            if not isinstance(material, OpticalMaterial):
                raise MaterialVisualizationError(
                    "All items must be OpticalMaterial instances."
                )

        return material_list

    @staticmethod
    def _finalize(
        figure: Figure,
        axes: Axes,
        legend: bool = True,
    ) -> Figure:
        """Apply final figure formatting."""

        if legend:
            handles, labels = axes.get_legend_handles_labels()

            if handles:
                legend_object = axes.legend(
                    loc="best",
                    framealpha=0.85,
                )

                foreground = axes.xaxis.label.get_color()

                for text in legend_object.get_texts():
                    text.set_color(foreground)

        figure.tight_layout()

        return figure

    def plot_refractive_index(
        self,
        materials: Iterable[OpticalMaterial],
        wavelength_start_nm: float = 400.0,
        wavelength_end_nm: float = 700.0,
        points: int = 200,
    ) -> Figure:
        """
        Plot refractive index versus wavelength
        for multiple optical materials.
        """

        material_list = self._validate_materials(materials)

        dataset = generate_comparison_dataset(
            materials=material_list,
            wavelength_start_nm=wavelength_start_nm,
            wavelength_end_nm=wavelength_end_nm,
            points=points,
        )

        figure, axes = self._create_figure(
            title="Refractive Index vs Wavelength",
            xlabel="Wavelength (nm)",
            ylabel="Refractive Index, n",
        )

        for material_name, results in dataset.items():
            wavelengths = [
                result.wavelength_nm
                for result in results
            ]

            indices = [
                result.refractive_index
                for result in results
            ]

            axes.plot(
                wavelengths,
                indices,
                linewidth=2,
                label=material_name,
            )

        return self._finalize(figure, axes)

    def plot_index_difference(
        self,
        material_1: OpticalMaterial,
        material_2: OpticalMaterial,
        wavelength_start_nm: float = 400.0,
        wavelength_end_nm: float = 700.0,
        points: int = 200,
    ) -> Figure:
        """
        Plot n(material_1) - n(material_2)
        across a wavelength interval.
        """

        self._validate_materials(
            [material_1, material_2],
            minimum=2,
        )

        dataset = generate_comparison_dataset(
            materials=[material_1, material_2],
            wavelength_start_nm=wavelength_start_nm,
            wavelength_end_nm=wavelength_end_nm,
            points=points,
        )

        first = dataset[material_1.name]
        second = dataset[material_2.name]

        wavelengths = [
            result.wavelength_nm
            for result in first
        ]

        differences = [
            result_1.refractive_index
            - result_2.refractive_index
            for result_1, result_2 in zip(
                first,
                second,
                strict=True,
            )
        ]

        figure, axes = self._create_figure(
            title="Refractive Index Difference",
            xlabel="Wavelength (nm)",
            ylabel="Index Difference, Δn",
        )

        axes.plot(
            wavelengths,
            differences,
            linewidth=2,
            label=f"{material_1.name} - {material_2.name}",
        )

        axes.axhline(
            0.0,
            color="gray",
            linestyle=":",
            linewidth=1,
        )

        return self._finalize(figure, axes)

    def plot_dispersion_comparison(
        self,
        materials: Iterable[OpticalMaterial],
        wavelength_min_nm: float = 450.0,
        wavelength_max_nm: float = 650.0,
    ) -> Figure:
        """
        Compare refractive index variation over
        a selected wavelength interval.

        Δn = n(lambda_min) - n(lambda_max)
        """

        material_list = self._validate_materials(materials)

        results = [
            calculate_material_dispersion(
                material,
                wavelength_min_nm,
                wavelength_max_nm,
            )
            for material in material_list
        ]

        names = [
            result.material_name
            for result in results
        ]

        differences = [
            result.index_difference
            for result in results
        ]

        figure, axes = self._create_figure(
            title="Optical Material Dispersion Comparison",
            xlabel="Optical Material",
            ylabel="Refractive Index Variation, Δn",
        )

        axes.bar(
            names,
            differences,
            alpha=0.85,
        )

        axes.tick_params(
            axis="x",
            rotation=20,
        )

        return self._finalize(
            figure,
            axes,
            legend=False,
        )

    def plot_index_at_wavelength(
        self,
        materials: Iterable[OpticalMaterial],
        wavelength_nm: float = 550.0,
    ) -> Figure:
        """
        Compare material refractive indices
        at a selected wavelength.
        """

        material_list = self._validate_materials(materials)

        results = compare_materials(
            material_list,
            wavelength_nm,
        )

        names = [
            result.material_name
            for result in results
        ]

        indices = [
            result.refractive_index
            for result in results
        ]

        figure, axes = self._create_figure(
            title=(
                "Refractive Index Comparison "
                f"at {wavelength_nm:g} nm"
            ),
            xlabel="Optical Material",
            ylabel="Refractive Index, n",
        )

        axes.bar(
            names,
            indices,
            alpha=0.85,
        )

        axes.tick_params(
            axis="x",
            rotation=20,
        )

        return self._finalize(
            figure,
            axes,
            legend=False,
        )

    @staticmethod
    def export_figure(
        figure: Figure,
        file_path: str | Path,
        dpi: int = 300,
    ) -> None:
        """
        Export a Matplotlib figure.

        Supported formats depend on the Matplotlib
        backend, including PNG, SVG, and PDF.
        """

        if not isinstance(figure, Figure):
            raise MaterialVisualizationError(
                "Expected a Matplotlib Figure."
            )

        path = Path(file_path)

        if path.suffix.lower() not in (
            ".png",
            ".svg",
            ".pdf",
        ):
            raise MaterialVisualizationError(
                "Supported export formats: PNG, SVG, PDF."
            )

        if (
            isinstance(dpi, bool)
            or not isinstance(dpi, int)
            or dpi <= 0
        ):
            raise MaterialVisualizationError(
                "DPI must be a positive integer."
            )

        figure.savefig(
            path,
            dpi=dpi,
            bbox_inches="tight",
        )
