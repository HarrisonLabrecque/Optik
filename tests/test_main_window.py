
"""
Optik - Main Window Unit and Integration Tests
Version: 0.4.0

Tests:
    - MainWindow initialization
    - Seven application pages
    - Sidebar navigation
    - HomePage navigation signals
    - PrismPage integration
    - Keyboard shortcuts
    - Light/dark theme switching
    - QSettings persistence
    - Legacy settings migration
    - Invalid navigation
    - Window closing
"""

from __future__ import annotations

import pytest

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QStackedWidget,
)

import app.main_window as main_window_module
from app.main_window import MainWindow


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def isolated_settings(tmp_path, monkeypatch):
    """
    Isolate QSettings so tests never modify real user settings.
    """

    original_qsettings = QSettings

    def create_settings(*args, **kwargs):
        settings_path = tmp_path / "optik_test.ini"

        return original_qsettings(
            str(settings_path),
            QSettings.Format.IniFormat,
        )

    monkeypatch.setattr(
        main_window_module,
        "QSettings",
        create_settings,
    )

    return create_settings()


@pytest.fixture
def window(qtbot, isolated_settings):
    """Create and register a MainWindow instance."""

    widget = MainWindow()

    qtbot.addWidget(widget)
    widget.show()

    return widget


# ============================================================
# INITIALIZATION
# ============================================================

class TestMainWindowInitialization:

    def test_window_creation(self, window):
        assert isinstance(window, QMainWindow)

    def test_window_title(self, window):
        assert "Optik v0.4.0" in window.windowTitle()

    def test_window_minimum_size(self, window):
        assert window.minimumWidth() == 900
        assert window.minimumHeight() == 650

    def test_window_default_page(self, window):
        assert window.current_page == window.HOME
        assert window.stack.currentIndex() == window.HOME

    def test_window_default_theme(self, window):
        assert window.current_theme == "light"

    def test_version_label(self, window):
        assert "0.4.0" in window.version_label.text()

    def test_sidebar_width(self, window):
        assert window.sidebar.width() == 220

    def test_sidebar_object_name(self, window):
        assert window.sidebar.objectName() == "sidebar"

    def test_stacked_widget(self, window):
        assert isinstance(
            window.stack,
            QStackedWidget,
        )

    def test_stack_alias(self, window):
        assert window.stacked_widget is window.stack


# ============================================================
# PAGE CONSTANTS AND REGISTRATION
# ============================================================

class TestMainWindowPages:

    @pytest.mark.parametrize(
        "attribute, expected",
        [
            ("HOME", 0),
            ("REFLECTION", 1),
            ("REFRACTION", 2),
            ("LENS", 3),
            ("MIRROR", 4),
            ("PRISM", 5),
            ("SETTINGS", 6),
        ],
    )
    def test_page_constants(
        self,
        attribute,
        expected,
    ):
        assert getattr(MainWindow, attribute) == expected

    def test_seven_pages_registered(self, window):
        assert window.stack.count() == 7
        assert len(window.pages) == 7

    def test_page_order(self, window):
        expected_pages = (
            window.home_page,
            window.reflection_page,
            window.refraction_page,
            window.lens_page,
            window.mirror_page,
            window.prism_page,
            window.settings_page,
        )

        assert window.pages == expected_pages

        for index, page in enumerate(expected_pages):
            assert window.stack.widget(index) is page

    def test_page_names(self, window):
        assert len(window.PAGE_NAMES) == 7

        assert window.PAGE_NAMES[window.PRISM] == (
            "Prism Optics & Dispersion"
        )

        assert window.PAGE_NAMES[window.SETTINGS] == (
            "Settings"
        )

    def test_prism_page_registered(self, window):
        assert window.prism_page is not None

        assert window.stack.indexOf(
            window.prism_page
        ) == window.PRISM


# ============================================================
# SIDEBAR
# ============================================================

