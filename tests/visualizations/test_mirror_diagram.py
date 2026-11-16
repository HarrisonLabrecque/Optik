
"""
Optik - Mirror Diagram Unit Tests
Version: 0.3.0

Tests for:
    visualization/mirror_diagram.py

Run:
    python -m pytest tests/test_mirror_diagram.py -v
"""

import math

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from matplotlib.figure import Figure

from visualization.mirror_diagram import MirrorDiagram


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def diagram():
    """Create a fresh mirror diagram for each test."""
    instance = MirrorDiagram()

    yield instance

    plt.close(instance.figure)


# ============================================================
# INITIALIZATION TESTS
# ============================================================

class TestMirrorDiagramInitialization:

    def test_creates_diagram(self, diagram):
        assert isinstance(diagram, MirrorDiagram)

    def test_figure_exists(self, diagram):
        assert isinstance(diagram.figure, Figure)

    def test_axes_exists(self, diagram):
        assert diagram.ax is not None

    def test_axes_alias(self, diagram):
        assert diagram.axes is diagram.ax

    def test_default_parameters_are_none(self, diagram):
        assert diagram._last_parameters is None

    def test_custom_figure_size(self):
        instance = MirrorDiagram(figsize=(12, 6))

        try:
            width, height = instance.figure.get_size_inches()

            assert width == pytest.approx(12)
            assert height == pytest.approx(6)
        finally:
            plt.close(instance.figure)


# ============================================================
# CONCAVE MIRROR TESTS
# ============================================================

class TestConcaveMirrorDiagram:

    def test_draw_concave_mirror(self, diagram):
        result = diagram.draw(
            focal_length=10.0,
            object_distance=30.0,
            object_height=5.0,
        )

        assert result is diagram.figure

    def test_concave_real_image_title(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)

        assert "Concave" in diagram.ax.get_title()
        assert "Real" in diagram.ax.get_title()

    def test_concave_virtual_image_title(self, diagram):
        diagram.draw(10.0, 5.0, 5.0)

        assert "Concave" in diagram.ax.get_title()
        assert "Virtual" in diagram.ax.get_title()

    def test_concave_at_center_of_curvature(self, diagram):
        diagram.draw(10.0, 20.0, 5.0)

        assert diagram._last_parameters == (
            10.0,
            20.0,
            5.0,
        )

    def test_concave_inside_focal_length(self, diagram):
        diagram.draw(10.0, 5.0, 5.0)

        assert diagram._last_parameters == (
            10.0,
            5.0,
            5.0,
        )


# ============================================================
# CONVEX MIRROR TESTS
# ============================================================

class TestConvexMirrorDiagram:

    def test_draw_convex_mirror(self, diagram):
        result = diagram.draw(
            focal_length=-10.0,
            object_distance=30.0,
            object_height=5.0,
        )

        assert result is diagram.figure

    def test_convex_virtual_image_title(self, diagram):
        diagram.draw(-10.0, 30.0, 5.0)

        assert "Convex" in diagram.ax.get_title()
        assert "Virtual" in diagram.ax.get_title()

    def test_convex_parameters(self, diagram):
        diagram.draw(-10.0, 30.0, 5.0)

        assert diagram._last_parameters == (
            -10.0,
            30.0,
            5.0,
        )

    def test_convex_different_distances(self, diagram):
        for distance in (5.0, 10.0, 20.0, 50.0):
            diagram.draw(-10.0, distance, 5.0)

            assert diagram._last_parameters[1] == distance


# ============================================================
# IMAGE GEOMETRY TESTS
# ============================================================

