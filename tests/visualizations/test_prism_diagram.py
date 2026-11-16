
"""
Optik — Prism Ray Diagram Tests
Version: 0.4.0

Unit tests for visualization/prism_diagram.py.

Coverage:
    - PrismDiagram initialization
    - Prism vertex geometry
    - Vector normalization and rotation
    - Ray-line intersection
    - Prism drawing
    - Incident, internal, and emergent rays
    - PrismResult integration
    - Total internal reflection
    - Light and dark themes
    - Clearing and redrawing
    - Image export
    - Input and geometry errors

Run:
    python -m pytest tests/test_prism_diagram.py -v
"""

import math

import matplotlib

# Use a non-interactive backend for automated tests.
matplotlib.use("Agg")

import numpy as np
import pytest

from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, Polygon

from optics.prisms import (
    PrismError,
    PrismResult,
    calculate_prism_refraction,
)

from visualization.prism_diagram import PrismDiagram


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def diagram():
    """Create an isolated prism diagram."""

    figure = Figure(figsize=(8, 6))

    return PrismDiagram(
        figure=figure,
        dark_mode=False,
    )


@pytest.fixture
def dark_diagram():
    """Create a prism diagram using dark mode."""

    figure = Figure(figsize=(8, 6))

    return PrismDiagram(
        figure=figure,
        dark_mode=True,
    )


@pytest.fixture
def standard_result(diagram):
    """Draw a standard glass prism."""

    return diagram.draw(
        apex_angle=60.0,
        incident_angle=45.0,
        refractive_index=1.5,
    )


# ============================================================
# INITIALIZATION TESTS
# ============================================================

class TestPrismDiagramInitialization:

    def test_creates_matplotlib_figure(self, diagram):
        assert isinstance(diagram.figure, Figure)

    def test_creates_axes(self, diagram):
        assert diagram.ax is not None
        assert diagram.ax in diagram.figure.axes

    def test_initial_result_is_none(self, diagram):
        assert diagram.last_result is None

    def test_initial_light_mode(self, diagram):
        assert diagram.dark_mode is False

    def test_initial_dark_mode(self, dark_diagram):
        assert dark_diagram.dark_mode is True

    def test_uses_provided_figure(self):
        figure = Figure(figsize=(10, 7))

        diagram = PrismDiagram(figure=figure)

        assert diagram.figure is figure


# ============================================================
# GEOMETRY TESTS
# ============================================================

class TestPrismGeometry:

    def test_prism_has_three_vertices(self, diagram):
        vertices = diagram._create_prism_vertices(60.0)

        assert vertices.shape == (3, 2)

    def test_prism_apex_is_above_base(self, diagram):
        vertices = diagram._create_prism_vertices(60.0)

        left_base, right_base, apex = vertices

        assert apex[1] > left_base[1]
        assert apex[1] > right_base[1]

    def test_prism_base_is_horizontal(self, diagram):
        vertices = diagram._create_prism_vertices(60.0)

        assert vertices[0, 1] == pytest.approx(
            vertices[1, 1]
        )

    def test_prism_is_symmetric(self, diagram):
        vertices = diagram._create_prism_vertices(60.0)

        assert vertices[0, 0] == pytest.approx(
            -vertices[1, 0]
        )

        assert vertices[2, 0] == pytest.approx(0.0)

    def test_prism_apex_angle(self, diagram):
        apex_angle = 45.0

        vertices = diagram._create_prism_vertices(
            apex_angle
        )

        left_base, right_base, apex = vertices

        left_vector = left_base - apex
        right_vector = right_base - apex

        cosine = np.dot(
            left_vector,
            right_vector,
        ) / (
            np.linalg.norm(left_vector)
            * np.linalg.norm(right_vector)
        )

        measured_angle = math.degrees(
            math.acos(np.clip(cosine, -1.0, 1.0))
        )

        assert measured_angle == pytest.approx(
            apex_angle,
            abs=1e-10,
        )

    def test_prism_height(self, diagram):
        vertices = diagram._create_prism_vertices(
            60.0,
            height=5.0,
        )

        assert vertices[2, 1] == pytest.approx(5.0)


# ============================================================
# VECTOR TESTS
# ============================================================

