from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDoubleSpinBox,
    QGroupBox,
    QMessageBox,
)

from optics.reflection import calculate_reflection


class ReflectionPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        title = QLabel("Reflection Calculator")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Calculate the reflected angle using the law of reflection."
        )
        description.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(description)

        # Input group
        input_group = QGroupBox("Incident Ray")

        input_layout = QHBoxLayout(input_group)

        input_label = QLabel("Incident Angle (°):")

        self.incident_angle = QDoubleSpinBox()
        self.incident_angle.setRange(0, 90)
        self.incident_angle.setDecimals(2)
        self.incident_angle.setValue(45)
        self.incident_angle.setSuffix("°")

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.incident_angle)

        layout.addWidget(input_group)

        # Calculate button
        self.calculate_button = QPushButton("Calculate Reflection")
        self.calculate_button.setObjectName("primaryButton")
        self.calculate_button.clicked.connect(self.calculate)

        layout.addWidget(self.calculate_button)

        # Result
        self.result_label = QLabel("Reflected Angle: --")
        self.result_label.setObjectName("resultLabel")

        layout.addWidget(self.result_label)

        layout.addStretch()

    def calculate(self):
        try:
            angle = self.incident_angle.value()

            result = calculate_reflection(angle)

            self.result_label.setText(
                f"Reflected Angle: {result:.2f}°"
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )