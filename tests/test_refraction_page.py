import pytest

from PySide6.QtCore import Qt

from ui.pages.refraction_page import RefractionPage


@pytest.fixture
def refraction_page(qtbot):
    page = RefractionPage()
    qtbot.addWidget(page)
    return page


def test_refraction_page_initialization(refraction_page):
    assert refraction_page.n1_input.value() == 1.0
    assert refraction_page.n2_input.value() == 1.5
    assert refraction_page.angle_input.value() == 30.0

    assert refraction_page.refraction_result.text() == (
        "Refracted Angle: 19.47°"
    )


def test_refraction_calculation(refraction_page, qtbot):
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
    refraction_page.n1_input.setValue(1.5)
    refraction_page.n2_input.setValue(1.0)
    refraction_page.angle_input.setValue(30.0)

    refraction_page.calculate()

    assert refraction_page.critical_result.text() == (
        "Critical Angle: 41.81°"
    )


def test_no_critical_angle(refraction_page):
    refraction_page.n1_input.setValue(1.0)
    refraction_page.n2_input.setValue(1.5)

    refraction_page.calculate()

    assert refraction_page.critical_result.text() == (
        "Critical Angle: Not applicable"
    )


def test_refraction_diagram_exists(refraction_page):
    assert refraction_page.ray_diagram is not None
    assert refraction_page.ray_diagram.canvas is not None