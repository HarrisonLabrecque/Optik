"""
Optik — Sidebar Navigation
Version: 0.1.0

Features:
    - Home navigation
    - Reflection navigation
    - Refraction navigation
    - Settings navigation
    - Active page highlighting
    - Qt signal-based navigation
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class Sidebar(QWidget):
    """Navigation sidebar for the Optik desktop application."""

    # Emitted when the user selects a page.
    page_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(240)

        self.buttons = {}

        self._setup_ui()
        self.set_active_page("home")

    def _setup_ui(self):
        """Create the sidebar interface."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 20)
        layout.setSpacing(10)

        # ====================================================
        # APPLICATION BRANDING
        # ====================================================

        self.logo_label = QLabel("OPTIK")
        self.logo_label.setObjectName("sidebarLogo")
        self.logo_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.subtitle_label = QLabel("Optics & Photonics")
        self.subtitle_label.setObjectName("sidebarSubtitle")
        self.subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.logo_label)
        layout.addWidget(self.subtitle_label)

        layout.addSpacing(25)

        # ====================================================
        # NAVIGATION HEADER
        # ====================================================

        navigation_label = QLabel("NAVIGATION")
        navigation_label.setObjectName("sidebarSectionTitle")

        layout.addWidget(navigation_label)
        layout.addSpacing(8)

        # ====================================================
        # NAVIGATION BUTTONS
        # ====================================================

        self.home_button = self._create_button(
            "Home",
            "home",
        )

        self.reflection_button = self._create_button(
            "Reflection",
            "reflection",
        )

        self.refraction_button = self._create_button(
            "Refraction",
            "refraction",
        )

        layout.addWidget(self.home_button)
        layout.addWidget(self.reflection_button)
        layout.addWidget(self.refraction_button)

        layout.addStretch()

        # ====================================================
        # SETTINGS
        # ====================================================

        separator = QFrame()
        separator.setFrameShape(
            QFrame.Shape.HLine
        )
        separator.setObjectName("sidebarSeparator")

        layout.addWidget(separator)

        self.settings_button = self._create_button(
            "Settings",
            "settings",
        )

        layout.addWidget(self.settings_button)

        # ====================================================
        # VERSION
        # ====================================================

        self.version_label = QLabel("Version 0.1.0")
        self.version_label.setObjectName("sidebarVersion")
        self.version_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addSpacing(12)
        layout.addWidget(self.version_label)

    def _create_button(
        self,
        text: str,
        page_name: str,
    ) -> QPushButton:
        """Create a navigation button."""

        button = QPushButton(text)
        button.setObjectName("sidebarButton")

        button.setCheckable(True)

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setMinimumHeight(44)

        button.clicked.connect(
            lambda checked=False, page=page_name:
            self._navigate(page)
        )

        self.buttons[page_name] = button

        return button

    def _navigate(self, page_name: str):
        """Handle navigation button clicks."""

        self.set_active_page(page_name)

        self.page_changed.emit(page_name)

    def set_active_page(self, page_name: str):
        """Highlight the currently selected page."""

        if page_name not in self.buttons:
            raise ValueError(
                f"Unknown sidebar page: {page_name}"
            )

        for name, button in self.buttons.items():
            button.setChecked(name == page_name)

    def get_active_page(self) -> str:
        """Return the currently selected page."""

        for name, button in self.buttons.items():
            if button.isChecked():
                return name

        return "home"