class TestMainWindowSidebar:

    def test_seven_navigation_buttons(self, window):
        assert len(window.nav_buttons) == 7

    @pytest.mark.parametrize(
        "page_index",
        range(7),
    )
    def test_navigation_button_exists(
        self,
        window,
        page_index,
    ):
        button = window.nav_buttons[page_index]

        assert isinstance(button, QPushButton)
        assert button.isCheckable()

    def test_home_button_checked_by_default(
        self,
        window,
    ):
        assert window.nav_buttons[
            window.HOME
        ].isChecked()

    @pytest.mark.parametrize(
        "page_index",
        range(7),
    )
    def test_sidebar_button_navigation(
        self,
        window,
        qtbot,
        page_index,
    ):
        button = window.nav_buttons[page_index]

        qtbot.mouseClick(
            button,
            Qt.MouseButton.LeftButton,
        )

        assert window.current_page == page_index
        assert window.stack.currentIndex() == page_index

        for index, nav_button in (
            window.nav_buttons.items()
        ):
            assert nav_button.isChecked() == (
                index == page_index
            )

    def test_prism_sidebar_button(self, window):
        button = window.nav_buttons[
            window.PRISM
        ]

        assert "Prism" in button.text()


# ============================================================
# NAVIGATION
# ============================================================

class TestMainWindowNavigation:

    @pytest.mark.parametrize(
        "page_index",
        range(7),
    )
    def test_navigate_to_page(
        self,
        window,
        page_index,
    ):
        window.navigate_to(page_index)

        assert window.current_page == page_index
        assert window.stack.currentIndex() == page_index

    def test_navigation_emits_signal(
        self,
        window,
        qtbot,
    ):
        with qtbot.waitSignal(
            window.page_changed,
            timeout=1000,
        ) as signal:
            window.navigate_to(window.PRISM)

        assert signal.args == [window.PRISM]

    @pytest.mark.parametrize(
        "invalid_index",
        [-1, 7, 100],
    )
    def test_invalid_page_index(
        self,
        window,
        invalid_index,
    ):
        with pytest.raises(ValueError):
            window.navigate_to(invalid_index)

    @pytest.mark.parametrize(
        "invalid_index",
        ["1", None, 1.5],
    )
    def test_non_integer_page_index(
        self,
        window,
        invalid_index,
    ):
        with pytest.raises(ValueError):
            window.navigate_to(invalid_index)

    def test_navigation_updates_settings(
        self,
        window,
    ):
        window.navigate_to(window.PRISM)

        assert window.settings.value(
            "window/last_page",
            type=int,
        ) == window.PRISM

        assert window.settings.value(
            "window/last_page_name",
            type=str,
        ) == "Prism Optics & Dispersion"

    def test_home_page_navigation_signal(
        self,
        window,
    ):
        window.home_page.navigate_to.emit(
            window.PRISM
        )

        assert window.current_page == window.PRISM


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

class TestMainWindowShortcuts:

    def test_seven_shortcuts(self, window):
        assert len(window.shortcut_actions) == 7

    @pytest.mark.parametrize(
        "page_index",
        range(7),
    )
    def test_shortcut_mapping(
        self,
        window,
        page_index,
    ):
        action = window.shortcut_actions[
            page_index
        ]

        expected = QKeySequence(
            f"Ctrl+{page_index + 1}"
        )

        assert action.shortcut() == expected

    @pytest.mark.parametrize(
        "page_index",
        range(7),
    )
    def test_shortcut_action_navigation(
        self,
        window,
        page_index,
    ):
        action = window.shortcut_actions[
            page_index
        ]

        action.trigger()

        assert window.current_page == page_index

    def test_prism_shortcut(self, window):
        window.shortcut_actions[5].trigger()

        assert window.current_page == window.PRISM

    def test_settings_shortcut(self, window):
        window.shortcut_actions[6].trigger()

        assert window.current_page == window.SETTINGS


# ============================================================
# THEME MANAGEMENT
# ============================================================