class TestVectorHelpers:

    def test_normalize_vector(self, diagram):
        vector = np.array([3.0, 4.0])

        result = diagram._normalize(vector)

        assert np.linalg.norm(result) == pytest.approx(1.0)

        assert result == pytest.approx(
            np.array([0.6, 0.8])
        )

    def test_normalize_zero_vector(self, diagram):
        with pytest.raises(PrismError):
            diagram._normalize(
                np.array([0.0, 0.0])
            )

    def test_rotate_90_degrees(self, diagram):
        vector = np.array([1.0, 0.0])

        result = diagram._rotate(vector, 90.0)

        assert result == pytest.approx(
            np.array([0.0, 1.0]),
            abs=1e-12,
        )

    def test_rotate_180_degrees(self, diagram):
        vector = np.array([1.0, 0.0])

        result = diagram._rotate(vector, 180.0)

        assert result == pytest.approx(
            np.array([-1.0, 0.0]),
            abs=1e-12,
        )

    def test_rotate_zero_degrees(self, diagram):
        vector = np.array([1.0, 0.0])

        result = diagram._rotate(vector, 0.0)

        assert result == pytest.approx(vector)


# ============================================================
# RAY INTERSECTION TESTS
# ============================================================

class TestRayIntersection:

    def test_forward_intersection(self, diagram):
        origin = np.array([0.0, 0.0])
        direction = np.array([1.0, 0.0])

        point_a = np.array([2.0, -1.0])
        point_b = np.array([2.0, 1.0])

        result = diagram._ray_intersection(
            origin,
            direction,
            point_a,
            point_b,
        )

        assert result is not None

        assert result == pytest.approx(
            np.array([2.0, 0.0])
        )

    def test_no_backward_intersection(self, diagram):
        origin = np.array([0.0, 0.0])
        direction = np.array([1.0, 0.0])

        point_a = np.array([-2.0, -1.0])
        point_b = np.array([-2.0, 1.0])

        result = diagram._ray_intersection(
            origin,
            direction,
            point_a,
            point_b,
        )

        assert result is None

    def test_parallel_ray(self, diagram):
        origin = np.array([0.0, 0.0])
        direction = np.array([1.0, 0.0])

        point_a = np.array([0.0, 1.0])
        point_b = np.array([2.0, 1.0])

        result = diagram._ray_intersection(
            origin,
            direction,
            point_a,
            point_b,
        )

        assert result is None

    def test_intersection_outside_segment(self, diagram):
        origin = np.array([0.0, 0.0])
        direction = np.array([1.0, 0.0])

        point_a = np.array([2.0, 2.0])
        point_b = np.array([2.0, 3.0])

        result = diagram._ray_intersection(
            origin,
            direction,
            point_a,
            point_b,
        )

        assert result is None


# ============================================================
# DRAWING TESTS
# ============================================================

class TestPrismDrawing:

    def test_draw_returns_prism_result(self, standard_result):
        assert isinstance(standard_result, PrismResult)

    def test_draw_stores_last_result(
        self,
        diagram,
    ):
        result = diagram.draw(60.0, 45.0, 1.5)

        assert diagram.last_result is result

    def test_draw_matches_optics_calculation(self, diagram):
        result = diagram.draw(60.0, 45.0, 1.5)

        expected = calculate_prism_refraction(
            60.0,
            45.0,
            1.5,
        )

        assert result.deviation_angle == pytest.approx(
            expected.deviation_angle
        )

        assert result.emergent_angle == pytest.approx(
            expected.emergent_angle
        )

    def test_draws_prism_polygon(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)

        polygons = [
            patch
            for patch in diagram.ax.patches
            if isinstance(patch, Polygon)
        ]

        assert len(polygons) == 1

    def test_draws_three_rays(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)

        arrows = [
            patch
            for patch in diagram.ax.patches
            if isinstance(patch, FancyArrowPatch)
        ]

        assert len(arrows) == 3

    def test_ray_labels(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)

        labels = {
            patch.get_label()
            for patch in diagram.ax.patches
            if isinstance(patch, FancyArrowPatch)
        }

        assert labels == {
            "Incident Ray",
            "Internal Ray",
            "Emergent Ray",
        }

    def test_diagram_title_contains_deviation(self, diagram):
        result = diagram.draw(60.0, 45.0, 1.5)

        title = diagram.ax.get_title()

        assert "Prism Ray Diagram" in title
        assert f"{result.deviation_angle:.2f}" in title

    def test_axis_labels(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)

        assert diagram.ax.get_xlabel() == "X Position"
        assert diagram.ax.get_ylabel() == "Y Position"

    def test_equal_aspect_ratio(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)

        assert diagram.ax.get_aspect() == 1.0

    def test_redraw_does_not_duplicate_rays(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)
        diagram.draw(60.0, 50.0, 1.5)

        arrows = [
            patch
            for patch in diagram.ax.patches
            if isinstance(patch, FancyArrowPatch)
        ]

        assert len(arrows) == 3


