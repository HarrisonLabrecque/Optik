"""
Optik — Thin Lens Ray Diagram Tests
Version: 0.2.0

Tests:
    - LensDiagram initialization
    - Converging lens calculations
    - Diverging lens calculations
    - Real and virtual images
    - Image orientation
    - Magnification
    - Focal points
    - Diagram rendering
    - Principal rays
    - Input validation
    - Image at infinity
    - Clear functionality
    - Save functionality
"""

import math

import pytest

from matplotlib.figure import Figure

from visualization.lens_diagram import LensDiagram


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def lens_diagram():
    """
    Create a fresh LensDiagram instance.
    """

    return LensDiagram()


@pytest.fixture
def converging_diagram():
    """
    Create a converging lens diagram with a real image.
    """

    diagram = LensDiagram()

    diagram.draw(
        focal_length=10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    return diagram


@pytest.fixture
def diverging_diagram():
    """
    Create a diverging lens diagram with a virtual image.
    """

    diagram = LensDiagram()

    diagram.draw(
        focal_length=-10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    return diagram


# ============================================================
# 1. INITIALIZATION
# ============================================================

def test_lens_diagram_initialization(lens_diagram):

    assert isinstance(lens_diagram.figure, Figure)

    assert lens_diagram.ax is not None

    assert lens_diagram.focal_length is None
    assert lens_diagram.object_distance is None
    assert lens_diagram.object_height is None

    assert lens_diagram.image_distance is None
    assert lens_diagram.image_height is None
    assert lens_diagram.magnification is None


# ============================================================
# 2. CONVERGING LENS
# ============================================================

def test_converging_lens_image_distance(converging_diagram):

    assert converging_diagram.image_distance == pytest.approx(
        15.0
    )


def test_converging_lens_magnification(converging_diagram):

    assert converging_diagram.magnification == pytest.approx(
        -0.5
    )


def test_converging_lens_image_height(converging_diagram):

    assert converging_diagram.image_height == pytest.approx(
        -2.0
    )


def test_converging_lens_type(converging_diagram):

    assert converging_diagram.focal_length > 0


def test_converging_lens_real_image(converging_diagram):

    assert converging_diagram.image_distance > 0

    assert converging_diagram.image_height < 0


# ============================================================
# 3. DIVERGING LENS
# ============================================================

def test_diverging_lens_image_distance(diverging_diagram):

    assert diverging_diagram.image_distance == pytest.approx(
        -7.5
    )


def test_diverging_lens_magnification(diverging_diagram):

    assert diverging_diagram.magnification == pytest.approx(
        0.25
    )


def test_diverging_lens_image_height(diverging_diagram):

    assert diverging_diagram.image_height == pytest.approx(
        1.0
    )


def test_diverging_lens_type(diverging_diagram):

    assert diverging_diagram.focal_length < 0


def test_diverging_lens_virtual_image(diverging_diagram):

    assert diverging_diagram.image_distance < 0

    assert diverging_diagram.image_height > 0


# ============================================================
# 4. VIRTUAL IMAGE — CONVERGING LENS
# ============================================================

def test_converging_lens_virtual_image(lens_diagram):

    lens_diagram.draw(
        focal_length=10.0,
        object_distance=5.0,
        object_height=4.0,
    )

    assert lens_diagram.image_distance == pytest.approx(
        -10.0
    )

    assert lens_diagram.magnification == pytest.approx(
        2.0
    )

    assert lens_diagram.image_height == pytest.approx(
        8.0
    )


# ============================================================
# 5. SAME-SIZE IMAGE
# ============================================================

def test_same_size_image(lens_diagram):

    lens_diagram.draw(
        focal_length=10.0,
        object_distance=20.0,
        object_height=4.0,
    )

    assert lens_diagram.image_distance == pytest.approx(
        20.0
    )

    assert lens_diagram.magnification == pytest.approx(
        -1.0
    )

    assert lens_diagram.image_height == pytest.approx(
        -4.0
    )


# ============================================================
# 6. IMAGE AT INFINITY
# ============================================================

def test_image_at_infinity(lens_diagram):

    lens_diagram.draw(
        focal_length=10.0,
        object_distance=10.0,
        object_height=4.0,
    )

    assert math.isinf(
        lens_diagram.image_distance
    )

    assert math.isinf(
        lens_diagram.magnification
    )

    assert math.isinf(
        lens_diagram.image_height
    )


def test_image_at_infinity_title(lens_diagram):

    lens_diagram.draw(
        focal_length=10.0,
        object_distance=10.0,
        object_height=4.0,
    )

    title = lens_diagram.ax.get_title()

    assert "Image at Infinity" in title


# ============================================================
# 7. RENDERING
# ============================================================

def test_draw_returns_figure(lens_diagram):

    figure = lens_diagram.draw(
        focal_length=10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    assert isinstance(figure, Figure)


def test_draw_returns_same_figure(lens_diagram):

    figure = lens_diagram.draw(
        focal_length=10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    assert figure is lens_diagram.figure


def test_axes_have_labels(converging_diagram):

    assert converging_diagram.ax.get_xlabel() == (
        "Distance from Lens"
    )

    assert converging_diagram.ax.get_ylabel() == (
        "Height"
    )


def test_converging_title(converging_diagram):

    title = converging_diagram.ax.get_title()

    assert "Converging Lens" in title
    assert "Real Image" in title


def test_diverging_title(diverging_diagram):

    title = diverging_diagram.ax.get_title()

    assert "Diverging Lens" in title
    assert "Virtual Image" in title


# ============================================================
# 8. PRINCIPAL RAYS
# ============================================================

def test_principal_rays_exist(converging_diagram):

    lines = converging_diagram.ax.get_lines()

    assert len(lines) >= 5


def test_diverging_principal_rays_exist(diverging_diagram):

    lines = diverging_diagram.ax.get_lines()

    assert len(lines) >= 5


def test_virtual_ray_extensions_exist(diverging_diagram):

    dashed_lines = [
        line
        for line in diverging_diagram.ax.get_lines()
        if line.get_linestyle() == "--"
    ]

    assert len(dashed_lines) >= 2


# ============================================================
# 9. FOCAL POINTS
# ============================================================

def test_focal_points_exist(converging_diagram):

    collections = converging_diagram.ax.collections

    assert len(collections) >= 1


def test_focal_point_positions(converging_diagram):

    offsets = converging_diagram.ax.collections[0].get_offsets()

    positions = {
        tuple(point)
        for point in offsets
    }

    assert (-10.0, 0.0) in positions
    assert (10.0, 0.0) in positions


# ============================================================
# 10. INPUT VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "focal_length, object_distance, object_height",
    [
        (0.0, 30.0, 4.0),
        (10.0, 0.0, 4.0),
        (10.0, -30.0, 4.0),
        (10.0, 30.0, 0.0),
        (10.0, 30.0, -4.0),
        (math.inf, 30.0, 4.0),
        (math.nan, 30.0, 4.0),
        (10.0, math.inf, 4.0),
        (10.0, math.nan, 4.0),
        (10.0, 30.0, math.inf),
        (10.0, 30.0, math.nan),
    ],
)
def test_invalid_inputs(
    lens_diagram,
    focal_length,
    object_distance,
    object_height,
):

    with pytest.raises(ValueError):

        lens_diagram.draw(
            focal_length,
            object_distance,
            object_height,
        )


# ============================================================
# 11. CLEAR
# ============================================================

def test_clear_resets_calculations(converging_diagram):

    converging_diagram.clear()

    assert converging_diagram.focal_length is None
    assert converging_diagram.object_distance is None
    assert converging_diagram.object_height is None

    assert converging_diagram.image_distance is None
    assert converging_diagram.image_height is None
    assert converging_diagram.magnification is None


def test_clear_removes_plot_lines(converging_diagram):

    converging_diagram.clear()

    assert len(
        converging_diagram.ax.get_lines()
    ) == 0


# ============================================================
# 12. SAVE
# ============================================================

def test_save_diagram(converging_diagram, tmp_path):

    filename = tmp_path / "lens_diagram.png"

    converging_diagram.save(
        str(filename)
    )

    assert filename.exists()

    assert filename.stat().st_size > 0


# ============================================================
# 13. MULTIPLE DRAW CALLS
# ============================================================

def test_redraw_updates_calculations(lens_diagram):

    lens_diagram.draw(
        focal_length=10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    assert lens_diagram.image_distance == pytest.approx(
        15.0
    )

    lens_diagram.draw(
        focal_length=-10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    assert lens_diagram.image_distance == pytest.approx(
        -7.5
    )


def test_redraw_clears_previous_rays(lens_diagram):

    lens_diagram.draw(
        focal_length=10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    initial_line_count = len(
        lens_diagram.ax.get_lines()
    )

    lens_diagram.draw(
        focal_length=10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    new_line_count = len(
        lens_diagram.ax.get_lines()
    )

    assert new_line_count == initial_line_count