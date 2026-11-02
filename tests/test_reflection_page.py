import pytest

from PySide6.QtCore import Qt

from ui.pages.reflection_page import ReflectionPage


@pytest.fixture
def reflection_page(qtbot):
    page = ReflectionPage()
    qtbot.addWidget(page)
    return page


def test_reflection_page_initialization(reflection_page):
    assert reflection_page.incident_angle.value() == 45.0
    assert reflection_page.result_label.text() == (
        "Reflected Angle: 45.00°"
    )


def test_reflection_calculation(reflection_page, qtbot):
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
    [0.0, 15.0, 45.0, 60.0, 90.0],
)
def test_reflection_angles(reflection_page, angle):
    reflection_page.incident_angle.setValue(angle)
    reflection_page.calculate()

    assert reflection_page.result_label.text() == (
        f"Reflected Angle: {angle:.2f}°"
    )


def test_reflection_diagram_exists(reflection_page):
    assert reflection_page.ray_diagram is not None
    assert reflection_page.ray_diagram.canvas is not None


def test_reflection_button_exists(reflection_page):
    assert reflection_page.calculate_button.text() == (
        "Calculate Reflection"
    )