# ============================================================
# TOTAL INTERNAL REFLECTION TESTS
# ============================================================

class TestTotalInternalReflection:

    def test_total_internal_reflection_returns_none(self, diagram):
        result = diagram.draw(
            apex_angle=70.0,
            incident_angle=20.0,
            refractive_index=1.5,
        )

        assert result is None

    def test_total_internal_reflection_title(self, diagram):
        diagram.draw(70.0, 20.0, 1.5)

        assert "Total Internal Reflection" in (
            diagram.ax.get_title()
        )

    def test_total_internal_reflection_ray(self, diagram):
        diagram.draw(70.0, 20.0, 1.5)

        labels = {
            patch.get_label()
            for patch in diagram.ax.patches
            if isinstance(patch, FancyArrowPatch)
        }

        assert "Total Internal Reflection" in labels

    def test_total_internal_reflection_clears_result(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)

        result = diagram.draw(70.0, 20.0, 1.5)

        assert result is None
        assert diagram.last_result is None


# ============================================================
# THEME TESTS
# ============================================================

class TestPrismDiagramThemes:

    def test_light_background(self, diagram):
        assert diagram.figure.get_facecolor() == pytest.approx(
            (1.0, 1.0, 1.0, 1.0)
        )

    def test_dark_background(self, dark_diagram):
        from matplotlib.colors import to_rgba

        assert dark_diagram.figure.get_facecolor() == pytest.approx(
            to_rgba("#1E1E1E")
        )

    def test_switch_to_dark_mode(self, diagram):
        diagram.set_dark_mode(True)

        assert diagram.dark_mode is True

    def test_switch_to_light_mode(self, dark_diagram):
        dark_diagram.set_dark_mode(False)

        assert dark_diagram.dark_mode is False

    def test_theme_preserves_result(self, diagram):
        result = diagram.draw(60.0, 45.0, 1.5)

        diagram.set_dark_mode(True)

        assert diagram.last_result is result


# ============================================================
# CLEAR TESTS
# ============================================================

class TestPrismDiagramClear:

    def test_clear_removes_patches(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)

        diagram.clear()

        assert len(diagram.ax.patches) == 0

    def test_clear_resets_result(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)

        diagram.clear()

        assert diagram.last_result is None

    def test_clear_allows_redraw(self, diagram):
        diagram.draw(60.0, 45.0, 1.5)
        diagram.clear()

        result = diagram.draw(60.0, 50.0, 1.5)

        assert isinstance(result, PrismResult)


# ============================================================
# EXPORT TESTS
# ============================================================

class TestPrismDiagramExport:

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
        diagram.draw(60.0, 45.0, 1.5)

        output = tmp_path / f"prism_diagram.{extension}"

        diagram.save(str(output))

        assert output.exists()
        assert output.stat().st_size > 0

    def test_save_with_custom_dpi(self, diagram, tmp_path):
        diagram.draw(60.0, 45.0, 1.5)

        output = tmp_path / "prism_high_resolution.png"

        diagram.save(str(output), dpi=300)

        assert output.exists()
        assert output.stat().st_size > 0


# ============================================================
# ERROR HANDLING TESTS
# ============================================================

class TestPrismDiagramErrors:

    def test_invalid_apex_angle(self, diagram):
        with pytest.raises(PrismError):
            diagram.draw(
                apex_angle=0.0,
                incident_angle=45.0,
                refractive_index=1.5,
            )

    def test_invalid_incident_angle(self, diagram):
        with pytest.raises(PrismError):
            diagram.draw(
                apex_angle=60.0,
                incident_angle=-10.0,
                refractive_index=1.5,
            )

    def test_invalid_refractive_index(self, diagram):
        with pytest.raises((PrismError, ValueError)):
            diagram.draw(
                apex_angle=60.0,
                incident_angle=45.0,
                refractive_index=1.0,
            )


# ============================================================
# TEST MODULE EXECUTION
# ============================================================

if __name__ == "__main__":
    raise SystemExit(
        pytest.main([__file__, "-v"])
    )
