"""
Optik — Settings Page
Version: 0.1.0
"""

from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QPushButton,
    QGroupBox,
    QScrollArea,
    QFrame,
    QMessageBox,
)


class SettingsPage(QWidget):
    """Application preferences and information."""

    def __init__(self):
        super().__init__()

        self.settings = QSettings("Optik", "Optik")
        self._setup_ui()
        self.load_settings()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        title = QLabel("Settings")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Configure your Optik preferences and "
            "default calculation parameters."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Appearance
        appearance_group = QGroupBox("Appearance")
        appearance_form = QFormLayout(appearance_group)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])

        appearance_form.addRow(
            "Application Theme:",
            self.theme_combo,
        )

        layout.addWidget(appearance_group)

        # Calculation defaults
        calculation_group = QGroupBox("Calculation Defaults")
        calculation_form = QFormLayout(calculation_group)

        self.default_angle = QDoubleSpinBox()
        self.default_angle.setRange(0.0, 90.0)
        self.default_angle.setDecimals(2)
        self.default_angle.setValue(45.0)
        self.default_angle.setSuffix("°")

        self.default_n1 = QDoubleSpinBox()
        self.default_n1.setRange(0.01, 10.0)
        self.default_n1.setDecimals(4)
        self.default_n1.setValue(1.0)

        self.default_n2 = QDoubleSpinBox()
        self.default_n2.setRange(0.01, 10.0)
        self.default_n2.setDecimals(4)
        self.default_n2.setValue(1.5)

        calculation_form.addRow(
            "Default Incident Angle:",
            self.default_angle,
        )

        calculation_form.addRow(
            "Default Refractive Index (n₁):",
            self.default_n1,
        )

        calculation_form.addRow(
            "Default Refractive Index (n₂):",
            self.default_n2,
        )

        layout.addWidget(calculation_group)

        # Actions
        self.save_button = QPushButton("Save Settings")
        self.save_button.setObjectName("primaryButton")

        self.reset_button = QPushButton("Restore Defaults")

        self.save_button.clicked.connect(self.save_settings)
        self.reset_button.clicked.connect(self.reset_settings)

        layout.addWidget(self.save_button)
        layout.addWidget(self.reset_button)

        # About
        about_group = QGroupBox("About Optik")
        about_layout = QVBoxLayout(about_group)

        about_text = QLabel(
            "Optik\n"
            "Version 0.1.0\n\n"
            "An open-source desktop application for "
            "optics and photonics calculations "
            "and scientific visualization.\n\n"
            "Developed with Python, PySide6, and Matplotlib.\n"
            "License: MIT"
        )

        about_text.setWordWrap(True)
        about_text.setObjectName("bodyText")

        about_layout.addWidget(about_text)

        layout.addWidget(about_group)
        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def load_settings(self):
        """Load stored application preferences."""

        theme = self.settings.value(
            "appearance/theme",
            "Dark",
            type=str,
        )

        angle = self.settings.value(
            "calculations/angle",
            45.0,
            type=float,
        )

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

        if theme not in ("Dark", "Light"):
            theme = "Dark"

        self.theme_combo.setCurrentText(theme)
        self.default_angle.setValue(angle)
        self.default_n1.setValue(n1)
        self.default_n2.setValue(n2)

    def save_settings(self):
        """Persist user preferences."""

        self.settings.setValue(
            "appearance/theme",
            self.theme_combo.currentText(),
        )

        self.settings.setValue(
            "calculations/angle",
            self.default_angle.value(),
        )

        self.settings.setValue(
            "calculations/n1",
            self.default_n1.value(),
        )

        self.settings.setValue(
            "calculations/n2",
            self.default_n2.value(),
        )

        self.settings.sync()

        if self.settings.status() != QSettings.Status.NoError:
            QMessageBox.warning(
                self,
                "Settings Error",
                "Unable to save application preferences.",
            )
            return

        QMessageBox.information(
            self,
            "Settings Saved",
            "Your preferences have been saved successfully.",
        )

    def reset_settings(self):
        """Restore default application preferences."""

        self.theme_combo.setCurrentText("Dark")
        self.default_angle.setValue(45.0)
        self.default_n1.setValue(1.0)
        self.default_n2.setValue(1.5)

        self.save_settings()