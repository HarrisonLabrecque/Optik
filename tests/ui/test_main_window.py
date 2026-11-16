
"""
Optik — Main Window Tests
Version: 0.4.0

Tests:
    - Main window initialization
    - Default Home page
    - Sidebar navigation
    - Navigation signals
    - Keyboard shortcuts
    - Page index validation
    - Theme management
    - Persistent appearance settings
    - Home startup regardless of saved navigation
    - Application close behavior

Requirements:
    pytest
    pytest-qt
    PySide6
"""

import pytest

from PySide6.QtCore import QSettings
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QStackedWidget

from app.main_window import MainWindow


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def isolated_settings(monkeypatch, tmp_path):
    """
    Use a temporary QSettings directory so tests do not
    modify the user's actual Optik settings.
    """

    QSettings.setDefaultFormat(
        QSettings.Format.IniFormat
    )

    QSettings.setPath(
        QSettings.Format.IniFormat,
        QSettings.Scope.UserScope,
        str(tmp_path),
    )

    settings = QSettings("Optik", "Optik")
    settings.clear()
    settings.sync()

    yield settings

    settings.clear()
    settings.sync()


@pytest.fixture
def window(qtbot, isolated_settings):
    """Create an isolated MainWindow instance."""

    main_window = MainWindow()
    qtbot.addWidget(main_window)

    yield main_window

    main_window.close()


# ============================================================
# INITIALIZATION TESTS
# ============================================================

class TestMainWindowInitialization:

    def test_window_title(self, window):
        assert "Optik" in window.windowTitle()
        assert "0.4.0" in window.windowTitle()

    def test_window_minimum_size(self, window):
        assert window.minimumWidth() == 900
        assert window.minimumHeight() == 650

    def test_stacked_widget_exists(self, window):
        assert isinstance(
            window.stack,
            QStackedWidget,
        )

    def test_stacked_widget_alias(self, window):
        assert window.stacked_widget is window.stack

    def test_page_count(self, window):
        assert window.stack.count() == 7

    def test_page_names(self, window):
        assert window.PAGE_NAMES == (
            "Home",
            "Reflection",
            "Refraction",
            "Thin Lenses",
            "Mirror Optics",
            "Prism Optics & Dispersion",
            "Settings",
        )

    def test_all_pages_registered(self, window):
        assert window.stack.widget(
            MainWindow.HOME
        ) is window.home_page

        assert window.stack.widget(
            MainWindow.REFLECTION
        ) is window.reflection_page

        assert window.stack.widget(
            MainWindow.REFRACTION
        ) is window.refraction_page

        assert window.stack.widget(
            MainWindow.LENS
        ) is window.lens_page

        assert window.stack.widget(
            MainWindow.MIRROR
        ) is window.mirror_page

        assert window.stack.widget(
            MainWindow.PRISM
        ) is window.prism_page

        assert window.stack.widget(
            MainWindow.SETTINGS
        ) is window.settings_page

    def test_home_is_default_page(self, window):
        assert window.stack.currentIndex() == (
            MainWindow.HOME
        )

        assert window.current_page == (
            MainWindow.HOME
        )

    def test_home_navigation_button_checked(self, window):
        assert window.nav_buttons[
            MainWindow.HOME
        ].isChecked()


# ============================================================
# NAVIGATION TESTS
# ============================================================