class TestMainWindowThemes:

    def test_light_theme(self, window):
        window.set_theme("light")

        assert window.current_theme == "light"

        assert window.settings.value(
            "appearance/theme"
        ) == "light"

    def test_dark_theme(self, window):
        window.set_theme("dark")

        assert window.current_theme == "dark"

        assert window.settings.value(
            "appearance/theme"
        ) == "dark"

    def test_theme_switching(self, window):
        window.set_theme("dark")
        assert window.current_theme == "dark"

        window.set_theme("light")
        assert window.current_theme == "light"

    def test_invalid_theme_defaults_to_light(
        self,
        window,
    ):
        window.set_theme("invalid")

        assert window.current_theme == "light"

    def test_case_insensitive_theme(self, window):
        window.set_theme("DARK")

        assert window.current_theme == "dark"

    def test_theme_emits_signal(
        self,
        window,
        qtbot,
    ):
        with qtbot.waitSignal(
            window.theme_changed,
            timeout=1000,
        ) as signal:
            window.set_theme("dark")

        assert signal.args == ["dark"]

    def test_prism_receives_dark_theme(
        self,
        window,
        monkeypatch,
    ):
        received = []

        monkeypatch.setattr(
            window.prism_page,
            "set_dark_mode",
            lambda dark: received.append(dark),
        )

        window.set_theme("dark")

        assert received == [True]

    def test_prism_receives_light_theme(
        self,
        window,
        monkeypatch,
    ):
        received = []

        monkeypatch.setattr(
            window.prism_page,
            "set_dark_mode",
            lambda dark: received.append(dark),
        )

        window.set_theme("light")

        assert received == [False]

    def test_dark_stylesheet(self, window):
        window.set_theme("dark")

        assert "#111827" in (
            window.central_widget.styleSheet()
        )

    def test_light_stylesheet(self, window):
        window.set_theme("light")

        assert "#f8fafc" in (
            window.central_widget.styleSheet()
        )


# ============================================================
# PERSISTENT SETTINGS
# ============================================================

class TestMainWindowPersistence:

    def test_restore_theme(
        self,
        qtbot,
        isolated_settings,
    ):
        isolated_settings.setValue(
            "appearance/theme",
            "dark",
        )

        widget = MainWindow()
        qtbot.addWidget(widget)

        assert widget.current_theme == "dark"

    def test_restore_prism_page(
        self,
        qtbot,
        isolated_settings,
    ):
        isolated_settings.setValue(
            "window/last_page_name",
            "Prism Optics & Dispersion",
        )

        widget = MainWindow()
        qtbot.addWidget(widget)

        assert widget.current_page == widget.PRISM
        assert widget.stack.currentIndex() == 5

    def test_restore_settings_page(
        self,
        qtbot,
        isolated_settings,
    ):
        isolated_settings.setValue(
            "window/last_page_name",
            "Settings",
        )

        widget = MainWindow()
        qtbot.addWidget(widget)

        assert widget.current_page == widget.SETTINGS

    def test_migrate_legacy_settings_index(
        self,
        qtbot,
        isolated_settings,
    ):
        """
        In v0.3.0 Settings was page 5.
        In v0.4.0 Settings is page 6.
        """

        isolated_settings.remove(
            "window/last_page_name"
        )

        isolated_settings.setValue(
            "window/last_page",
            5,
        )

        widget = MainWindow()
        qtbot.addWidget(widget)

        assert widget.current_page == widget.SETTINGS

    def test_invalid_saved_page_falls_back_home(
        self,
        qtbot,
        isolated_settings,
    ):
        isolated_settings.setValue(
            "window/last_page_name",
            "Nonexistent Page",
        )

        isolated_settings.setValue(
            "window/last_page",
            999,
        )

        widget = MainWindow()
        qtbot.addWidget(widget)

        assert widget.current_page == widget.HOME

    def test_close_saves_settings(
        self,
        window,
    ):
        window.navigate_to(window.PRISM)
        window.set_theme("dark")

        window.close()

        assert window.settings.value(
            "window/last_page",
            type=int,
        ) == window.PRISM

        assert window.settings.value(
            "window/last_page_name",
            type=str,
        ) == "Prism Optics & Dispersion"

        assert window.settings.value(
            "appearance/theme",
            type=str,
        ) == "dark"


# ============================================================
# WINDOW VISIBILITY
# ============================================================

class TestMainWindowVisibility:

    def test_window_visible(self, window):
        assert window.isVisible()

    def test_sidebar_visible(self, window):
        assert window.sidebar.isVisible()

    def test_stack_visible(self, window):
        assert window.stack.isVisible()