class TestMirrorImageGeometry:

    @staticmethod
    def get_arrow_annotations(diagram):
        """Return arrows created using Matplotlib annotations."""
        return [
            item
            for item in diagram.ax.texts
            if hasattr(item, "xy")
            and hasattr(item, "xyann")
        ]

    def test_real_image_position(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)

        arrows = self.get_arrow_annotations(diagram)

        # Object tip: x=-30, y=+5
        # Real image tip: x=-15, y=-2.5
        assert any(
            arrow.xy[0] == pytest.approx(-30.0)
            and arrow.xy[1] == pytest.approx(5.0)
            for arrow in arrows
        )

        assert any(
            arrow.xy[0] == pytest.approx(-15.0)
            and arrow.xy[1] == pytest.approx(-2.5)
            for arrow in arrows
        )

    def test_virtual_image_position(self, diagram):
        diagram.draw(-10.0, 30.0, 5.0)

        arrows = self.get_arrow_annotations(diagram)

        # Virtual image tip: x=+7.5, y=+1.25
        assert any(
            arrow.xy[0] == pytest.approx(7.5)
            and arrow.xy[1] == pytest.approx(1.25)
            for arrow in arrows
        )

    def test_concave_virtual_image_position(self, diagram):
        diagram.draw(10.0, 5.0, 5.0)

        arrows = self.get_arrow_annotations(diagram)

        # Virtual image tip: x=+10, y=+10
        assert any(
            arrow.xy[0] == pytest.approx(10.0)
            and arrow.xy[1] == pytest.approx(10.0)
            for arrow in arrows
        )

    def test_focus_and_center_markers(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)

        labels = [
            text.get_text()
            for text in diagram.ax.texts
        ]

        assert "F" in labels
        assert "C" in labels

    def test_focus_and_center_positions(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)

        annotations = {
            item.get_text(): item.xy
            for item in diagram.ax.texts
            if hasattr(item, "xy")
            and item.get_text() in ("F", "C")
        }

        assert annotations["F"][0] == pytest.approx(-10.0)
        assert annotations["C"][0] == pytest.approx(-20.0)

    def test_convex_focus_and_center_positions(self, diagram):
        diagram.draw(-10.0, 30.0, 5.0)

        annotations = {
            item.get_text(): item.xy
            for item in diagram.ax.texts
            if hasattr(item, "xy")
            and item.get_text() in ("F", "C")
        }

        assert annotations["F"][0] == pytest.approx(10.0)
        assert annotations["C"][0] == pytest.approx(20.0)


# ============================================================
# RAY DRAWING TESTS
# ============================================================

class TestMirrorRayDrawing:

    def test_concave_rays_exist(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)

        assert len(diagram.ax.lines) >= 5

    def test_convex_rays_exist(self, diagram):
        diagram.draw(-10.0, 30.0, 5.0)

        assert len(diagram.ax.lines) >= 5

    def test_virtual_extensions_exist(self, diagram):
        diagram.draw(-10.0, 30.0, 5.0)

        dashed_lines = [
            line
            for line in diagram.ax.lines
            if line.get_linestyle() == "--"
        ]

        assert len(dashed_lines) >= 2

    def test_real_image_has_no_virtual_extensions(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)

        dashed_lines = [
            line
            for line in diagram.ax.lines
            if line.get_linestyle() == "--"
        ]

        assert len(dashed_lines) == 0

    def test_reflected_ray_colors(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)

        colors = {
            line.get_color()
            for line in diagram.ax.lines
        }

        assert "crimson" in colors
        assert "royalblue" in colors


# ============================================================
# FOCAL POINT TESTS
# ============================================================

class TestMirrorFocalPoint:

    def test_object_at_focus(self, diagram):
        diagram.draw(10.0, 10.0, 5.0)

        assert "At Infinity" in diagram.ax.get_title()

    def test_focus_does_not_draw_finite_image(self, diagram):
        diagram.draw(10.0, 10.0, 5.0)

        labels = [
            text.get_text()
            for text in diagram.ax.texts
        ]

        assert "Image" not in labels

    def test_focus_displays_infinity_message(self, diagram):
        diagram.draw(10.0, 10.0, 5.0)

        labels = [
            text.get_text()
            for text in diagram.ax.texts
        ]

        assert any(
            "infinity" in label.lower()
            for label in labels
        )


