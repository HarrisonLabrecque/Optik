from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QDoubleSpinBox,
    QGroupBox,
    QMessageBox,
)

from optics.refraction import calculate_refraction

from optics.total_internal_reflection import (
    calculate_critical_angle,
    is_total_internal_reflection,
)


class RefractionPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        title = QLabel("Refraction Calculator")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Calculate light refraction using Snell's law."
        )
        description.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(description)

        # Input group
        input_group = QGroupBox("Optical Properties")

        form = QFormLayout(input_group)

        self.n1_input = QDoubleSpinBox()
        self.n1_input.setRange(0.01, 10.0)
        self.n1_input.setDecimals(4)
        self.n1_input.setValue(1.0)

        self.n2_input = QDoubleSpinBox()
        self.n2_input.setRange(0.01, 10.0)
        self.n2_input.setDecimals(4)
        self.n2_input.setValue(1.5)

        self.angle_input = QDoubleSpinBox()
        self.angle_input.setRange(0, 90)
        self.angle_input.setDecimals(2)
        self.angle_input.setValue(30)
        self.angle_input.setSuffix("°")

        form.addRow("Refractive Index (n₁):", self.n1_input)
        form.addRow("Refractive Index (n₂):", self.n2_input)
        form.addRow("Incident Angle:", self.angle_input)

        layout.addWidget(input_group)

        # Calculate button
        self.calculate_button = QPushButton("Calculate Refraction")
        self.calculate_button.setObjectName("primaryButton")
        self.calculate_button.clicked.connect(self.calculate)

        layout.addWidget(self.calculate_button)

        # Results
        self.refraction_result = QLabel("Refracted Angle: --")
        self.refraction_result.setObjectName("resultLabel")

        self.critical_result = QLabel("Critical Angle: --")
        self.critical_result.setObjectName("resultLabel")

        self.tir_result = QLabel("Total Internal Reflection: --")
        self.tir_result.setObjectName("resultLabel")

        layout.addWidget(self.refraction_result)
        layout.addWidget(self.critical_result)
        layout.addWidget(self.tir_result)

        layout.addStretch()

    def calculate(self):
        n1 = self.n1_input.value()
        n2 = self.n2_input.value()
        angle = self.angle_input.value()

        try:
            # Check total internal reflection
            tir = is_total_internal_reflection(n1, n2, angle)

            self.tir_result.setText(
                f"Total Internal Reflection: {'Yes' if tir else 'No'}"
            )

            # Calculate critical angle when applicable
            if n1 > n2:
                critical = calculate_critical_angle(n1, n2)

                self.critical_result.setText(
                    f"Critical Angle: {critical:.2f}°"
                )
            else:
                self.critical_result.setText(
                    "Critical Angle: Not applicable"
                )

            # Calculate refraction
            if tir:
                self.refraction_result.setText(
                    "Refracted Angle: No transmitted ray (TIR)"
                )
            else:
                refracted = calculate_refraction(n1, n2, angle)

                self.refraction_result.setText(
                    f"Refracted Angle: {refracted:.2f}°"
                )

        except ValueError as error:
            self.refraction_result.setText("Refracted Angle: --")
            self.critical_result.setText("Critical Angle: --")
            self.tir_result.setText("Total Internal Reflection: --")

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )