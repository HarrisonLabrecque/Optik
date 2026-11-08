
"""
Optik - Mirror Page GUI Unit Tests
Version: 0.3.0

Tests:
    ui/pages/mirror_page.py

Requirements:
    pytest
    pytest-qt
    PySide6
    matplotlib

Run:
    python -m pytest tests/test_mirror_page.py -v
"""

import os

# Must be configured before QApplication is created.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from PySide6.QtCore import Qt, QSettings
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QPushButton,
    QScrollArea,
    QGroupBox,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from ui.pages.mirror_page import MirrorPage


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def isolated_settings(tmp_path, monkeypatch):
    """Redirect application settings to a temporary directory."""
    monkeypatch.setattr(
        QSettings,
        "defaultFormat",
        lambda: QSettings.IniFormat,
        raising=False,
    )

    QSettings.setDefaultFormat(QSettings.IniFormat)
    QSettings.setPath(
        QSettings.IniFormat,
        QSettings.UserScope,
        str(tmp_path),
    )

    settings = QSettings("Optik", "Optik")
    settings.clear()
    settings.sync()

    yield settings

    settings.clear()
    settings.sync()


@pytest.fixture
def mirror_page(qtbot, isolated_settings):
    """Create an isolated MirrorPage instance."""
    page = MirrorPage()
    qtbot.addWidget(page)
    page.show()

    yield page

    page.close()


# ============================================================
# INITIALIZATION TESTS
# ============================================================

class TestMirrorPageInitialization:

    def test_page_creation(self, mirror_page):
        assert isinstance(mirror_page, MirrorPage)

    def test_title(self, mirror_page):
        assert mirror_page.title_label.text() == "Mirror Optics"

    def test_description(self, mirror_page):
        assert "concave" in mirror_page.description_label.text().lower()
        assert "convex" in mirror_page.description_label.text().lower()

    def test_scroll_area(self, mirror_page):
        assert isinstance(mirror_page.scroll_area, QScrollArea)

    def test_input_group(self, mirror_page):
        assert isinstance(mirror_page.input_group, QGroupBox)

    def test_results_group(self, mirror_page):
        assert isinstance(mirror_page.results_group, QGroupBox)

    def test_diagram_group(self, mirror_page):
        assert isinstance(mirror_page.diagram_group, QGroupBox)

    def test_default_theme(self, mirror_page):
        assert mirror_page.current_theme == "light"


# ============================================================
# INPUT CONTROL TESTS
# ============================================================

class TestMirrorPageInputs:

    def test_mirror_selector(self, mirror_page):
        assert isinstance(mirror_page.mirror_type_combo, QComboBox)
        assert mirror_page.mirror_type_combo.count() == 2

    def test_mirror_options(self, mirror_page):
        assert mirror_page.mirror_type_combo.itemText(0) == (
            "Concave Mirror"
        )
        assert mirror_page.mirror_type_combo.itemText(1) == (
            "Convex Mirror"
        )

    @pytest.mark.parametrize(
        "attribute",
        [
            "focal_length_input",
            "object_distance_input",
            "object_height_input",
        ],
    )
    def test_spinboxes_exist(self, mirror_page, attribute):
        widget = getattr(mirror_page, attribute)
        assert isinstance(widget, QDoubleSpinBox)

    def test_default_focal_length(self, mirror_page):
        assert mirror_page.focal_length_input.value() == 10.0

    def test_default_object_distance(self, mirror_page):
        assert mirror_page.object_distance_input.value() == 30.0

    def test_default_object_height(self, mirror_page):
        assert mirror_page.object_height_input.value() == 5.0

    def test_calculate_button(self, mirror_page):
        assert isinstance(
            mirror_page.calculate_button,
            QPushButton,
        )

    def test_reset_button(self, mirror_page):
        assert isinstance(
            mirror_page.reset_button,
            QPushButton,
        )


# ============================================================
# CONCAVE MIRROR CALCULATION TESTS
# ============================================================

