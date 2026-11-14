
"""
Optik - Main Application Window
Version: 0.4.0

Pages:
    0 - Home
    1 - Reflection
    2 - Refraction
    3 - Thin Lenses
    4 - Mirror Optics
    5 - Prism Optics & Dispersion
    6 - Settings
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt, QSettings, Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QFrame,
)

from ui.pages.home_page import HomePage
from ui.pages.reflection_page import ReflectionPage
from ui.pages.refraction_page import RefractionPage
from ui.pages.lens_page import LensPage
from ui.pages.mirror_page import MirrorPage
from ui.pages.prisms_page import PrismPage
from ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    """Main application window for Optik."""

    page_changed = Signal(int)
    theme_changed = Signal(str)

    HOME = 0
    REFLECTION = 1
    REFRACTION = 2
    LENS = 3
    MIRROR = 4
    PRISM = 5
    SETTINGS = 6

    PAGE_NAMES = (
        "Home",
        "Reflection",
        "Refraction",
        "Thin Lenses",
        "Mirror Optics",
        "Prism Optics & Dispersion",
        "Settings",
    )

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings("Optik", "Optik")

        self.current_theme = "light"
        self.current_page = self.HOME

        self.nav_buttons = {}
        self.shortcut_actions = []

        self._setup_window()
        self._setup_ui()
        self._setup_shortcuts()
        self._connect_signals()
        self._restore_settings()

    # ========================================================
    # WINDOW SETUP
    # ========================================================

    def _setup_window(self):
        self.setWindowTitle(
            "Optik v0.4.0 - Optics & Photonics"
        )
        self.setMinimumSize(900, 650)
        self.resize(1250, 850)

    def _setup_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(
            self.central_widget
        )
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._create_sidebar()
        self._create_pages()

    # ========================================================
    # SIDEBAR NAVIGATION
    # ========================================================

    def _create_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(220)

        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(8)

        self.logo_label = QLabel("OPTIK")
        self.logo_label.setObjectName("sidebarLogo")
        self.logo_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        logo_font = self.logo_label.font()
        logo_font.setPointSize(20)
        logo_font.setBold(True)
        self.logo_label.setFont(logo_font)

        self.version_label = QLabel("Version 0.4.0")
        self.version_label.setObjectName("versionLabel")
        self.version_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.logo_label)
        layout.addWidget(self.version_label)
        layout.addSpacing(25)

        navigation = [
            (self.HOME, "Home"),
            (self.REFLECTION, "Reflection"),
            (self.REFRACTION, "Refraction"),
            (self.LENS, "Thin Lenses"),
            (self.MIRROR, "Mirror Optics"),
            (self.PRISM, "Prism Optics"),
        ]

        for index, name in navigation:
            self._add_nav_button(layout, index, name)

        layout.addStretch()

        self._add_nav_button(
            layout,
            self.SETTINGS,
            "Settings",
        )

        self.main_layout.addWidget(self.sidebar)

    def _add_nav_button(self, layout, index, text):
        button = QPushButton(text)
        button.setObjectName(f"navButton{index}")
        button.setCheckable(True)
        button.setMinimumHeight(42)
        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.clicked.connect(
            lambda checked=False, page=index:
            self.navigate_to(page)
        )

        self.nav_buttons[index] = button
        layout.addWidget(button)

    # ========================================================
    # APPLICATION PAGES
    # ========================================================

    def _create_pages(self):
        self.stack = QStackedWidget()
        self.stacked_widget = self.stack

        self.home_page = HomePage()
        self.reflection_page = ReflectionPage()
        self.refraction_page = RefractionPage()
        self.lens_page = LensPage()
        self.mirror_page = MirrorPage()

        self.prism_page = PrismPage(
            dark_mode=self.current_theme == "dark"
        )

        self.settings_page = SettingsPage()

        self.pages = (
            self.home_page,
            self.reflection_page,
            self.refraction_page,
            self.lens_page,
            self.mirror_page,
            self.prism_page,
            self.settings_page,
        )

        for page in self.pages:
            self.stack.addWidget(page)

        self.main_layout.addWidget(self.stack, 1)

    # ========================================================
    # NAVIGATION
    # ========================================================

    def navigate_to(self, index: int):
        """Navigate to an application page."""

        if not isinstance(index, int):
            raise ValueError(
                "Page index must be an integer."
            )

        if not 0 <= index < self.stack.count():
            raise ValueError(
                f"Invalid page index: {index}"
            )

        self.stack.setCurrentIndex(index)
        self.current_page = index

        for page_index, button in self.nav_buttons.items():
            button.setChecked(page_index == index)

        self.settings.setValue(
            "window/last_page",
            index,
        )
        self.settings.setValue(
            "window/last_page_name",
            self.PAGE_NAMES[index],
        )

        self.page_changed.emit(index)

    # ========================================================
    # SIGNAL CONNECTIONS
    # ========================================================

    def _connect_signals(self):
        """Connect dashboard and settings signals."""

        self.home_page.navigate_to.connect(
            self.navigate_to
        )

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

            if (
                signal is not None
                and hasattr(signal, "connect")
            ):
                signal.connect(self.set_theme)

    # ========================================================
    # THEME MANAGEMENT
    # ========================================================

    def set_theme(self, theme: str):
        """Apply a light or dark theme."""

        normalized = str(theme).lower().strip()

        if normalized not in ("light", "dark"):
            normalized = "light"

        self.current_theme = normalized

        self._apply_window_theme()

        for page in self.pages:
            if page is self.prism_page:
                page.set_dark_mode(
                    normalized == "dark"
                )
            elif hasattr(page, "set_theme"):
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
            sidebar_bg = "#172033"
            foreground = "#f9fafb"
            muted = "#9ca3af"
            button_bg = "#253249"
            hover_bg = "#344563"
            selected_bg = "#2563eb"
            border = "#374151"
        else:
            background = "#f8fafc"
            sidebar_bg = "#e9eef5"
            foreground = "#172033"
            muted = "#64748b"
            button_bg = "#ffffff"
            hover_bg = "#dbeafe"
            selected_bg = "#2563eb"
            border = "#cbd5e1"

        self.central_widget.setStyleSheet(
            f"""
            QWidget {{
                background-color: {background};
                color: {foreground};
            }}

            QFrame#sidebar {{
                background-color: {sidebar_bg};
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
                background-color: {button_bg};
                color: {foreground};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 10px;
                text-align: left;
            }}

            QPushButton[checkable="true"]:hover {{
                background-color: {hover_bg};
            }}

            QPushButton[checkable="true"]:checked {{
                background-color: {selected_bg};
                color: white;
                border-color: {selected_bg};
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
            ("Ctrl+6", self.PRISM),
            ("Ctrl+7", self.SETTINGS),
        ]

        for key_sequence, page_index in shortcuts:
            action = QAction(self)
            action.setShortcut(
                QKeySequence(key_sequence)
            )

            action.triggered.connect(
                lambda checked=False, index=page_index:
                self.navigate_to(index)
            )

            self.addAction(action)
            self.shortcut_actions.append(action)

    # ========================================================
    # PERSISTENT SETTINGS
    # ========================================================

    def _restore_settings(self):
        theme = self.settings.value(
            "appearance/theme",
            "light",
            type=str,
        )

        self.set_theme(theme)

        saved_page_name = self.settings.value(
            "window/last_page_name",
            "",
            type=str,
        )

        if saved_page_name in self.PAGE_NAMES:
            last_page = self.PAGE_NAMES.index(
                saved_page_name
            )
        else:
            last_page = self.settings.value(
                "window/last_page",
                self.HOME,
                type=int,
            )

            # v0.3.0 stored Settings at index 5.
            if last_page == 5:
                last_page = self.SETTINGS

        if not 0 <= last_page < self.stack.count():
            last_page = self.HOME

        self.navigate_to(last_page)

    # ========================================================
    # APPLICATION CLOSE EVENT
    # ========================================================

    def closeEvent(self, event):
        self.settings.setValue(
            "window/last_page",
            self.current_page,
        )
        self.settings.setValue(
            "window/last_page_name",
            self.PAGE_NAMES[self.current_page],
        )
        self.settings.setValue(
            "appearance/theme",
            self.current_theme,
        )

        self.settings.sync()
        super().closeEvent(event)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
