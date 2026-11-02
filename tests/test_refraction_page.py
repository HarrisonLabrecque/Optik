"""
Optik — Refraction Page Tests
Version: 0.2.0

Tests:
    - Page initialization
    - Refraction calculations
    - Total internal reflection
    - Critical angle calculations
    - Ray diagram initialization
    - Saved settings integration
"""

import pytest

from PySide6.QtCore import Qt, QSettings

from ui.pages.refraction_page import RefractionPage


@pytest.fixture
def isolated_settings(tmp_path, monkeypatch):
    """
    Use a temporary QSettings directory.

    Prevent tests from modifying the user's
    saved Optik preferences.
    """

    settings_directory = tmp_path / "settings"
    settings_directory.mkdir()

    QSettings.setDefaultFormat(QSettings.Format.IniFormat)

    QSettings.setPath(
        QSettings.Format.IniFormat,
        QSettings.Scope.UserScope,
        str(settings_directory),
    )

    settings = QSettings("Optik", "Optik")

    settings.setValue("calculations/angle", 45.0)
    settings.setValue("calculations/n1", 1.0)
    settings.setValue("calculations/n2", 1.5)
    settings.sync()

    yield settings

    # Restore QSettings defaults for subsequent tests.
    QSettings.setDefaultFormat(QSettings.Format.NativeFormat)


@pytest.fixture
def refraction_page(qtbot, isolated_settings):
    """Create a RefractionPage with predictable settings."""

    page = RefractionPage()
    qtbot.addWidget(page)

    return page


def test_refraction_page_initialization(refraction_page):
    """Verify the page loads configured defaults."""

    assert refraction_page.n1_input.value() == pytest.approx(1.0)
    assert refraction_page.n2_input.value() == pytest.approx(1.5)
    assert refraction_page.angle_input.value() == pytest.approx(45.0)

    # Snell's law: asin((1.0 / 1.5) * sin(45°))
    assert refraction_page.refraction_result.text() == (
        "Refracted Angle: 28.13°"
    )


def test_refraction_calculation(refraction_page, qtbot):
    """Verify refraction calculation through the GUI."""

    refraction_page.n1_input.setValue(1.5)
    refraction_page.n2_input.setValue(1.0)
    refraction_page.angle_input.setValue(30.0)

    qtbot.mouseClick(
        refraction_page.calculate_button,
        Qt.MouseButton.LeftButton,
    )

    assert refraction_page.refraction_result.text() == (
        "Refracted Angle: 48.59°"
    )


def test_total_internal_reflection(refraction_page):
    """Verify total internal reflection detection."""

    refraction_page.n1_input.setValue(1.5)
    refraction_page.n2_input.setValue(1.0)
    refraction_page.angle_input.setValue(50.0)

    refraction_page.calculate()

    assert refraction_page.tir_result.text() == (
        "Total Internal Reflection: Yes"
    )

    assert refraction_page.refraction_result.text() == (
        "Refracted Angle: No transmitted ray (TIR)"
    )


def test_critical_angle(refraction_page):
    """Verify critical angle calculations."""

    refraction_page.n1_input.setValue(1.5)
    refraction_page.n2_input.setValue(1.0)
    refraction_page.angle_input.setValue(30.0)

    refraction_page.calculate()

    assert refraction_page.critical_result.text() == (
        "Critical Angle: 41.81°"
    )


def test_no_critical_angle(refraction_page):
    """Verify that no critical angle exists when n1 < n2."""

    refraction_page.n1_input.setValue(1.0)
    refraction_page.n2_input.setValue(1.5)
    refraction_page.angle_input.setValue(45.0)

    refraction_page.calculate()

    assert refraction_page.critical_result.text() == (
        "Critical Angle: Not applicable"
    )


def test_refraction_diagram_exists(refraction_page):
    """Verify Matplotlib ray diagram initialization."""

    assert refraction_page.ray_diagram is not None
    assert refraction_page.ray_diagram.canvas is not None


def test_custom_settings_loaded(qtbot, isolated_settings):
    """Verify that saved defaults are loaded correctly."""

    isolated_settings.setValue("calculations/angle", 30.0)
    isolated_settings.setValue("calculations/n1", 1.5)
    isolated_settings.setValue("calculations/n2", 1.0)
    isolated_settings.sync()

    page = RefractionPage()
    qtbot.addWidget(page)

    assert page.angle_input.value() == pytest.approx(30.0)
    assert page.n1_input.value() == pytest.approx(1.5)
    assert page.n2_input.value() == pytest.approx(1.0)

    assert page.refraction_result.text() == (
        "Refracted Angle: 48.59°"
    )