class TestMainWindowNavigation:

    @pytest.mark.parametrize(
        "page_index",
        [
            MainWindow.HOME,
            MainWindow.REFLECTION,
            MainWindow.REFRACTION,
            MainWindow.LENS,
            MainWindow.MIRROR,
            MainWindow.PRISM,
            MainWindow.SETTINGS,
        ],
    )
    def test_navigate_to_each_page(
        self,
        window,
        page_index,
    ):
        window.navigate_to(page_index)

        assert window.stack.currentIndex() == (
            page_index
        )

        assert window.current_page == page_index

    def test_navigation_updates_checked_button(
        self,
        window,
    ):
        window.navigate_to(MainWindow.PRISM)

        for index, button in window.nav_buttons.items():
            assert button.isChecked() == (
                index == MainWindow.PRISM
            )

    def test_navigation_emits_page_changed(
        self,
        window,
        qtbot,
    ):
        with qtbot.waitSignal(
            window.page_changed,
            timeout=1000,
        ) as blocker:
            window.navigate_to(MainWindow.PRISM)

        assert blocker.args == [
            MainWindow.PRISM
        ]

    def test_navigation_does_not_save_last_page(
        self,
        window,
        isolated_settings,
    ):
        """
        Navigation is session-only in v0.4.0.
        """

        window.navigate_to(MainWindow.PRISM)

        assert window.current_page == (
            MainWindow.PRISM
        )

        assert not isolated_settings.contains(
            "window/last_page"
        )

        assert not isolated_settings.contains(
            "window/last_page_name"
        )

    def test_sidebar_button_navigation(
        self,
        window,
        qtbot,
    ):
        window.show()

        button = window.nav_buttons[
            MainWindow.PRISM
        ]

        qtbot.mouseClick(
            button,
            __import__(
                "PySide6.QtCore",
                fromlist=["Qt"],
            ).Qt.MouseButton.LeftButton,
        )

        assert window.current_page == (
            MainWindow.PRISM
        )

    @pytest.mark.parametrize(
        "invalid_index",
        [-1, 7, 100, "5", None, True, 2.5],
    )
    def test_invalid_navigation_index(
        self,
        window,
        invalid_index,
    ):
        with pytest.raises(ValueError):
            window.navigate_to(invalid_index)

    def test_navigation_to_same_page(
        self,
        window,
    ):
        window.navigate_to(MainWindow.HOME)

        assert window.current_page == (
            MainWindow.HOME
        )

        assert window.stack.currentIndex() == (
            MainWindow.HOME
        )


# ============================================================
# KEYBOARD SHORTCUT TESTS
# ============================================================

class TestMainWindowShortcuts:

    @pytest.mark.parametrize(
        "shortcut,page_index",
        [
            ("Ctrl+1", MainWindow.HOME),
            ("Ctrl+2", MainWindow.REFLECTION),
            ("Ctrl+3", MainWindow.REFRACTION),
            ("Ctrl+4", MainWindow.LENS),
            ("Ctrl+5", MainWindow.MIRROR),
            ("Ctrl+6", MainWindow.PRISM),
            ("Ctrl+7", MainWindow.SETTINGS),
        ],
    )
    def test_shortcut_registration(
        self,
        window,
        shortcut,
        page_index,
    ):
        matching_actions = [
            action
            for action in window.shortcut_actions
            if action.shortcut() == QKeySequence(
                shortcut
            )
        ]

        assert len(matching_actions) == 1

        window.navigate_to(MainWindow.HOME)

        matching_actions[0].trigger()

        assert window.current_page == page_index


# ============================================================
# PERSISTENCE TESTS
# ============================================================

