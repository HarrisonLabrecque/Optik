"""
Optik — Reflection Page Tests
Version: 0.2.0

Tests:
    - Page initialization
    - Reflection calculations
    - Multiple incident angles
    - Ray diagram initialization
    - Calculate button
    - Saved settings integration
"""

import pytest

from PySide6.QtCore import Qt, QSettings

from ui.pages.reflection_page import ReflectionPage


@pytest.fixture
def isolated_settings(tmp_path):
    """
    Isolate QSettings from the user's saved preferences.
    """

    original_format = QSettings.defaultFormat()

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
    settings.sync()

    yield settings

    QSettings.setDefaultFormat(original_format)


@pytest.fixture
def reflection_page(qtbot, isolated_settings):
    """Create a ReflectionPage with predictable defaults."""

    page = ReflectionPage()
    qtbot.addWidget(page)

    return page


def test_reflection_page_initialization(reflection_page):
    """Verify the initial reflection angle and result."""

    assert reflection_page.incident_angle.value() == pytest.approx(45.0)

    assert reflection_page.result_label.text() == (
        "Reflected Angle: 45.00°"
    )


def test_reflection_calculation(reflection_page, qtbot):
    """Verify reflection calculation through the GUI."""

    reflection_page.incident_angle.setValue(30.0)

    qtbot.mouseClick(
        reflection_page.calculate_button,
        Qt.MouseButton.LeftButton,
    )

    assert reflection_page.result_label.text() == (
        "Reflected Angle: 30.00°"
    )


@pytest.mark.parametrize(
    "angle",
    [0.0, 15.0, 30.0, 45.0, 60.0, 90.0],
)
def test_reflection_angles(reflection_page, angle):
    """Verify reflection calculations for multiple angles."""

    reflection_page.incident_angle.setValue(angle)
    reflection_page.calculate()

    assert reflection_page.result_label.text() == (
        f"Reflected Angle: {angle:.2f}°"
    )


def test_reflection_diagram_exists(reflection_page):
    """Verify the ray diagram is initialized."""

    assert reflection_page.ray_diagram is not None
    assert reflection_page.ray_diagram.canvas is not None


def test_reflection_button_exists(reflection_page):
    """Verify the Calculate Reflection button exists."""

    assert reflection_page.calculate_button.text() == (
        "Calculate Reflection"
    )


def test_custom_settings_loaded(qtbot, isolated_settings):
    """Verify that custom saved angles load correctly."""

    isolated_settings.setValue(
        "calculations/angle",
        30.0,
    )
    isolated_settings.sync()

    page = ReflectionPage()
    qtbot.addWidget(page)

    assert page.incident_angle.value() == pytest.approx(30.0)

    assert page.result_label.text() == (
        "Reflected Angle: 30.00°"
    )


def test_zero_degree_reflection(reflection_page):
    """Verify reflection at normal incidence."""

    reflection_page.incident_angle.setValue(0.0)
    reflection_page.calculate()

    assert reflection_page.result_label.text() == (
        "Reflected Angle: 0.00°"
    )


def test_ninety_degree_reflection(reflection_page):
    """Verify reflection at grazing incidence."""

    reflection_page.incident_angle.setValue(90.0)
    reflection_page.calculate()

    assert reflection_page.result_label.text() == (
        "Reflected Angle: 90.00°"
    )