"""
Optik — Ray Diagram Tests
Version: 0.1.0

Tests:
    - Widget initialization
    - Matplotlib canvas
    - Reflection visualization
    - Refraction visualization
    - Total internal reflection
    - Ray geometry
    - Diagram updates
    - Input validation
"""

import math

import pytest

from matplotlib.text import Annotation
from PySide6.QtWidgets import QWidget

from visualization.ray_diagram import RayDiagram


@pytest.fixture
def ray_diagram(qtbot):
    """Create a ray diagram widget."""

    diagram = RayDiagram()
    qtbot.addWidget(diagram)

    return diagram


def get_ray_annotations(diagram):
    """Return directional ray annotations."""

    return [
        artist
        for artist in diagram.axes.texts
        if isinstance(artist, Annotation)
    ]


def get_ray_labels(diagram):
    """Return ray labels registered with Matplotlib."""

    return diagram.axes.get_legend_handles_labels()[1]


# ============================================================
# INITIALIZATION
# ============================================================

def test_ray_diagram_initialization(ray_diagram):
    assert isinstance(ray_diagram, QWidget)
    assert ray_diagram.figure is not None
    assert ray_diagram.canvas is not None
    assert ray_diagram.axes is not None


def test_default_diagram(ray_diagram):
    assert ray_diagram.axes.get_title() == "Law of Reflection"


# ============================================================
# REFLECTION
# ============================================================

@pytest.mark.parametrize(
    "angle",
    [0.0, 15.0, 30.0, 45.0, 60.0, 90.0],
)
def test_reflection_diagram(ray_diagram, angle):
    ray_diagram.draw_reflection(angle)

    assert ray_diagram.axes.get_title() == "Law of Reflection"

    rays = get_ray_annotations(ray_diagram)

    assert len(rays) == 2

    labels = get_ray_labels(ray_diagram)

    assert "Incident Ray" in labels
    assert "Reflected Ray" in labels


def test_reflection_geometry(ray_diagram):
    """Verify the incident and reflected ray endpoints."""

    ray_diagram.draw_reflection(45.0)

    rays = get_ray_annotations(ray_diagram)

    incident = rays[0]
    reflected = rays[1]

    expected_x = math.sin(math.radians(45.0))
    expected_y = math.cos(math.radians(45.0))

    # Incident ray ends at the interface.
    assert incident.xy == (0, 0)

    # Incident ray begins in the upper-left region.
    assert incident.xyann[0] == pytest.approx(-expected_x)
    assert incident.xyann[1] == pytest.approx(expected_y)

    # Reflected ray begins at the interface.
    assert reflected.xyann == (0, 0)

    # Reflected ray ends in the upper-right region.
    assert reflected.xy[0] == pytest.approx(expected_x)
    assert reflected.xy[1] == pytest.approx(expected_y)


# ============================================================
# REFRACTION
# ============================================================

@pytest.mark.parametrize(
    "n1, n2, angle",
    [
        (1.0, 1.5, 0.0),
        (1.0, 1.5, 30.0),
        (1.0, 1.33, 45.0),
        (1.5, 1.0, 30.0),
    ],
)
def test_refraction_diagram(ray_diagram, n1, n2, angle):
    ray_diagram.draw_refraction(n1, n2, angle)

    assert ray_diagram.axes.get_title() == (
        "Snell's Law — Refraction"
    )

    rays = get_ray_annotations(ray_diagram)

    assert len(rays) == 3

    labels = get_ray_labels(ray_diagram)

    assert "Incident Ray" in labels
    assert "Reflected Ray" in labels
    assert "Refracted Ray" in labels


def test_refraction_geometry(ray_diagram):
    """Verify that the refracted ray follows Snell's law."""

    ray_diagram.draw_refraction(1.0, 1.5, 30.0)

    rays = get_ray_annotations(ray_diagram)

    refracted = rays[2]

    expected_angle = math.asin(
        (1.0 / 1.5) * math.sin(math.radians(30.0))
    )

    assert refracted.xyann == (0, 0)

    assert refracted.xy[0] == pytest.approx(
        math.sin(expected_angle)
    )

    assert refracted.xy[1] == pytest.approx(
        -math.cos(expected_angle)
    )


# ============================================================
# TOTAL INTERNAL REFLECTION
# ============================================================

def test_total_internal_reflection_diagram(ray_diagram):
    ray_diagram.draw_refraction(1.5, 1.0, 50.0)

    rays = get_ray_annotations(ray_diagram)

    assert len(rays) == 2

    labels = [
        artist.get_text()
        for artist in ray_diagram.axes.texts
    ]

    assert "TOTAL INTERNAL REFLECTION" in labels


def test_tir_has_no_refracted_ray(ray_diagram):
    ray_diagram.draw_refraction(1.5, 1.0, 50.0)

    labels = get_ray_labels(ray_diagram)

    assert "Incident Ray" in labels
    assert "Reflected Ray" in labels
    assert "Refracted Ray" not in labels


# ============================================================
# DIAGRAM UPDATES
# ============================================================

def test_diagram_updates(ray_diagram):
    ray_diagram.draw_reflection(30.0)

    assert len(get_ray_annotations(ray_diagram)) == 2

    ray_diagram.draw_refraction(1.0, 1.5, 30.0)

    assert len(get_ray_annotations(ray_diagram)) == 3


def test_multiple_updates(ray_diagram):
    for angle in [10.0, 20.0, 30.0, 40.0, 50.0]:
        ray_diagram.draw_reflection(angle)

    assert len(get_ray_annotations(ray_diagram)) == 2


# ============================================================
# INPUT VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "angle",
    [-10.0, 100.0, math.inf, math.nan],
)
def test_invalid_reflection_angle(ray_diagram, angle):
    with pytest.raises(ValueError):
        ray_diagram.draw_reflection(angle)


def test_invalid_refraction_index(ray_diagram):
    with pytest.raises(ValueError):
        ray_diagram.draw_refraction(0.0, 1.5, 30.0)