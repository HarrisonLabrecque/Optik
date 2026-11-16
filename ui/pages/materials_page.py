
"""
Optik - Optical Materials Page
Version: 0.5.0

PySide6 GUI for optical material comparison
and dispersion analysis.

Features:
    - Optical material selection
    - Four scientific visualization modes
    - Wavelength and sample controls
    - Embedded Matplotlib plots
    - Material comparison results
    - Light/dark theme support
    - PNG, SVG, and PDF export
    - Persistent user preferences
"""

import json
from pathlib import Path

from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from optics.material_repository import (
    MaterialRepository,
    MaterialRepositoryError,
)
from optics.material_comparison import (
    MaterialComparisonError,
    compare_materials,
)
from optics.optical_material import OpticalMaterialError

from visualization.material_comparison import (
    MaterialComparisonVisualizer,
    MaterialVisualizationError,
)


class MaterialsPage(QWidget):
    """
    Optical Materials & Dispersion GUI page.

    Designed for integration into Optik's
    QStackedWidget-based MainWindow.
    """

    calculation_completed = Signal()
    calculation_failed = Signal(str)

    PLOT_MODES = (
        "Refractive Index vs Wavelength",
        "Refractive Index Difference",
        "Dispersion Comparison",
        "Refractive Index at Wavelength",
    )

    def __init__(
        self,
        parent: QWidget | None = None,
        repository: MaterialRepository | None = None,
    ) -> None:
        super().__init__(parent)

        self.settings = QSettings("Optik", "Optik")

        self.repository = (
            repository
            if repository is not None
            else MaterialRepository()
        )

        self.visualizer = MaterialComparisonVisualizer()

        self.current_figure: Figure | None = None
        self.canvas: FigureCanvasQTAgg | None = None

        self.material_checkboxes: dict[str, QCheckBox] = {}

        self._build_ui()

        if repository is None:
            self._load_default_materials()

        self._populate_materials()
        self._restore_settings()
        self._update_control_states()

    def _build_ui(self) -> None:
        """Create the page layout."""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        title = QLabel("Optical Materials & Dispersion")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Compare optical materials, refractive indices, "
            "and wavelength-dependent dispersion."
        )
        subtitle.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)

        controls = self._create_controls()
        controls.setMinimumWidth(280)
        controls.setMaximumWidth(360)

        content_layout.addWidget(controls, 0)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        self.plot_container = QWidget()
        self.plot_layout = QVBoxLayout(self.plot_container)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)

        self.plot_placeholder = QLabel(
            "Select materials and click Calculate "
            "to generate a visualization."
        )
        self.plot_placeholder.setAlignment(Qt.AlignCenter)
        self.plot_placeholder.setWordWrap(True)
        self.plot_placeholder.setMinimumHeight(300)

        self.plot_layout.addWidget(self.plot_placeholder)

        right_layout.addWidget(self.plot_container, 1)

        results_group = QGroupBox("Calculation Results")
        results_layout = QVBoxLayout(results_group)

        self.results_label = QLabel(
            "No calculation has been performed."
        )
        self.results_label.setWordWrap(True)
        self.results_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        results_layout.addWidget(self.results_label)

        right_layout.addWidget(results_group)

        content_layout.addLayout(right_layout, 1)
        main_layout.addLayout(content_layout, 1)

        self.status_label = QLabel("Ready.")
        main_layout.addWidget(self.status_label)

    def _create_controls(self) -> QWidget:
        """Create the left-side control panel."""

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        material_group = QGroupBox("Optical Materials")
        material_layout = QVBoxLayout(material_group)

        self.material_scroll = QScrollArea()
        self.material_scroll.setWidgetResizable(True)
        self.material_scroll.setMinimumHeight(130)
        self.material_scroll.setMaximumHeight(210)

        self.material_list_widget = QWidget()
        self.material_list_layout = QVBoxLayout(
            self.material_list_widget
        )
        self.material_list_layout.setAlignment(Qt.AlignTop)

        self.material_scroll.setWidget(
            self.material_list_widget
        )

        material_layout.addWidget(self.material_scroll)
        layout.addWidget(material_group)

        plot_group = QGroupBox("Visualization Settings")
        plot_layout = QFormLayout(plot_group)

        self.plot_mode_combo = QComboBox()
        self.plot_mode_combo.addItems(self.PLOT_MODES)

        self.wavelength_start_spin = QDoubleSpinBox()
        self.wavelength_start_spin.setRange(1.0, 100000.0)
        self.wavelength_start_spin.setDecimals(2)
        self.wavelength_start_spin.setValue(400.0)
        self.wavelength_start_spin.setSuffix(" nm")

        self.wavelength_end_spin = QDoubleSpinBox()
        self.wavelength_end_spin.setRange(1.0, 100000.0)
        self.wavelength_end_spin.setDecimals(2)
        self.wavelength_end_spin.setValue(700.0)
        self.wavelength_end_spin.setSuffix(" nm")

        self.selected_wavelength_spin = QDoubleSpinBox()
        self.selected_wavelength_spin.setRange(
            1.0, 100000.0
        )
        self.selected_wavelength_spin.setDecimals(2)
        self.selected_wavelength_spin.setValue(550.0)
        self.selected_wavelength_spin.setSuffix(" nm")

        self.sample_count_spin = QSpinBox()
        self.sample_count_spin.setRange(2, 5000)
        self.sample_count_spin.setValue(200)

        plot_layout.addRow(
            "Plot Mode:", self.plot_mode_combo
        )
        plot_layout.addRow(
            "Start Wavelength:",
            self.wavelength_start_spin,
        )
        plot_layout.addRow(
            "End Wavelength:",
            self.wavelength_end_spin,
        )
        plot_layout.addRow(
            "Selected Wavelength:",
            self.selected_wavelength_spin,
        )
        plot_layout.addRow(
            "Samples:", self.sample_count_spin
        )

        layout.addWidget(plot_group)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(
            self.calculate
        )

        self.export_button = QPushButton("Export Plot")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(
            self.export_plot
        )

        layout.addWidget(self.calculate_button)
        layout.addWidget(self.export_button)

        layout.addStretch()

        self.plot_mode_combo.currentIndexChanged.connect(
            self._update_control_states
        )

        return panel

    def _load_default_materials(self) -> None:
        """Load the bundled JSON material catalog."""

        project_root = Path(__file__).resolve().parents[2]

        catalog_path = (
            project_root
            / "data"
            / "optical_materials.json"
        )

        try:
            with catalog_path.open(
                "r", encoding="utf-8"
            ) as file:
                material_data = json.load(file)

            self.repository = MaterialRepository.from_dict_list(
                material_data
            )

        except (
            OSError,
            json.JSONDecodeError,
            MaterialRepositoryError,
            OpticalMaterialError,
        ) as error:
            self.status_label.setText(
                f"Failed to load material catalog: {error}"
            )

    def _populate_materials(self) -> None:
        """Populate the material selection checkboxes."""

        for checkbox in self.material_checkboxes.values():
            self.material_list_layout.removeWidget(checkbox)
            checkbox.deleteLater()

        self.material_checkboxes.clear()

        materials = self.repository.get_all_materials()

        for material in materials:
            checkbox = QCheckBox(material.name)
            checkbox.setChecked(True)

            self.material_checkboxes[
                material.name
            ] = checkbox

            self.material_list_layout.addWidget(checkbox)

        if not materials:
            self.status_label.setText(
                "No optical materials are available."
            )

    def _get_selected_materials(self) -> list:
        """Return checked optical materials."""

        selected = []

        for name, checkbox in self.material_checkboxes.items():
            if not checkbox.isChecked():
                continue

            material = self.repository.get_material_by_name(
                name
            )

            if material is not None:
                selected.append(material)

        return selected

    def _update_control_states(self, *_args) -> None:
        """Enable controls relevant to the selected plot."""

        mode = self.plot_mode_combo.currentText()

        uses_range = mode in (
            self.PLOT_MODES[0],
            self.PLOT_MODES[1],
            self.PLOT_MODES[2],
        )

        uses_samples = mode in (
            self.PLOT_MODES[0],
            self.PLOT_MODES[1],
        )

        uses_selected_wavelength = (
            mode == self.PLOT_MODES[3]
        )

        self.wavelength_start_spin.setEnabled(
            uses_range
        )
        self.wavelength_end_spin.setEnabled(
            uses_range
        )
        self.sample_count_spin.setEnabled(
            uses_samples
        )
        self.selected_wavelength_spin.setEnabled(
            uses_selected_wavelength
        )

    def _validate_selection(self, materials: list) -> None:
        """Validate material selection and plot settings."""

        if not materials:
            raise MaterialVisualizationError(
                "Select at least one optical material."
            )

        mode = self.plot_mode_combo.currentText()

        if (
            mode == self.PLOT_MODES[1]
            and len(materials) != 2
        ):
            raise MaterialVisualizationError(
                "Index Difference requires exactly "
                "two selected materials."
            )

        if mode in self.PLOT_MODES[:3]:
            start = self.wavelength_start_spin.value()
            end = self.wavelength_end_spin.value()

            if start >= end:
                raise MaterialVisualizationError(
                    "Start wavelength must be less "
                    "than end wavelength."
                )

            for material in materials:
                if (
                    not material.supports_wavelength(start)
                    or not material.supports_wavelength(end)
                ):
                    raise MaterialVisualizationError(
                        f"{material.name} does not support "
                        f"the full {start:g}-{end:g} nm range."
                    )

        else:
            wavelength = self.selected_wavelength_spin.value()

            for material in materials:
                if not material.supports_wavelength(
                    wavelength
                ):
                    raise MaterialVisualizationError(
                        f"{material.name} does not support "
                        f"{wavelength:g} nm."
                    )

    def calculate(self) -> None:
        """Perform the selected visualization calculation."""

        try:
            materials = self._get_selected_materials()
            self._validate_selection(materials)

            mode = self.plot_mode_combo.currentText()

            start = self.wavelength_start_spin.value()
            end = self.wavelength_end_spin.value()
            wavelength = (
                self.selected_wavelength_spin.value()
            )
            points = self.sample_count_spin.value()

            if mode == self.PLOT_MODES[0]:
                figure = self.visualizer.plot_refractive_index(
                    materials,
                    start,
                    end,
                    points,
                )

            elif mode == self.PLOT_MODES[1]:
                figure = self.visualizer.plot_index_difference(
                    materials[0],
                    materials[1],
                    start,
                    end,
                    points,
                )

            elif mode == self.PLOT_MODES[2]:
                figure = (
                    self.visualizer.plot_dispersion_comparison(
                        materials,
                        start,
                        end,
                    )
                )

            else:
                figure = (
                    self.visualizer.plot_index_at_wavelength(
                        materials,
                        wavelength,
                    )
                )

            self._display_figure(figure)
            self._update_results(materials)

            self.status_label.setText(
                "Calculation completed successfully."
            )

            self._save_settings()
            self.calculation_completed.emit()

        except (
            MaterialComparisonError,
            MaterialVisualizationError,
            ValueError,
            ArithmeticError,
        ) as error:
            message = str(error)

            self.status_label.setText(
                f"Calculation failed: {message}"
            )

            self.calculation_failed.emit(message)

            QMessageBox.warning(
                self,
                "Calculation Error",
                message,
            )

    def _display_figure(self, figure: Figure) -> None:
        """Embed a Matplotlib figure in the page."""

        if self.canvas is not None:
            self.plot_layout.removeWidget(self.canvas)
            self.canvas.setParent(None)
            self.canvas.deleteLater()
            self.canvas = None

        self.plot_placeholder.hide()

        self.current_figure = figure

        self.canvas = FigureCanvasQTAgg(figure)
        self.canvas.setMinimumHeight(350)

        self.plot_layout.addWidget(self.canvas)
        self.canvas.draw()

        self.export_button.setEnabled(True)

    def _update_results(self, materials: list) -> None:
        """Display numerical results for selected materials."""

        mode = self.plot_mode_combo.currentText()

        if mode == self.PLOT_MODES[3]:
            wavelength = (
                self.selected_wavelength_spin.value()
            )
        else:
            wavelength = (
                self.wavelength_start_spin.value()
                + self.wavelength_end_spin.value()
            ) / 2.0

        results = compare_materials(
            materials,
            wavelength,
        )

        lines = [
            f"Comparison wavelength: {wavelength:g} nm",
            "",
        ]

        for result in results:
            lines.append(
                f"{result.material_name}: "
                f"n = {result.refractive_index:.6f}"
            )

        self.results_label.setText(
            "\n".join(lines)
        )

    def export_plot(self) -> None:
        """Export the current plot to PNG, SVG, or PDF."""

        if self.current_figure is None:
            return

        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export Optical Materials Plot",
            "optik_material_comparison.png",
            (
                "PNG Image (*.png);;"
                "SVG Image (*.svg);;"
                "PDF Document (*.pdf)"
            ),
        )

        if not file_path:
            return

        path = Path(file_path)

        if not path.suffix:
            if "SVG" in selected_filter:
                path = path.with_suffix(".svg")
            elif "PDF" in selected_filter:
                path = path.with_suffix(".pdf")
            else:
                path = path.with_suffix(".png")

        try:
            self.visualizer.export_figure(
                self.current_figure,
                path,
            )

            self.status_label.setText(
                f"Plot exported: {path.name}"
            )

        except (OSError, ValueError) as error:
            QMessageBox.warning(
                self,
                "Export Error",
                str(error),
            )

    def set_theme(self, theme: str) -> None:
        """Update the Matplotlib visualization theme."""

        self.visualizer.set_theme(theme)

        if self.current_figure is not None:
            self.calculate()

    def _save_settings(self) -> None:
        """Persist visualization preferences."""

        self.settings.setValue(
            "materials/plot_mode",
            self.plot_mode_combo.currentIndex(),
        )

        self.settings.setValue(
            "materials/wavelength_start",
            self.wavelength_start_spin.value(),
        )

        self.settings.setValue(
            "materials/wavelength_end",
            self.wavelength_end_spin.value(),
        )

        self.settings.setValue(
            "materials/selected_wavelength",
            self.selected_wavelength_spin.value(),
        )

        self.settings.setValue(
            "materials/sample_count",
            self.sample_count_spin.value(),
        )

        selected_names = [
            name
            for name, checkbox in self.material_checkboxes.items()
            if checkbox.isChecked()
        ]

        self.settings.setValue(
            "materials/selected_materials",
            selected_names,
        )

    def _restore_settings(self) -> None:
        """Restore previously saved preferences."""

        mode_index = int(
            self.settings.value(
                "materials/plot_mode",
                0,
            )
        )

        if 0 <= mode_index < len(self.PLOT_MODES):
            self.plot_mode_combo.setCurrentIndex(
                mode_index
            )

        self.wavelength_start_spin.setValue(
            float(
                self.settings.value(
                    "materials/wavelength_start",
                    400.0,
                )
            )
        )

        self.wavelength_end_spin.setValue(
            float(
                self.settings.value(
                    "materials/wavelength_end",
                    700.0,
                )
            )
        )

        self.selected_wavelength_spin.setValue(
            float(
                self.settings.value(
                    "materials/selected_wavelength",
                    550.0,
                )
            )
        )

        self.sample_count_spin.setValue(
            int(
                self.settings.value(
                    "materials/sample_count",
                    200,
                )
            )
        )

        saved_materials = self.settings.value(
            "materials/selected_materials",
            None,
        )

        if saved_materials is not None:
            if isinstance(saved_materials, str):
                saved_materials = [saved_materials]

            selected = set(saved_materials)

            for name, checkbox in (
                self.material_checkboxes.items()
            ):
                checkbox.setChecked(name in selected)

    def closeEvent(self, event) -> None:
        """Save preferences when the page closes."""

        self._save_settings()
        super().closeEvent(event)
