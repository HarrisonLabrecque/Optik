
"""
Optik - Mirror Physics Unit Tests
Version: 0.3.0

Tests for:
    optics/mirrors.py

Run:
    python -m pytest tests/test_mirrors.py -v
"""

import math

import pytest

from optics.mirrors import (
    MirrorResult,
    calculate_mirror_image_distance,
    calculate_radius_of_curvature,
    classify_mirror,
    classify_mirror_image,
    calculate_mirror_properties,
)


# ============================================================
# MIRROR CLASSIFICATION TESTS
# ============================================================

class TestMirrorClassification:

    def test_concave_mirror(self):
        assert classify_mirror(10.0) == "Concave"

    def test_convex_mirror(self):
        assert classify_mirror(-10.0) == "Convex"

    def test_zero_focal_length(self):
        with pytest.raises(ValueError):
            classify_mirror(0.0)

    @pytest.mark.parametrize(
        "value",
        [float("nan"), float("inf"), -float("inf")],
    )
    def test_nonfinite_focal_length(self, value):
        with pytest.raises(ValueError):
            classify_mirror(value)


# ============================================================
# RADIUS OF CURVATURE TESTS
# ============================================================

class TestRadiusOfCurvature:

    def test_concave_radius(self):
        assert calculate_radius_of_curvature(10.0) == 20.0

    def test_convex_radius(self):
        assert calculate_radius_of_curvature(-10.0) == -20.0

    def test_fractional_radius(self):
        assert calculate_radius_of_curvature(7.5) == 15.0

    def test_zero_focal_length(self):
        with pytest.raises(ValueError):
            calculate_radius_of_curvature(0.0)

    def test_overflow_radius(self):
        with pytest.raises(ValueError):
            calculate_radius_of_curvature(1e308)


# ============================================================
# IMAGE DISTANCE TESTS
# ============================================================

class TestMirrorImageDistance:

    @pytest.mark.parametrize(
        "focal_length, object_distance, expected",
        [
            (10.0, 30.0, 15.0),
            (10.0, 20.0, 20.0),
            (10.0, 15.0, 30.0),
            (10.0, 5.0, -10.0),
            (-10.0, 30.0, -7.5),
            (-10.0, 10.0, -5.0),
            (-20.0, 20.0, -10.0),
        ],
    )
    def test_image_distance(
        self,
        focal_length,
        object_distance,
        expected,
    ):
        result = calculate_mirror_image_distance(
            focal_length,
            object_distance,
        )

        assert result == pytest.approx(expected)

    def test_object_at_focal_point(self):
        result = calculate_mirror_image_distance(10.0, 10.0)
        assert result == math.inf

    def test_zero_focal_length(self):
        with pytest.raises(ValueError):
            calculate_mirror_image_distance(0.0, 30.0)

    @pytest.mark.parametrize(
        "distance",
        [0.0, -1.0, -10.0],
    )
    def test_invalid_object_distance(self, distance):
        with pytest.raises(ValueError):
            calculate_mirror_image_distance(10.0, distance)

    @pytest.mark.parametrize(
        "value",
        [float("nan"), float("inf"), -float("inf")],
    )
    def test_nonfinite_object_distance(self, value):
        with pytest.raises(ValueError):
            calculate_mirror_image_distance(10.0, value)

    def test_invalid_focal_length_type(self):
        with pytest.raises(ValueError):
            calculate_mirror_image_distance("invalid", 30.0)

    def test_invalid_object_distance_type(self):
        with pytest.raises(ValueError):
            calculate_mirror_image_distance(10.0, "invalid")


# ============================================================
# IMAGE CLASSIFICATION TESTS
# ============================================================

class TestMirrorImageClassification:

    def test_real_image(self):
        assert classify_mirror_image(15.0) == "Real"

    def test_virtual_image(self):
        assert classify_mirror_image(-7.5) == "Virtual"

    def test_image_at_infinity(self):
        assert classify_mirror_image(math.inf) == "At Infinity"

    def test_zero_image_distance(self):
        with pytest.raises(ValueError):
            classify_mirror_image(0.0)

    @pytest.mark.parametrize(
        "value",
        [float("nan"), -float("inf")],
    )
    def test_invalid_nonfinite_image_distance(self, value):
        with pytest.raises(ValueError):
            classify_mirror_image(value)


# ============================================================
# COMPLETE MIRROR PROPERTY TESTS
# ============================================================

class TestMirrorProperties:

    def test_returns_mirror_result(self):
        result = calculate_mirror_properties(10.0, 30.0)

        assert isinstance(result, MirrorResult)

    def test_concave_mirror_properties(self):
        result = calculate_mirror_properties(10.0, 30.0)

        assert result.focal_length == 10.0
        assert result.object_distance == 30.0
        assert result.image_distance == pytest.approx(15.0)
        assert result.radius_of_curvature == pytest.approx(20.0)
        assert result.mirror_type == "Concave"
        assert result.image_type == "Real"

    def test_convex_mirror_properties(self):
        result = calculate_mirror_properties(-10.0, 30.0)

        assert result.focal_length == -10.0
        assert result.object_distance == 30.0
        assert result.image_distance == pytest.approx(-7.5)
        assert result.radius_of_curvature == pytest.approx(-20.0)
        assert result.mirror_type == "Convex"
        assert result.image_type == "Virtual"

    def test_concave_virtual_image(self):
        result = calculate_mirror_properties(10.0, 5.0)

        assert result.image_distance == pytest.approx(-10.0)
        assert result.image_type == "Virtual"

    def test_object_at_focus(self):
        result = calculate_mirror_properties(10.0, 10.0)

        assert result.image_distance == math.inf
        assert result.image_type == "At Infinity"

    def test_result_is_immutable(self):
        result = calculate_mirror_properties(10.0, 30.0)

        with pytest.raises(AttributeError):
            result.image_distance = 50.0

    @pytest.mark.parametrize(
        "focal_length, object_distance",
        [
            (0.0, 30.0),
            (10.0, 0.0),
            (10.0, -5.0),
            (float("nan"), 30.0),
            (10.0, float("inf")),
        ],
    )
    def test_invalid_mirror_properties(
        self,
        focal_length,
        object_distance,
    ):
        with pytest.raises(ValueError):
            calculate_mirror_properties(
                focal_length,
                object_distance,
            )
