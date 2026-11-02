"""
Optik — Main Window
Version: 0.1.0

Features:
    - Sidebar navigation
    - Home dashboard navigation
    - Reflection and refraction calculators
    - Persistent Light/Dark themes
    - Saved calculation defaults
"""

from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from ui.widgets.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.reflection_page import ReflectionPage
from ui.pages.refraction_page import RefractionPage
from ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    """Main application window for Optik."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optik — Optics & Photonics")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)

        self.settings = QSettings("Optik", "Optik")

        self._setup_ui()
        self._connect_signals()
        self._load_stylesheet()

    def _setup_ui(self):
        """Create the main application interface."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()

        # Page stack
        self.stack = QStackedWidget()

        self.home_page = HomePage()
        self.reflection_page = ReflectionPage()
        self.refraction_page = RefractionPage()
        self.settings_page = SettingsPage()

        self.pages = {
            "home": self.home_page,
            "reflection": self.reflection_page,
            "refraction": self.refraction_page,
            "settings": self.settings_page,
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, 1)

        self.stack.setCurrentWidget(self.home_page)
        self.sidebar.set_active_page("home")

    def _connect_signals(self):
        """Connect navigation and settings signals."""

        # Sidebar navigation
        self.sidebar.page_changed.connect(
            self.change_page
        )

        # Home dashboard navigation
        self.home_page.reflection_card.open_button.clicked.connect(
            lambda: self.change_page("reflection")
        )

        self.home_page.refraction_card.open_button.clicked.connect(
            lambda: self.change_page("refraction")
        )

        # Theme switching
        self.settings_page.theme_changed.connect(
            self.apply_theme
        )

    def change_page(self, page_name: str):
        """Switch pages and synchronize the sidebar."""

        if page_name not in self.pages:
            raise ValueError(
                f"Unknown page: {page_name}"
            )

        self.stack.setCurrentWidget(
            self.pages[page_name]
        )

        self.sidebar.set_active_page(page_name)

        if page_name == "reflection":
            self.reflection_page.load_defaults()

        elif page_name == "refraction":
            self.refraction_page.load_defaults()

    def _load_stylesheet(self):
        """Load the saved application theme."""

        theme = self.settings.value(
            "appearance/theme",
            "Light",
            type=str,
        )

        self.apply_theme(theme)

    def apply_theme(self, theme: str):
        """Apply the selected Light or Dark stylesheet."""

        theme_files = {
            "Light": "light.qss",
            "Dark": "dark.qss",
        }

        stylesheet_name = theme_files.get(
            theme,
            "light.qss",
        )

        stylesheet_path = (
            Path(__file__).resolve().parent.parent
            / "ui"
            / "styles"
            / stylesheet_name
        )

        if not stylesheet_path.is_file():
            raise FileNotFoundError(
                f"Theme stylesheet not found: "
                f"{stylesheet_path}"
            )

        stylesheet = stylesheet_path.read_text(
            encoding="utf-8"
        )

        self.setStyleSheet(stylesheet)