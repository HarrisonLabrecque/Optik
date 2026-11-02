"""
Optik — Main Window Tests
Version: 0.1.0

Tests:
    - Main window initialization
    - Window title
    - Sidebar initialization
    - Page stack initialization
    - Default page
    - Sidebar navigation
    - Page switching
    - Invalid navigation handling
    - Window visibility
    - Window closing
"""

import pytest

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from app.main_window import MainWindow


@pytest.fixture
def main_window(qtbot):
    """Create the main window for testing."""

    window = MainWindow()
    qtbot.addWidget(window)

    return window


# ============================================================
# WINDOW INITIALIZATION
# ============================================================

def test_main_window_initialization(main_window):
    """Verify that the main window initializes correctly."""

    assert main_window is not None
    assert isinstance(main_window, QMainWindow)


def test_window_title(main_window):
    """Verify that the application has a window title."""

    assert main_window.windowTitle() != ""


def test_window_size(main_window):
    """Verify that the window has valid dimensions."""

    assert main_window.width() > 0
    assert main_window.height() > 0


# ============================================================
# SIDEBAR TESTS
# ============================================================

def test_sidebar_exists(main_window):
    """Verify that the sidebar exists."""

    assert main_window.sidebar is not None


def test_sidebar_visible(main_window, qtbot):
    """Verify that the sidebar becomes visible."""

    main_window.show()
    qtbot.waitExposed(main_window)

    assert main_window.sidebar.isVisible()


# ============================================================
# PAGE STACK TESTS
# ============================================================

def test_page_stack_exists(main_window):
    """Verify that the stacked widget exists."""

    assert main_window.stack is not None
    assert isinstance(main_window.stack, QStackedWidget)


def test_page_count(main_window):
    """Verify that all four pages are registered."""

    assert main_window.stack.count() == 4


def test_default_page(main_window):
    """Verify that the home page is selected initially."""

    assert main_window.stack.currentIndex() == 0


# ============================================================
# PAGE NAVIGATION TESTS
# ============================================================

@pytest.mark.parametrize(
    "page_name, expected_index",
    [
        ("home", 0),
        ("reflection", 1),
        ("refraction", 2),
        ("settings", 3),
    ],
)
def test_page_navigation(
    main_window,
    page_name,
    expected_index,
):
    """Verify navigation between application pages."""

    main_window.change_page(page_name)

    assert main_window.stack.currentIndex() == expected_index


def test_navigation_between_pages(main_window):
    """Verify that multiple navigation changes work."""

    main_window.change_page("reflection")
    assert main_window.stack.currentIndex() == 1

    main_window.change_page("refraction")
    assert main_window.stack.currentIndex() == 2

    main_window.change_page("settings")
    assert main_window.stack.currentIndex() == 3

    main_window.change_page("home")
    assert main_window.stack.currentIndex() == 0


def test_invalid_navigation(main_window):
    """Verify that invalid navigation does not crash the app."""

    initial_index = main_window.stack.currentIndex()

    try:
        main_window.change_page("invalid_page")
    except (KeyError, ValueError):
        pass
    else:
        assert main_window.stack.currentIndex() == initial_index


# ============================================================
# WINDOW LIFECYCLE TESTS
# ============================================================

def test_window_visibility(main_window, qtbot):
    """Verify that the main window can be displayed."""

    main_window.show()
    qtbot.waitExposed(main_window)

    assert main_window.isVisible()


def test_window_close(main_window):
    """Verify that the main window closes correctly."""

    main_window.show()

    main_window.close()

    assert not main_window.isVisible()