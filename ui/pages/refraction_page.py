"""
Optik — Refraction Calculator
Version: 0.1.0

Features:
    - Snell's law calculation
    - Critical-angle calculation
    - Total internal reflection detection
    - Saved calculation defaults
    - Interactive ray visualization
"""

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QDoubleSpinBox,
    QGroupBox,
    QMessageBox,
    QScrollArea,
)

from optics.refraction import calculate_refraction
from optics.total_internal_reflection import (
    calculate_critical_angle,
    is_total_internal_reflection,
)
from visualization.ray_diagram import RayDiagram


class RefractionPage(QWidget):
    """Refraction calculator interface."""

    def __init__(self):
        super().__init__()

        self.settings = QSettings("Optik", "Optik")

        self._setup_ui()
        self.load_defaults()
        self.calculate()

    def _setup_ui(self):
        """Initialize the refraction calculator UI."""

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        # Title
        title = QLabel("Refraction Calculator")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Calculate and visualize light refraction "
            "using Snell's law."
        )
        description.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(description)

        # Inputs
        input_group = QGroupBox("Optical Properties")
        form = QFormLayout(input_group)

        self.n1_input = QDoubleSpinBox()
        self.n1_input.setRange(0.01, 10.0)
        self.n1_input.setDecimals(4)
        self.n1_input.setSingleStep(0.01)

        self.n2_input = QDoubleSpinBox()
        self.n2_input.setRange(0.01, 10.0)
        self.n2_input.setDecimals(4)
        self.n2_input.setSingleStep(0.01)

        self.angle_input = QDoubleSpinBox()
        self.angle_input.setRange(0.0, 90.0)
        self.angle_input.setDecimals(2)
        self.angle_input.setSingleStep(1.0)
        self.angle_input.setSuffix("°")

        form.addRow(
            "Refractive Index (n₁):",
            self.n1_input,
        )

        form.addRow(
            "Refractive Index (n₂):",
            self.n2_input,
        )

        form.addRow(
            "Incident Angle:",
            self.angle_input,
        )

        layout.addWidget(input_group)

        # Calculate button
        self.calculate_button = QPushButton(
            "Calculate Refraction"
        )
        self.calculate_button.setObjectName("primaryButton")
        self.calculate_button.clicked.connect(self.calculate)

        layout.addWidget(self.calculate_button)

        # Results
        results_group = QGroupBox("Calculation Results")
        results_layout = QVBoxLayout(results_group)

        self.refraction_result = QLabel(
            "Refracted Angle: --"
        )

        self.critical_result = QLabel(
            "Critical Angle: --"
        )

        self.tir_result = QLabel(
            "Total Internal Reflection: --"
        )

        for label in (
            self.refraction_result,
            self.critical_result,
            self.tir_result,
        ):
            label.setObjectName("resultLabel")
            results_layout.addWidget(label)

        layout.addWidget(results_group)

        # Ray diagram
        diagram_group = QGroupBox("Optical Ray Diagram")
        diagram_layout = QVBoxLayout(diagram_group)

        self.ray_diagram = RayDiagram()
        self.ray_diagram.setMinimumHeight(350)

        diagram_layout.addWidget(self.ray_diagram)

        layout.addWidget(diagram_group)

        scroll_area.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)

    def load_defaults(self):
        """Load saved calculation defaults."""

        n1 = self.settings.value(
            "calculations/n1",
            1.0,
            type=float,
        )

        n2 = self.settings.value(
            "calculations/n2",
            1.5,
            type=float,
        )

        angle = self.settings.value(
            "calculations/angle",
            45.0,
            type=float,
        )

        self.n1_input.setValue(n1)
        self.n2_input.setValue(n2)
        self.angle_input.setValue(angle)

        self.calculate()

    def calculate(self):
        """Calculate refraction and update the ray diagram."""

        n1 = self.n1_input.value()
        n2 = self.n2_input.value()
        incident_angle = self.angle_input.value()

        try:
            tir = is_total_internal_reflection(
                n1,
                n2,
                incident_angle,
            )

            # Critical angle
            if n1 > n2:
                critical_angle = calculate_critical_angle(
                    n1,
                    n2,
                )

                self.critical_result.setText(
                    f"Critical Angle: {critical_angle:.2f}°"
                )

            else:
                self.critical_result.setText(
                    "Critical Angle: Not applicable"
                )

            # Total internal reflection
            self.tir_result.setText(
                "Total Internal Reflection: "
                f"{'Yes' if tir else 'No'}"
            )

            # Refraction
            if tir:
                self.refraction_result.setText(
                    "Refracted Angle: "
                    "No transmitted ray (TIR)"
                )

            else:
                refracted_angle = calculate_refraction(
                    n1,
                    n2,
                    incident_angle,
                )

                self.refraction_result.setText(
                    f"Refracted Angle: "
                    f"{refracted_angle:.2f}°"
                )

            # Update diagram
            self.ray_diagram.draw_refraction(
                n1,
                n2,
                incident_angle,
            )

        except ValueError as error:
            self.refraction_result.setText(
                "Refracted Angle: --"
            )

            self.critical_result.setText(
                "Critical Angle: --"
            )

            self.tir_result.setText(
                "Total Internal Reflection: --"
            )

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error),
            )