class TestConcaveMirrorCalculations:

    def test_concave_mirror_type(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.calculate()

        assert mirror_page.mirror_type_result.text() == "Concave"

    def test_concave_image_distance(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.calculate()

        assert mirror_page.image_distance_result.text() == "15.00"

    def test_concave_radius(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.calculate()

        assert mirror_page.radius_result.text() == "20.00"

    def test_concave_magnification(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.calculate()

        assert mirror_page.magnification_result.text() == "-0.500"

    def test_concave_image_height(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.calculate()

        assert mirror_page.image_height_result.text() == "-2.50"

    def test_concave_image_type(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.calculate()

        assert mirror_page.image_type_result.text() == "Real"

    def test_concave_orientation(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.calculate()

        assert mirror_page.orientation_result.text() == "Inverted"

    def test_concave_image_size(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.calculate()

        assert mirror_page.image_size_result.text() == "Reduced"

    def test_concave_virtual_image(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.object_distance_input.setValue(5.0)
        mirror_page.calculate()

        assert mirror_page.image_distance_result.text() == "-10.00"
        assert mirror_page.image_type_result.text() == "Virtual"
        assert mirror_page.orientation_result.text() == "Upright"
        assert mirror_page.image_size_result.text() == "Enlarged"


# ============================================================
# CONVEX MIRROR CALCULATION TESTS
# ============================================================

class TestConvexMirrorCalculations:

    def test_convex_mirror_type(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert mirror_page.mirror_type_result.text() == "Convex"

    def test_convex_image_distance(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert mirror_page.image_distance_result.text() == "-7.50"

    def test_convex_radius(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert mirror_page.radius_result.text() == "-20.00"

    def test_convex_magnification(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert mirror_page.magnification_result.text() == "0.250"

    def test_convex_image_height(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert mirror_page.image_height_result.text() == "1.25"

    def test_convex_image_type(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert mirror_page.image_type_result.text() == "Virtual"

    def test_convex_orientation(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert mirror_page.orientation_result.text() == "Upright"

    def test_convex_image_size(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert mirror_page.image_size_result.text() == "Reduced"


# ============================================================
# SPECIAL CASE TESTS
# ============================================================

class TestMirrorSpecialCases:

    def test_object_at_focal_point(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.object_distance_input.setValue(10.0)
        mirror_page.calculate()

        assert mirror_page.image_distance_result.text() == "Infinity"
        assert mirror_page.magnification_result.text() == "Undefined"
        assert mirror_page.image_height_result.text() == "Undefined"
        assert mirror_page.image_type_result.text() == "At Infinity"
        assert mirror_page.orientation_result.text() == "Not Applicable"
        assert mirror_page.image_size_result.text() == "Not Applicable"

    def test_same_size_image(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(0)
        mirror_page.object_distance_input.setValue(20.0)
        mirror_page.calculate()

        assert mirror_page.magnification_result.text() == "-1.000"
        assert mirror_page.image_size_result.text() == "Same Size"

    def test_custom_object_height(self, mirror_page):
        mirror_page.object_height_input.setValue(8.0)
        mirror_page.calculate()

        assert mirror_page.image_height_result.text() == "-4.00"


# ============================================================
# DIAGRAM TESTS
# ============================================================

class TestMirrorPageDiagram:

    def test_canvas_exists(self, mirror_page):
        assert isinstance(
            mirror_page.canvas,
            FigureCanvasQTAgg,
        )

    def test_toolbar_exists(self, mirror_page):
        assert isinstance(
            mirror_page.toolbar,
            NavigationToolbar2QT,
        )

    def test_diagram_figure(self, mirror_page):
        assert mirror_page.canvas.figure is mirror_page.diagram.figure

    def test_diagram_updates(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        assert "Convex" in mirror_page.diagram.ax.get_title()

    def test_diagram_parameters(self, mirror_page):
        mirror_page.focal_length_input.setValue(15.0)
        mirror_page.object_distance_input.setValue(45.0)
        mirror_page.object_height_input.setValue(6.0)
        mirror_page.calculate()

        assert mirror_page.diagram._last_parameters == (
            15.0,
            45.0,
            6.0,
        )


# ============================================================
# BUTTON TESTS
# ============================================================

class TestMirrorPageButtons:

    def test_calculate_button_click(self, mirror_page, qtbot):
        mirror_page.object_distance_input.setValue(20.0)

        qtbot.mouseClick(
            mirror_page.calculate_button,
            Qt.LeftButton,
        )

        assert mirror_page.image_distance_result.text() == "20.00"

    def test_reset_button_click(self, mirror_page, qtbot):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.focal_length_input.setValue(25.0)
        mirror_page.object_distance_input.setValue(50.0)

        qtbot.mouseClick(
            mirror_page.reset_button,
            Qt.LeftButton,
        )

        assert mirror_page.mirror_type_combo.currentIndex() == 0
        assert mirror_page.focal_length_input.value() == 10.0
        assert mirror_page.object_distance_input.value() == 30.0
        assert mirror_page.object_height_input.value() == 5.0

    def test_reset_updates_results(self, mirror_page):
        mirror_page.mirror_type_combo.setCurrentIndex(1)
        mirror_page.calculate()

        mirror_page.reset_inputs()

        assert mirror_page.mirror_type_result.text() == "Concave"
        assert mirror_page.image_distance_result.text() == "15.00"


# ============================================================
# SETTINGS TESTS
# ============================================================

class TestMirrorPageSettings:

    def test_settings_saved(self, mirror_page):
        mirror_page.focal_length_input.setValue(15.0)
        mirror_page.object_distance_input.setValue(40.0)
        mirror_page.calculate()

        settings = QSettings("Optik", "Optik")

        assert settings.value(
            "mirror/focal_length", type=float
        ) == 15.0

        assert settings.value(
            "mirror/object_distance", type=float
        ) == 40.0

    def test_settings_loaded(self, qtbot, isolated_settings):
        settings = QSettings("Optik", "Optik")
        settings.setValue("mirror/type", 1)
        settings.setValue("mirror/focal_length", 20.0)
        settings.setValue("mirror/object_distance", 50.0)
        settings.setValue("mirror/object_height", 8.0)
        settings.sync()

        page = MirrorPage()
        qtbot.addWidget(page)

        assert page.mirror_type_combo.currentIndex() == 1
        assert page.focal_length_input.value() == 20.0
        assert page.object_distance_input.value() == 50.0
        assert page.object_height_input.value() == 8.0


# ============================================================
# THEME TESTS
# ============================================================

class TestMirrorPageThemes:

    def test_light_theme(self, mirror_page):
        mirror_page.set_theme("light")

        assert mirror_page.current_theme == "light"
        assert mirror_page.diagram.figure.get_facecolor() == (
            1.0, 1.0, 1.0, 1.0
        )

    def test_dark_theme(self, mirror_page):
        mirror_page.set_theme("dark")

        assert mirror_page.current_theme == "dark"

        background = mirror_page.diagram.figure.get_facecolor()

        assert background != (1.0, 1.0, 1.0, 1.0)

    def test_invalid_theme_falls_back_to_light(self, mirror_page):
        mirror_page.set_theme("invalid")

        assert mirror_page.current_theme == "light"