class TestMainWindowPersistence:

    def test_default_theme_is_light(
        self,
        window,
    ):
        assert window.current_theme == "light"

    def test_restore_prism_page_opens_home(
        self,
        qtbot,
        isolated_settings,
    ):
        """
        Saved Prism navigation must not override Home.
        """

        isolated_settings.setValue(
            "window/last_page",
            MainWindow.PRISM,
        )

        isolated_settings.setValue(
            "window/last_page_name",
            "Prism Optics & Dispersion",
        )

        isolated_settings.sync()

        restored_window = MainWindow()
        qtbot.addWidget(restored_window)

        assert restored_window.current_page == (
            MainWindow.HOME
        )

        assert restored_window.stack.currentIndex() == (
            MainWindow.HOME
        )

        restored_window.close()

    def test_restore_settings_page_opens_home(
        self,
        qtbot,
        isolated_settings,
    ):
        isolated_settings.setValue(
            "window/last_page",
            MainWindow.SETTINGS,
        )

        isolated_settings.setValue(
            "window/last_page_name",
            "Settings",
        )

        isolated_settings.sync()

        restored_window = MainWindow()
        qtbot.addWidget(restored_window)

        assert restored_window.current_page == (
            MainWindow.HOME
        )

        restored_window.close()

    def test_legacy_settings_index_ignored(
        self,
        qtbot,
        isolated_settings,
    ):
        """
        Legacy v0.3.0 page index 5 is ignored
        during startup.
        """

        isolated_settings.setValue(
            "window/last_page",
            5,
        )

        isolated_settings.sync()

        restored_window = MainWindow()
        qtbot.addWidget(restored_window)

        assert restored_window.current_page == (
            MainWindow.HOME
        )

        restored_window.close()

    def test_restore_dark_theme(
        self,
        qtbot,
        isolated_settings,
    ):
        isolated_settings.setValue(
            "appearance/theme",
            "dark",
        )

        isolated_settings.sync()

        restored_window = MainWindow()
        qtbot.addWidget(restored_window)

        assert restored_window.current_theme == "dark"

        assert restored_window.current_page == (
            MainWindow.HOME
        )

        restored_window.close()

    def test_close_saves_theme(
        self,
        window,
        isolated_settings,
    ):
        window.set_theme("dark")
        window.navigate_to(MainWindow.PRISM)

        window.close()

        isolated_settings.sync()

        assert isolated_settings.value(
            "appearance/theme"
        ) == "dark"

        assert not isolated_settings.contains(
            "window/last_page"
        )

        assert not isolated_settings.contains(
            "window/last_page_name"
        )

    def test_restart_always_opens_home(
        self,
        qtbot,
        isolated_settings,
    ):
        first_window = MainWindow()
        qtbot.addWidget(first_window)

        first_window.navigate_to(
            MainWindow.PRISM
        )

        first_window.close()

        second_window = MainWindow()
        qtbot.addWidget(second_window)

        assert second_window.current_page == (
            MainWindow.HOME
        )

        assert second_window.stack.currentIndex() == (
            MainWindow.HOME
        )

        second_window.close()


# ============================================================
# THEME TESTS
# ============================================================

class TestMainWindowTheme:

    def test_set_dark_theme(
        self,
        window,
    ):
        window.set_theme("dark")

        assert window.current_theme == "dark"

    def test_set_light_theme(
        self,
        window,
    ):
        window.set_theme("dark")
        window.set_theme("light")

        assert window.current_theme == "light"

    def test_invalid_theme_defaults_to_light(
        self,
        window,
    ):
        window.set_theme("invalid")

        assert window.current_theme == "light"

    def test_theme_change_emits_signal(
        self,
        window,
        qtbot,
    ):
        with qtbot.waitSignal(
            window.theme_changed,
            timeout=1000,
        ) as blocker:
            window.set_theme("dark")

        assert blocker.args == ["dark"]

    def test_theme_change_preserves_navigation(
        self,
        window,
    ):
        window.navigate_to(MainWindow.PRISM)

        window.set_theme("dark")

        assert window.current_page == (
            MainWindow.PRISM
        )

        assert window.stack.currentIndex() == (
            MainWindow.PRISM
        )


# ============================================================
# APPLICATION STATE TESTS
# ============================================================

class TestMainWindowState:

    def test_initial_page_matches_stack(
        self,
        window,
    ):
        assert window.current_page == (
            window.stack.currentIndex()
        )

    def test_navigation_keeps_state_synchronized(
        self,
        window,
    ):
        for page_index in range(
            window.stack.count()
        ):
            window.navigate_to(page_index)

            assert window.current_page == (
                window.stack.currentIndex()
            )

    def test_all_navigation_buttons_exist(
        self,
        window,
    ):
        assert len(window.nav_buttons) == 7

        for index in range(7):
            assert index in window.nav_buttons
