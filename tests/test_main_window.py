
"""
Optik — Main Window Tests
Version: 0.2.0

Tests:
    - Main window initialization
    - Window title and dimensions
    - Sidebar initialization
    - Page stack initialization
    - Five registered pages
    - Default home page
    - Navigation between all pages
    - Thin Lens navigation
    - Invalid navigation handling
    - Window visibility
    - Window closing
"""

import pytest

from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
)

from app.main_window import MainWindow


# ============================================================
# FIXTURES
# ============================================================

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

    assert isinstance(main_window, QMainWindow)


def test_window_title(main_window):
    """Verify that the application has a window title."""

    assert main_window.windowTitle() == (
        "Optik — Optics & Photonics"
    )


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

    assert isinstance(
        main_window.stack,
        QStackedWidget,
    )


def test_page_count(main_window):
    """Verify that all five pages are registered."""

    assert main_window.stack.count() == 5


def test_registered_pages(main_window):
    """Verify all expected page names are registered."""

    expected_pages = {
        "home",
        "reflection",
        "refraction",
        "lens",
        "settings",
    }

    assert set(main_window.pages.keys()) == expected_pages


def test_default_page(main_window):
    """Verify that the Home page is selected initially."""

    assert (
        main_window.stack.currentWidget()
        is main_window.home_page
    )


# ============================================================
# PAGE NAVIGATION TESTS
# ============================================================

@pytest.mark.parametrize(
    "page_name, expected_index",
    [
        ("home", 0),
        ("reflection", 1),
        ("refraction", 2),
        ("lens", 3),
        ("settings", 4),
    ],
)
def test_page_navigation(
    main_window,
    page_name,
    expected_index,
):
    """Verify navigation between application pages."""

    main_window.change_page(page_name)

    assert (
        main_window.stack.currentIndex()
        == expected_index
    )

    assert (
        main_window.stack.currentWidget()
        is main_window.pages[page_name]
    )


def test_navigation_between_pages(main_window):
    """Verify that multiple navigation changes work."""

    pages = [
        "reflection",
        "refraction",
        "lens",
        "settings",
        "home",
    ]

    for page_name in pages:
        main_window.change_page(page_name)

        assert (
            main_window.stack.currentWidget()
            is main_window.pages[page_name]
        )


def test_thin_lens_navigation(main_window):
    """Verify navigation to the Thin Lens calculator."""

    main_window.change_page("lens")

    assert (
        main_window.stack.currentWidget()
        is main_window.lens_page
    )

    assert main_window.stack.currentIndex() == 3


def test_home_lens_card_navigation(main_window, qtbot):
    """Verify that the Home card opens Thin Lens."""

    main_window.show()

    qtbot.mouseClick(
        main_window.home_page.lens_card.open_button,
        __import__(
            "PySide6.QtCore",
            fromlist=["Qt"],
        ).Qt.MouseButton.LeftButton,
    )

    assert (
        main_window.stack.currentWidget()
        is main_window.lens_page
    )


def test_invalid_navigation(main_window):
    """Verify invalid page names raise an error."""

    initial_page = main_window.stack.currentWidget()

    with pytest.raises(ValueError):
        main_window.change_page("invalid_page")

    assert main_window.stack.currentWidget() is initial_page


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
