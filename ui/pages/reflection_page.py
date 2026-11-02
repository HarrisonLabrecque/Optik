"""
Optik — Reflection Calculator
Version: 0.1.0

Features:
    - Reflection calculation
    - Saved default incident angle
    - Interactive ray visualization
    - Input validation
"""

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDoubleSpinBox,
    QGroupBox,
    QMessageBox,
    QScrollArea,
)

from optics.reflection import calculate_reflection
from visualization.ray_diagram import RayDiagram


class ReflectionPage(QWidget):
    """Reflection calculator interface."""

    def __init__(self):
        super().__init__()

        self.settings = QSettings("Optik", "Optik")

        self._setup_ui()
        self.load_defaults()
        self.calculate()

    def _setup_ui(self):
        """Initialize the reflection calculator UI."""

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        # Title
        title = QLabel("Reflection Calculator")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Calculate and visualize the law of reflection."
        )
        description.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(description)

        # Input
        input_group = QGroupBox("Incident Ray")
        input_layout = QHBoxLayout(input_group)

        input_label = QLabel("Incident Angle:")

        self.incident_angle = QDoubleSpinBox()
        self.incident_angle.setRange(0.0, 90.0)
        self.incident_angle.setDecimals(2)
        self.incident_angle.setSingleStep(1.0)
        self.incident_angle.setSuffix("°")

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.incident_angle)

        layout.addWidget(input_group)

        # Calculate button
        self.calculate_button = QPushButton(
            "Calculate Reflection"
        )
        self.calculate_button.setObjectName("primaryButton")
        self.calculate_button.clicked.connect(self.calculate)

        layout.addWidget(self.calculate_button)

        # Results
        self.result_label = QLabel("Reflected Angle: --")
        self.result_label.setObjectName("resultLabel")

        layout.addWidget(self.result_label)

        # Diagram
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
        """Load the default incident angle from settings."""

        angle = self.settings.value(
            "calculations/angle",
            45.0,
            type=float,
        )

        self.incident_angle.setValue(angle)
        self.calculate()

    def calculate(self):
        """Calculate and visualize reflection."""

        try:
            angle = self.incident_angle.value()

            reflected_angle = calculate_reflection(angle)

            self.result_label.setText(
                f"Reflected Angle: {reflected_angle:.2f}°"
            )

            self.ray_diagram.draw_reflection(angle)

        except ValueError as error:
            self.result_label.setText("Reflected Angle: --")

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error),
            )