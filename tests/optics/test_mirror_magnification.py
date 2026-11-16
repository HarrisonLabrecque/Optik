
"""
Optik - Mirror Magnification Unit Tests
Version: 0.3.0

Tests for:
    optics/mirror_magnification.py

Run:
    python -m pytest tests/test_mirror_magnification.py -v
"""

from dataclasses import FrozenInstanceError
import math

import pytest

from optics.mirror_magnification import (
    MirrorMagnificationResult,
    calculate_mirror_magnification,
    calculate_mirror_image_height,
    classify_mirror_orientation,
    classify_mirror_image_size,
    calculate_mirror_magnification_properties,
)


# ============================================================
# MAGNIFICATION CALCULATION TESTS
# ============================================================

class TestMirrorMagnification:

    @pytest.mark.parametrize(
        "image_distance, object_distance, expected",
        [
            (15.0, 30.0, -0.5),
            (-7.5, 30.0, 0.25),
            (-10.0, 5.0, 2.0),
            (20.0, 20.0, -1.0),
            (30.0, 15.0, -2.0),
        ],
    )
    def test_calculate_magnification(
        self,
        image_distance,
        object_distance,
        expected,
    ):
        result = calculate_mirror_magnification(
            image_distance,
            object_distance,
        )
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize(
        "object_distance",
        [0.0, -1.0, -10.0],
    )
    def test_invalid_object_distance(self, object_distance):
        with pytest.raises(ValueError):
            calculate_mirror_magnification(
                15.0,
                object_distance,
            )

    @pytest.mark.parametrize(
        "image_distance",
        [math.nan, math.inf, -math.inf],
    )
    def test_nonfinite_image_distance(self, image_distance):
        with pytest.raises(ValueError):
            calculate_mirror_magnification(
                image_distance,
                30.0,
            )

    @pytest.mark.parametrize(
        "object_distance",
        [math.nan, math.inf, -math.inf],
    )
    def test_nonfinite_object_distance(self, object_distance):
        with pytest.raises(ValueError):
            calculate_mirror_magnification(
                15.0,
                object_distance,
            )

    def test_invalid_input_type(self):
        with pytest.raises(ValueError):
            calculate_mirror_magnification(
                "invalid",
                30.0,
            )


# ============================================================
# IMAGE HEIGHT TESTS
# ============================================================

class TestMirrorImageHeight:

    @pytest.mark.parametrize(
        "magnification, object_height, expected",
        [
            (-0.5, 5.0, -2.5),
            (0.25, 5.0, 1.25),
            (2.0, 5.0, 10.0),
            (-1.0, 4.0, -4.0),
            (1.0, 3.0, 3.0),
        ],
    )
    def test_calculate_image_height(
        self,
        magnification,
        object_height,
        expected,
    ):
        result = calculate_mirror_image_height(
            magnification,
            object_height,
        )
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize(
        "object_height",
        [0.0, -1.0, -5.0],
    )
    def test_invalid_object_height(self, object_height):
        with pytest.raises(ValueError):
            calculate_mirror_image_height(
                2.0,
                object_height,
            )

    @pytest.mark.parametrize(
        "magnification",
        [math.nan, math.inf, -math.inf],
    )
    def test_nonfinite_magnification(self, magnification):
        with pytest.raises(ValueError):
            calculate_mirror_image_height(
                magnification,
                5.0,
            )

    def test_image_height_overflow(self):
        with pytest.raises(ValueError):
            calculate_mirror_image_height(
                1e308,
                1e308,
            )


# ============================================================
# ORIENTATION CLASSIFICATION TESTS
# ============================================================

class TestMirrorOrientation:

    @pytest.mark.parametrize(
        "magnification, expected",
        [
            (2.0, "Upright"),
            (0.25, "Upright"),
            (-0.5, "Inverted"),
            (-2.0, "Inverted"),
            (0.0, "Undefined"),
        ],
    )
    def test_orientation(self, magnification, expected):
        result = classify_mirror_orientation(magnification)
        assert result == expected

    @pytest.mark.parametrize(
        "value",
        [math.nan, math.inf, -math.inf],
    )
    def test_invalid_orientation_input(self, value):
        with pytest.raises(ValueError):
            classify_mirror_orientation(value)


# ============================================================
# IMAGE SIZE CLASSIFICATION TESTS
# ============================================================

class TestMirrorImageSize:

    @pytest.mark.parametrize(
        "magnification, expected",
        [
            (2.0, "Enlarged"),
            (-3.0, "Enlarged"),
            (1.0, "Same Size"),
            (-1.0, "Same Size"),
            (0.5, "Reduced"),
            (-0.25, "Reduced"),
            (0.0, "Reduced"),
        ],
    )
    def test_image_size(self, magnification, expected):
        result = classify_mirror_image_size(magnification)
        assert result == expected

    @pytest.mark.parametrize(
        "value",
        [math.nan, math.inf, -math.inf],
    )
    def test_invalid_image_size_input(self, value):
        with pytest.raises(ValueError):
            classify_mirror_image_size(value)


# ============================================================
# COMPLETE MAGNIFICATION PROPERTIES TESTS
# ============================================================

class TestMirrorMagnificationProperties:

    def test_returns_dataclass(self):
        result = calculate_mirror_magnification_properties(
            10.0, 30.0, 5.0
        )
        assert isinstance(result, MirrorMagnificationResult)

    @pytest.mark.parametrize(
        "focal_length, object_distance, object_height, "
        "expected_distance, expected_magnification, "
        "expected_height, expected_orientation, expected_size",
        [
            (
                10.0, 30.0, 5.0,
                15.0, -0.5, -2.5,
                "Inverted", "Reduced",
            ),
            (
                -10.0, 30.0, 5.0,
                -7.5, 0.25, 1.25,
                "Upright", "Reduced",
            ),
            (
                10.0, 5.0, 5.0,
                -10.0, 2.0, 10.0,
                "Upright", "Enlarged",
            ),
            (
                10.0, 20.0, 5.0,
                20.0, -1.0, -5.0,
                "Inverted", "Same Size",
            ),
        ],
    )
    def test_complete_properties(
        self,
        focal_length,
        object_distance,
        object_height,
        expected_distance,
        expected_magnification,
        expected_height,
        expected_orientation,
        expected_size,
    ):
        result = calculate_mirror_magnification_properties(
            focal_length,
            object_distance,
            object_height,
        )

        assert result.image_distance == pytest.approx(
            expected_distance
        )
        assert result.magnification == pytest.approx(
            expected_magnification
        )
        assert result.image_height == pytest.approx(
            expected_height
        )
        assert result.orientation == expected_orientation
        assert result.image_size == expected_size

    def test_object_at_focal_point(self):
        with pytest.raises(ValueError, match="infinity"):
            calculate_mirror_magnification_properties(
                10.0, 10.0, 5.0
            )

    @pytest.mark.parametrize(
        "focal_length, object_distance, object_height",
        [
            (0.0, 30.0, 5.0),
            (10.0, 0.0, 5.0),
            (10.0, -5.0, 5.0),
            (10.0, 30.0, 0.0),
            (10.0, 30.0, -5.0),
            (math.nan, 30.0, 5.0),
            (10.0, math.inf, 5.0),
            (10.0, 30.0, math.nan),
        ],
    )
    def test_invalid_properties(
        self,
        focal_length,
        object_distance,
        object_height,
    ):
        with pytest.raises(ValueError):
            calculate_mirror_magnification_properties(
                focal_length,
                object_distance,
                object_height,
            )

    def test_result_is_immutable(self):
        result = calculate_mirror_magnification_properties(
            10.0, 30.0, 5.0
        )

        with pytest.raises(FrozenInstanceError):
            result.magnification = 5.0
