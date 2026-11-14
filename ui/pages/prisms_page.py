
"""
Optik — Prism Optics & Dispersion Page
Version: 0.4.0

Features:
    - Prism refraction calculations
    - Minimum deviation and critical angle
    - Cauchy dispersion calculations
    - Four visualization modes
    - Shared Matplotlib canvas
    - Independent calculation error handling
    - Light and dark themes
    - Persistent settings
    - Diagram export
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QDoubleSpinBox,
    QSpinBox,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QSplitter,
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT,
)

from optics.prisms import (
    PrismError,
    TotalInternalReflectionError,
    calculate_prism_refraction,
    calculate_minimum_deviation,
    calculate_prism_critical_angle,
)

from optics.dispersion import (
    CauchyCoefficients,
    DispersionError,
    calculate_cauchy_index,
)

from visualization.prism_diagram import PrismDiagram
from visualization.dispersion_diagram import DispersionDiagram


# ============================================================
# DEFAULT VALUES
# ============================================================

DEFAULT_APEX_ANGLE = 60.0
DEFAULT_INCIDENT_ANGLE = 45.0
DEFAULT_REFRACTIVE_INDEX = 1.5

DEFAULT_WAVELENGTH = 550.0

DEFAULT_CAUCHY_A = 1.5046
DEFAULT_CAUCHY_B = 0.00420
DEFAULT_CAUCHY_C = 0.00012

DEFAULT_SAMPLES = 100


# ============================================================
# PRISM PAGE
# ============================================================

class PrismPage(QWidget):
    """Prism optics and dispersion interface."""

    def __init__(
        self,
        parent: QWidget | None = None,
        dark_mode: bool = False,
    ) -> None:
        super().__init__(parent)

        self.settings = QSettings("Optik", "Optik")
        self.dark_mode = bool(dark_mode)

        self._setup_ui()
        self._load_settings()
        self._connect_signals()

        self.calculate()

    # ========================================================
    # UI SETUP
    # ========================================================

    def _setup_ui(self) -> None:

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        title = QLabel("Prism Optics & Dispersion")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Explore prism refraction, angular deviation, "
            "and wavelength-dependent dispersion."
        )
        subtitle.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        splitter.addWidget(self._create_controls())
        splitter.addWidget(self._create_visualization())

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter, 1)

    # ========================================================
    # CONTROLS
    # ========================================================

    def _create_controls(self) -> QWidget:

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumWidth(300)

        container = QWidget()
        layout = QVBoxLayout(container)

        # PRISM PARAMETERS

        prism_group = QGroupBox("Prism Parameters")
        prism_grid = QGridLayout(prism_group)

        self.apex_spin = self._double_spin(
            DEFAULT_APEX_ANGLE, 0.01, 179.99, "°"
        )

        self.incident_spin = self._double_spin(
            DEFAULT_INCIDENT_ANGLE, 0.0, 89.99, "°"
        )

        self.index_spin = self._double_spin(
            DEFAULT_REFRACTIVE_INDEX,
            1.0001,
            5.0,
            "",
            decimals=4,
        )

        prism_grid.addWidget(QLabel("Apex Angle:"), 0, 0)
        prism_grid.addWidget(self.apex_spin, 0, 1)

        prism_grid.addWidget(QLabel("Incident Angle:"), 1, 0)
        prism_grid.addWidget(self.incident_spin, 1, 1)

        prism_grid.addWidget(QLabel("Refractive Index:"), 2, 0)
        prism_grid.addWidget(self.index_spin, 2, 1)

        layout.addWidget(prism_group)

        # DISPERSION PARAMETERS

        dispersion_group = QGroupBox("Dispersion Parameters")
        dispersion_grid = QGridLayout(dispersion_group)

        self.wavelength_spin = self._double_spin(
            DEFAULT_WAVELENGTH,
            100.0,
            2000.0,
            " nm",
        )

        self.cauchy_a_spin = self._double_spin(
            DEFAULT_CAUCHY_A,
            1.0,
            5.0,
            "",
            decimals=6,
        )

        self.cauchy_b_spin = self._double_spin(
            DEFAULT_CAUCHY_B,
            -1.0,
            1.0,
            "",
            decimals=8,
        )

        self.cauchy_c_spin = self._double_spin(
            DEFAULT_CAUCHY_C,
            -1.0,
            1.0,
            "",
            decimals=10,
        )

        self.samples_spin = QSpinBox()
        self.samples_spin.setRange(2, 10000)
        self.samples_spin.setValue(DEFAULT_SAMPLES)

        fields = [
            ("Wavelength:", self.wavelength_spin),
            ("Cauchy A:", self.cauchy_a_spin),
            ("Cauchy B:", self.cauchy_b_spin),
            ("Cauchy C:", self.cauchy_c_spin),
            ("Samples:", self.samples_spin),
        ]

        for row, (label, widget) in enumerate(fields):
            dispersion_grid.addWidget(QLabel(label), row, 0)
            dispersion_grid.addWidget(widget, row, 1)

        layout.addWidget(dispersion_group)

        # VISUALIZATION MODE

        visualization_group = QGroupBox("Visualization")
        visualization_layout = QVBoxLayout(visualization_group)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Prism Ray Diagram",
            "Refractive Index vs Wavelength",
            "Prism Deviation vs Wavelength",
            "Visible Spectrum",
        ])

        visualization_layout.addWidget(self.mode_combo)

        layout.addWidget(visualization_group)

        # ACTION BUTTONS

        actions = QHBoxLayout()

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setObjectName("primaryButton")

        self.reset_button = QPushButton("Reset")
        self.export_button = QPushButton("Export")

        actions.addWidget(self.calculate_button)
        actions.addWidget(self.reset_button)
        actions.addWidget(self.export_button)

        layout.addLayout(actions)

        # RESULTS

        results_group = QGroupBox("Calculation Results")
        results_layout = QVBoxLayout(results_group)

        self.results_label = QLabel(
            "Enter parameters and select Calculate."
        )

        self.results_label.setWordWrap(True)
        self.results_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        results_layout.addWidget(self.results_label)

        layout.addWidget(results_group)
        layout.addStretch()

        scroll.setWidget(container)

        return scroll

    # ========================================================
    # SHARED MATPLOTLIB CANVAS
    # ========================================================

    def _create_visualization(self) -> QWidget:

        container = QWidget()
        layout = QVBoxLayout(container)

        self.figure = Figure(figsize=(9, 6))
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar2QT(
            self.canvas,
            container,
        )

        self.prism_diagram = PrismDiagram(
            figure=self.figure,
            dark_mode=self.dark_mode,
        )

        self.dispersion_diagram = DispersionDiagram(
            figure=self.figure,
            dark_mode=self.dark_mode,
        )

        self.figure.clear()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas, 1)

        return container

    # ========================================================
    # SPIN BOX HELPER
    # ========================================================

    @staticmethod
    def _double_spin(
        value: float,
        minimum: float,
        maximum: float,
        suffix: str,
        decimals: int = 2,
    ) -> QDoubleSpinBox:

        spin = QDoubleSpinBox()

        spin.setDecimals(decimals)
        spin.setRange(minimum, maximum)
        spin.setValue(value)
        spin.setSuffix(suffix)

        return spin

    # ========================================================
    # SETTINGS
    # ========================================================

    def _load_settings(self) -> None:

        values = [
            (
                self.apex_spin,
                "prism/apex_angle",
                DEFAULT_APEX_ANGLE,
            ),
            (
                self.incident_spin,
                "prism/incident_angle",
                DEFAULT_INCIDENT_ANGLE,
            ),
            (
                self.index_spin,
                "prism/refractive_index",
                DEFAULT_REFRACTIVE_INDEX,
            ),
            (
                self.wavelength_spin,
                "prism/wavelength",
                DEFAULT_WAVELENGTH,
            ),
            (
                self.cauchy_a_spin,
                "prism/cauchy_a",
                DEFAULT_CAUCHY_A,
            ),
            (
                self.cauchy_b_spin,
                "prism/cauchy_b",
                DEFAULT_CAUCHY_B,
            ),
            (
                self.cauchy_c_spin,
                "prism/cauchy_c",
                DEFAULT_CAUCHY_C,
            ),
            (
                self.samples_spin,
                "prism/samples",
                DEFAULT_SAMPLES,
            ),
        ]

        for widget, key, default in values:
            value = self.settings.value(key, default)

            try:
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                else:
                    widget.setValue(float(value))
            except (TypeError, ValueError):
                widget.setValue(default)

    def _save_settings(self) -> None:

        values = {
            "prism/apex_angle": self.apex_spin.value(),
            "prism/incident_angle": self.incident_spin.value(),
            "prism/refractive_index": self.index_spin.value(),
            "prism/wavelength": self.wavelength_spin.value(),
            "prism/cauchy_a": self.cauchy_a_spin.value(),
            "prism/cauchy_b": self.cauchy_b_spin.value(),
            "prism/cauchy_c": self.cauchy_c_spin.value(),
            "prism/samples": self.samples_spin.value(),
        }

        for key, value in values.items():
            self.settings.setValue(key, value)

    # ========================================================
    # SIGNALS
    # ========================================================

    def _connect_signals(self) -> None:

        self.calculate_button.clicked.connect(
            self.calculate
        )

        self.reset_button.clicked.connect(
            self.reset
        )

        self.export_button.clicked.connect(
            self.export_diagram
        )

        self.mode_combo.currentIndexChanged.connect(
            self.calculate
        )

    # ========================================================
    # CALCULATIONS
    # ========================================================

    def calculate(self) -> None:
        """
        Calculate prism optics and dispersion results.

        Each optical calculation is handled independently.
        Unsupported prism geometries do not erase other
        valid results.

        Visualization failures are handled separately.
        """

        # ----------------------------------------------------
        # READ USER INPUTS
        # ----------------------------------------------------

        apex = self.apex_spin.value()
        incident = self.incident_spin.value()
        index = self.index_spin.value()
        wavelength = self.wavelength_spin.value()
        samples = self.samples_spin.value()

        coefficients = CauchyCoefficients(
            A=self.cauchy_a_spin.value(),
            B=self.cauchy_b_spin.value(),
            C=self.cauchy_c_spin.value(),
        )

        # ----------------------------------------------------
        # CAUCHY REFRACTIVE INDEX
        # ----------------------------------------------------

        try:
            cauchy_index = calculate_cauchy_index(
                wavelength,
                coefficients,
            )

        except (DispersionError, ValueError) as exc:
            self.results_label.setText(
                f"Calculation Error:\n{exc}"
            )

            self.figure.clear()
            self.canvas.draw_idle()
            return

        # ----------------------------------------------------
        # CRITICAL ANGLE
        # ----------------------------------------------------

        try:
            critical_angle = calculate_prism_critical_angle(
                index
            )

            critical_text = f"{critical_angle:.3f}°"

        except PrismError as exc:
            critical_text = f"Unavailable: {exc}"

        # ----------------------------------------------------
        # MINIMUM DEVIATION
        # ----------------------------------------------------

        try:
            minimum_deviation = calculate_minimum_deviation(
                apex,
                index,
            )

            minimum_text = f"{minimum_deviation:.3f}°"

        except PrismError:
            minimum_text = (
                "Unavailable for this prism geometry"
            )

        # ----------------------------------------------------
        # PRISM REFRACTION
        # ----------------------------------------------------

        try:
            result = calculate_prism_refraction(
                apex,
                incident,
                index,
            )

            prism_results = (
                f"First Refraction: "
                f"{result.first_refracted_angle:.3f}°\n"
                f"Second Internal Angle: "
                f"{result.second_internal_angle:.3f}°\n"
                f"Emergent Angle: "
                f"{result.emergent_angle:.3f}°\n"
                f"Deviation Angle: "
                f"{result.deviation_angle:.3f}°"
            )

        except TotalInternalReflectionError:
            prism_results = (
                "Total internal reflection occurs "
                "at the second prism surface."
            )

        except PrismError as exc:
            prism_results = (
                "Prism refraction unavailable for "
                "this geometry.\n"
                f"Reason: {exc}"
            )

        # ----------------------------------------------------
        # DISPLAY RESULTS
        # ----------------------------------------------------

        self.results_label.setText(
            f"Prism Apex Angle: {apex:.2f}°\n"
            f"Incident Angle: {incident:.2f}°\n"
            f"Refractive Index: {index:.4f}\n\n"
            f"{prism_results}\n\n"
            f"Minimum Deviation: {minimum_text}\n"
            f"Critical Angle: {critical_text}\n\n"
            f"Wavelength: {wavelength:.1f} nm\n"
            f"Cauchy Index: {cauchy_index:.6f}"
        )

        # ----------------------------------------------------
        # SAVE SETTINGS
        # ----------------------------------------------------

        self._save_settings()

        # ----------------------------------------------------
        # UPDATE VISUALIZATION
        # ----------------------------------------------------

        try:
            self._update_visualization(
                apex,
                incident,
                index,
                coefficients,
                samples,
            )

        except (PrismError, DispersionError, ValueError) as exc:
            self.figure.clear()
            self.canvas.draw_idle()

            self.results_label.setText(
                self.results_label.text()
                + f"\n\nVisualization unavailable: {exc}"
            )

    # ========================================================
    # VISUALIZATION UPDATE
    # ========================================================

    def _update_visualization(
        self,
        apex: float,
        incident: float,
        index: float,
        coefficients: CauchyCoefficients,
        samples: int,
    ) -> None:
        """Draw the selected visualization using one canvas."""

        mode = self.mode_combo.currentIndex()

        self.figure.clear()

        if mode == 0:
            self.prism_diagram.ax = (
                self.figure.add_subplot(111)
            )

            self.prism_diagram.draw(
                apex_angle=apex,
                incident_angle=incident,
                refractive_index=index,
            )

        else:
            self.dispersion_diagram.ax = (
                self.figure.add_subplot(111)
            )

            if mode == 1:
                self.dispersion_diagram.draw_refractive_index(
                    coefficients=coefficients,
                    samples=samples,
                )

            elif mode == 2:
                self.dispersion_diagram.draw_prism_deviation(
                    apex_angle=apex,
                    incident_angle=incident,
                    coefficients=coefficients,
                    samples=samples,
                )

            elif mode == 3:
                self.dispersion_diagram.draw_visible_spectrum(
                    samples=samples,
                )

        self.canvas.draw_idle()

    # ========================================================
    # RESET
    # ========================================================

    def reset(self) -> None:

        self.apex_spin.setValue(DEFAULT_APEX_ANGLE)
        self.incident_spin.setValue(DEFAULT_INCIDENT_ANGLE)
        self.index_spin.setValue(DEFAULT_REFRACTIVE_INDEX)

        self.wavelength_spin.setValue(DEFAULT_WAVELENGTH)

        self.cauchy_a_spin.setValue(DEFAULT_CAUCHY_A)
        self.cauchy_b_spin.setValue(DEFAULT_CAUCHY_B)
        self.cauchy_c_spin.setValue(DEFAULT_CAUCHY_C)

        self.samples_spin.setValue(DEFAULT_SAMPLES)

        self.mode_combo.setCurrentIndex(0)

        self.calculate()

    # ========================================================
    # THEME
    # ========================================================

    def set_dark_mode(self, enabled: bool) -> None:

        self.dark_mode = bool(enabled)

        self.prism_diagram.set_dark_mode(enabled)
        self.dispersion_diagram.set_dark_mode(enabled)

        self.canvas.draw_idle()

    # ========================================================
    # EXPORT
    # ========================================================

    def export_diagram(self) -> None:

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Prism Diagram",
            str(Path.home() / "prism_diagram.png"),
            "PNG Images (*.png);;"
            "SVG Images (*.svg);;"
            "PDF Documents (*.pdf)",
        )

        if not filename:
            return

        try:
            self.figure.savefig(
                filename,
                dpi=150,
                bbox_inches="tight",
            )

        except (OSError, ValueError) as exc:
            QMessageBox.warning(
                self,
                "Export Error",
                str(exc),
            )


# ============================================================
# STANDALONE PREVIEW
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    page = PrismPage()
    page.resize(1200, 750)
    page.show()

    sys.exit(app.exec())
