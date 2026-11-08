
"""
Optik - Main Application Window
Version: 0.3.0

Pages:
    0 - Home
    1 - Reflection
    2 - Refraction
    3 - Thin Lenses
    4 - Mirror Optics
    5 - Settings

Features:
    - Sidebar navigation
    - Stacked page management
    - Light and dark themes
    - Persistent theme and page settings
    - Home page navigation support
    - Keyboard shortcuts
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QSettings, Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QFrame,
    QSizePolicy,
)

from ui.pages.home_page import HomePage
from ui.pages.reflection_page import ReflectionPage
from ui.pages.refraction_page import RefractionPage
from ui.pages.lens_page import LensPage
from ui.pages.mirror_page import MirrorPage
from ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    """Main window for the Optik desktop application."""

    page_changed = Signal(int)
    theme_changed = Signal(str)

    HOME = 0
    REFLECTION = 1
    REFRACTION = 2
    LENS = 3
    MIRROR = 4
    SETTINGS = 5

    PAGE_NAMES = (
        "Home",
        "Reflection",
        "Refraction",
        "Thin Lenses",
        "Mirror Optics",
        "Settings",
    )

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings("Optik", "Optik")

        self.current_theme = "light"
        self.current_page = self.HOME

        self.nav_buttons = {}

        self._setup_window()
        self._setup_ui()
        self._setup_shortcuts()
        self._connect_page_signals()
        self._restore_settings()

    # ========================================================
    # WINDOW SETUP
    # ========================================================

    def _setup_window(self):
        self.setWindowTitle("Optik v0.3.0 - Optics & Photonics")
        self.setMinimumSize(900, 650)
        self.resize(1250, 850)

    def _setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._create_sidebar()
        self._create_pages()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def _create_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(220)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(15, 20, 15, 20)
        self.sidebar_layout.setSpacing(8)

        self.logo_label = QLabel("OPTIK")
        self.logo_label.setObjectName("sidebarLogo")
        self.logo_label.setAlignment(Qt.AlignCenter)

        logo_font = self.logo_label.font()
        logo_font.setPointSize(20)
        logo_font.setBold(True)
        self.logo_label.setFont(logo_font)

        self.version_label = QLabel("Version 0.3.0")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setObjectName("versionLabel")

        self.sidebar_layout.addWidget(self.logo_label)
        self.sidebar_layout.addWidget(self.version_label)
        self.sidebar_layout.addSpacing(25)

        navigation = [
            (self.HOME, "Home"),
            (self.REFLECTION, "Reflection"),
            (self.REFRACTION, "Refraction"),
            (self.LENS, "Thin Lenses"),
            (self.MIRROR, "Mirror Optics"),
        ]

        for index, label in navigation:
            self._add_navigation_button(index, label)

        self.sidebar_layout.addStretch()

        self._add_navigation_button(
            self.SETTINGS,
            "Settings",
        )

        self.main_layout.addWidget(self.sidebar)

    def _add_navigation_button(self, index, label):
        button = QPushButton(label)
        button.setObjectName(f"navButton{index}")
        button.setCheckable(True)
        button.setMinimumHeight(42)
        button.setCursor(Qt.PointingHandCursor)

        button.clicked.connect(
            lambda checked=False, page=index: self.navigate_to(page)
        )

        self.nav_buttons[index] = button
        self.sidebar_layout.addWidget(button)

    # ========================================================
    # PAGES
    # ========================================================

    def _create_pages(self):
        self.stack = QStackedWidget()
        self.stacked_widget = self.stack

        self.home_page = HomePage()
        self.reflection_page = ReflectionPage()
        self.refraction_page = RefractionPage()
        self.lens_page = LensPage()
        self.mirror_page = MirrorPage()
        self.settings_page = SettingsPage()

        self.pages = (
            self.home_page,
            self.reflection_page,
            self.refraction_page,
            self.lens_page,
            self.mirror_page,
            self.settings_page,
        )

        for page in self.pages:
            self.stack.addWidget(page)

        self.main_layout.addWidget(self.stack, 1)

    def navigate_to(self, index: int):
        """Navigate to a page by its index."""
        if not isinstance(index, int):
            raise ValueError("Page index must be an integer.")

        if not 0 <= index < self.stack.count():
            raise ValueError(f"Invalid page index: {index}")

        self.stack.setCurrentIndex(index)
        self.current_page = index

        self._update_navigation_buttons()

        self.settings.setValue("window/last_page", index)

        self.page_changed.emit(index)

    def _update_navigation_buttons(self):
        for index, button in self.nav_buttons.items():
            button.setChecked(index == self.current_page)

    # ========================================================
    # PAGE SIGNAL CONNECTIONS
    # ========================================================

    def _connect_page_signals(self):
        """
        Connect supported page navigation signals.

        Different Optik versions may expose different
        signal names. Only existing signals are connected.
        """

        self._connect_navigation_signal(
            self.home_page,
            "navigate_to",
        )

        self._connect_navigation_signal(
            self.home_page,
            "page_requested",
        )

        self._connect_navigation_signal(
            self.home_page,
            "navigation_requested",
        )

        self._connect_navigation_signal(
            self.home_page,
            "page_changed",
        )

        self._connect_theme_signals()

    def _connect_navigation_signal(self, page, signal_name):
        signal = getattr(page, signal_name, None)

        if signal is None or not hasattr(signal, "connect"):
            return

        signal.connect(self._handle_navigation_request)

    def _handle_navigation_request(self, destination):
        """Handle navigation requests from child pages."""
        if isinstance(destination, int):
            if 0 <= destination < self.stack.count():
                self.navigate_to(destination)
            return

        if isinstance(destination, str):
            names = {
                "home": self.HOME,
                "reflection": self.REFLECTION,
                "refraction": self.REFRACTION,
                "lens": self.LENS,
                "lenses": self.LENS,
                "thin lens": self.LENS,
                "thin lenses": self.LENS,
                "mirror": self.MIRROR,
                "mirrors": self.MIRROR,
                "mirror optics": self.MIRROR,
                "settings": self.SETTINGS,
            }

            index = names.get(destination.strip().lower())

            if index is not None:
                self.navigate_to(index)

    def _connect_theme_signals(self):
        """Connect theme signals exposed by SettingsPage."""
        for signal_name in (
            "theme_changed",
            "theme_selected",
            "theme_requested",
        ):
            signal = getattr(
                self.settings_page,
                signal_name,
                None,
            )

            if signal is not None and hasattr(signal, "connect"):
                signal.connect(self.set_theme)

    # ========================================================
    # THEMES
    # ========================================================

    def set_theme(self, theme: str):
        """Apply the selected theme to the application."""
        normalized = str(theme).strip().lower()

        if normalized not in ("light", "dark"):
            normalized = "light"

        self.current_theme = normalized

        self._apply_window_theme()

        for page in self.pages:
            if hasattr(page, "set_theme"):
                page.set_theme(normalized)

        self.settings.setValue(
            "appearance/theme",
            normalized,
        )

        self.theme_changed.emit(normalized)

    def _apply_window_theme(self):
        dark = self.current_theme == "dark"

        if dark:
            background = "#111827"
            sidebar_background = "#172033"
            foreground = "#f9fafb"
            muted = "#9ca3af"
            button_background = "#253249"
            hover_background = "#344563"
            selected_background = "#2563eb"
            border = "#374151"
        else:
            background = "#f8fafc"
            sidebar_background = "#e9eef5"
            foreground = "#172033"
            muted = "#64748b"
            button_background = "#ffffff"
            hover_background = "#dbeafe"
            selected_background = "#2563eb"
            border = "#cbd5e1"

        self.central_widget.setStyleSheet(
            f"""
            QWidget {{
                background-color: {background};
                color: {foreground};
            }}

            QFrame#sidebar {{
                background-color: {sidebar_background};
                border-right: 1px solid {border};
            }}

            QLabel#sidebarLogo {{
                color: {foreground};
                background: transparent;
            }}

            QLabel#versionLabel {{
                color: {muted};
                background: transparent;
            }}

            QPushButton[checkable="true"] {{
                background-color: {button_background};
                color: {foreground};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 10px;
                text-align: left;
            }}

            QPushButton[checkable="true"]:hover {{
                background-color: {hover_background};
            }}

            QPushButton[checkable="true"]:checked {{
                background-color: {selected_background};
                color: white;
                border-color: {selected_background};
            }}
            """
        )

    # ========================================================
    # KEYBOARD SHORTCUTS
    # ========================================================

    def _setup_shortcuts(self):
        shortcuts = [
            ("Ctrl+1", self.HOME),
            ("Ctrl+2", self.REFLECTION),
            ("Ctrl+3", self.REFRACTION),
            ("Ctrl+4", self.LENS),
            ("Ctrl+5", self.MIRROR),
            ("Ctrl+6", self.SETTINGS),
        ]

        self.shortcut_actions = []

        for key_sequence, index in shortcuts:
            action = QAction(self)
            action.setShortcut(QKeySequence(key_sequence))

            action.triggered.connect(
                lambda checked=False, page=index: self.navigate_to(page)
            )

            self.addAction(action)
            self.shortcut_actions.append(action)

    # ========================================================
    # SETTINGS PERSISTENCE
    # ========================================================

    def _restore_settings(self):
        theme = self.settings.value(
            "appearance/theme",
            "light",
            type=str,
        )

        self.set_theme(theme)

        last_page = self.settings.value(
            "window/last_page",
            self.HOME,
            type=int,
        )

        if not 0 <= last_page < self.stack.count():
            last_page = self.HOME

        self.navigate_to(last_page)

    # ========================================================
    # APPLICATION LIFECYCLE
    # ========================================================

    def closeEvent(self, event):
        self.settings.setValue(
            "window/last_page",
            self.current_page,
        )

        self.settings.setValue(
            "appearance/theme",
            self.current_theme,
        )

        self.settings.sync()

        super().closeEvent(event)


if __name__ == "__main__":
    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