# ============================================================
# CLEAR AND REDRAW TESTS
# ============================================================

class TestMirrorClearAndRedraw:

    def test_clear_removes_lines(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)
        diagram.clear()

        assert len(diagram.ax.lines) == 0

    def test_clear_removes_title(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)
        diagram.clear()

        assert diagram.ax.get_title() == ""

    def test_clear_resets_parameters(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)
        diagram.clear()

        assert diagram._last_parameters is None

    def test_redraw_changes_mirror_type(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)
        diagram.draw(-10.0, 30.0, 5.0)

        assert "Convex" in diagram.ax.get_title()

    def test_redraw_does_not_accumulate_lines(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)
        first_count = len(diagram.ax.lines)

        diagram.draw(10.0, 30.0, 5.0)
        second_count = len(diagram.ax.lines)

        assert first_count == second_count


# ============================================================
# SAVE / EXPORT TESTS
# ============================================================

class TestMirrorDiagramExport:

    @pytest.mark.parametrize(
        "extension",
        ["png", "svg", "pdf"],
    )
    def test_save_diagram(
        self,
        diagram,
        tmp_path,
        extension,
    ):
        diagram.draw(10.0, 30.0, 5.0)

        filename = tmp_path / f"mirror_diagram.{extension}"
        diagram.save(filename)

        assert filename.exists()
        assert filename.stat().st_size > 0

    def test_save_custom_dpi(self, diagram, tmp_path):
        diagram.draw(-10.0, 30.0, 5.0)

        filename = tmp_path / "convex_mirror.png"
        diagram.save(filename, dpi=200)

        assert filename.exists()
        assert filename.stat().st_size > 0


# ============================================================
# INPUT VALIDATION TESTS
# ============================================================

class TestMirrorDiagramValidation:

    @pytest.mark.parametrize(
        "focal_length, object_distance, object_height",
        [
            (0.0, 30.0, 5.0),
            (10.0, 0.0, 5.0),
            (10.0, -5.0, 5.0),
            (10.0, 30.0, 0.0),
            (10.0, 30.0, -5.0),
            (math.nan, 30.0, 5.0),
            (math.inf, 30.0, 5.0),
            (10.0, math.nan, 5.0),
            (10.0, math.inf, 5.0),
            (10.0, 30.0, math.nan),
            (10.0, 30.0, math.inf),
        ],
    )
    def test_invalid_parameters(
        self,
        diagram,
        focal_length,
        object_distance,
        object_height,
    ):
        with pytest.raises(ValueError):
            diagram.draw(
                focal_length,
                object_distance,
                object_height,
            )

    def test_invalid_object_height_type(self, diagram):
        with pytest.raises(ValueError):
            diagram.draw(10.0, 30.0, "invalid")

    def test_invalid_focal_length_type(self, diagram):
        with pytest.raises(ValueError):
            diagram.draw("invalid", 30.0, 5.0)

    def test_invalid_object_distance_type(self, diagram):
        with pytest.raises(ValueError):
            diagram.draw(10.0, "invalid", 5.0)


# ============================================================
# FIGURE AND AXES TESTS
# ============================================================

class TestMirrorFigureProperties:

    def test_axis_labels(self, diagram):
        diagram.draw(10.0, 30.0, 5.0)

        assert "Optical axis" in diagram.ax.get_xlabel()
        assert "Height" in diagram.ax.get_ylabel()

    def test_axis_limits_are_valid(self, diagram):
        diagram.draw(-10.0, 30.0, 5.0)

        xmin, xmax = diagram.ax.get_xlim()
        ymin, ymax = diagram.ax.get_ylim()

        assert xmin < xmax
        assert ymin < ymax

    def test_figure_contains_one_axes(self, diagram):
        assert len(diagram.figure.axes) == 1
