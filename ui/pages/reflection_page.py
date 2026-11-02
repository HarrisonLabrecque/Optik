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
    """Reflection calculator with optical ray visualization."""

    def __init__(self):
        super().__init__()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)

        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        # Page title
        title = QLabel("Reflection Calculator")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Calculate and visualize the law of reflection."
        )
        description.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(description)

        # Input group
        input_group = QGroupBox("Incident Ray")
        input_layout = QHBoxLayout(input_group)

        input_label = QLabel("Incident Angle:")

        self.incident_angle = QDoubleSpinBox()
        self.incident_angle.setRange(0.0, 90.0)
        self.incident_angle.setDecimals(2)
        self.incident_angle.setSingleStep(1.0)
        self.incident_angle.setValue(45.0)
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

        # Result
        self.result_label = QLabel("Reflected Angle: --")
        self.result_label.setObjectName("resultLabel")

        layout.addWidget(self.result_label)

        # Optical visualization
        diagram_group = QGroupBox("Optical Ray Diagram")
        diagram_layout = QVBoxLayout(diagram_group)

        self.ray_diagram = RayDiagram()
        self.ray_diagram.setMinimumHeight(350)

        diagram_layout.addWidget(self.ray_diagram)

        layout.addWidget(diagram_group)

        # Finalize scroll area
        scroll_area.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)

        # Display initial calculation
        self.calculate()

    def calculate(self):
        """Calculate and visualize the reflected angle."""

        try:
            angle = self.incident_angle.value()

            reflected_angle = calculate_reflection(angle)

            self.result_label.setText(
                f"Reflected Angle: {reflected_angle:.2f}°"
            )

            self.ray_diagram.draw_reflection(angle)

        except ValueError as error:
            self.result_label.setText(
                "Reflected Angle: --"
            )

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )