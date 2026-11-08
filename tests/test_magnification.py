
"""
Optik - Magnification Unit Tests
Version: 0.3.0

Tests:
    optics/magnification.py

Coverage:
    - Magnification calculations
    - Positive and negative object distances
    - Image height calculations
    - Zero and negative object heights
    - Image orientation classification
    - Non-finite input validation
    - Integration tests

Run:
    python -m pytest tests/test_magnification.py -v
"""

import math

import pytest

from optics.magnification import (
    calculate_magnification,
    calculate_image_height,
    classify_orientation,
)


# ============================================================
# MAGNIFICATION CALCULATIONS
# ============================================================

class TestCalculateMagnification:

    @pytest.mark.parametrize(
        "image_distance, object_distance, expected",
        [
            (15.0, 30.0, -0.5),
            (20.0, 20.0, -1.0),
            (30.0, 15.0, -2.0),
            (-10.0, 20.0, 0.5),
            (-20.0, 10.0, 2.0),
            (0.0, 20.0, 0.0),
            (10.0, -5.0, 2.0),
            (-10.0, -5.0, -2.0),
        ],
    )
    def test_magnification_values(
        self,
        image_distance,
        object_distance,
        expected,
    ):
        result = calculate_magnification(
            image_distance,
            object_distance,
        )

        assert result == pytest.approx(expected)

    def test_zero_object_distance(self):
        with pytest.raises((ValueError, ZeroDivisionError)):
            calculate_magnification(10.0, 0.0)

    @pytest.mark.parametrize(
        "image_distance, object_distance",
        [
            (math.nan, 10.0),
            (math.inf, 10.0),
            (-math.inf, 10.0),
            (10.0, math.nan),
            (10.0, math.inf),
            (10.0, -math.inf),
        ],
    )
    def test_nonfinite_inputs(
        self,
        image_distance,
        object_distance,
    ):
        with pytest.raises(ValueError):
            calculate_magnification(
                image_distance,
                object_distance,
            )


# ============================================================
# IMAGE HEIGHT CALCULATIONS
# ============================================================

class TestCalculateImageHeight:

    @pytest.mark.parametrize(
        "magnification, object_height, expected",
        [
            (-0.5, 5.0, -2.5),
            (-1.0, 5.0, -5.0),
            (-2.0, 3.0, -6.0),
            (0.5, 8.0, 4.0),
            (2.0, 4.0, 8.0),
            (0.0, 5.0, 0.0),
            (-1.0, 0.0, 0.0),
            (-1.0, -5.0, 5.0),
            (2.0, -4.0, -8.0),
        ],
    )
    def test_image_height_values(
        self,
        magnification,
        object_height,
        expected,
    ):
        result = calculate_image_height(
            magnification,
            object_height,
        )

        assert result == pytest.approx(expected)

    @pytest.mark.parametrize(
        "magnification, object_height",
        [
            (math.nan, 5.0),
            (math.inf, 5.0),
            (-math.inf, 5.0),
            (1.0, math.nan),
            (1.0, math.inf),
            (1.0, -math.inf),
        ],
    )
    def test_nonfinite_inputs(
        self,
        magnification,
        object_height,
    ):
        with pytest.raises(ValueError):
            calculate_image_height(
                magnification,
                object_height,
            )


# ============================================================
# IMAGE ORIENTATION
# ============================================================

class TestClassifyOrientation:

    @pytest.mark.parametrize(
        "magnification, expected",
        [
            (-2.0, "Inverted"),
            (-1.0, "Inverted"),
            (-0.5, "Inverted"),
            (0.5, "Upright"),
            (1.0, "Upright"),
            (2.0, "Upright"),
        ],
    )
    def test_orientation(
        self,
        magnification,
        expected,
    ):
        result = classify_orientation(
            magnification
        )

        assert result == expected

    def test_zero_magnification(self):
        result = classify_orientation(0.0)
        assert result == "Undefined"

    @pytest.mark.parametrize(
        "value",
        [
            math.nan,
            math.inf,
            -math.inf,
        ],
    )
    def test_invalid_orientation(self, value):
        with pytest.raises(ValueError):
            classify_orientation(value)


# ============================================================
# INTEGRATION TESTS
# ============================================================

class TestMagnificationIntegration:

    def test_real_reduced_image(self):
        image_distance = 15.0
        object_distance = 30.0
        object_height = 5.0

        magnification = calculate_magnification(
            image_distance,
            object_distance,
        )

        image_height = calculate_image_height(
            magnification,
            object_height,
        )

        assert magnification == pytest.approx(-0.5)
        assert image_height == pytest.approx(-2.5)

        assert classify_orientation(
            magnification
        ) == "Inverted"

    def test_virtual_enlarged_image(self):
        image_distance = -20.0
        object_distance = 10.0
        object_height = 4.0

        magnification = calculate_magnification(
            image_distance,
            object_distance,
        )

        image_height = calculate_image_height(
            magnification,
            object_height,
        )

        assert magnification == pytest.approx(2.0)
        assert image_height == pytest.approx(8.0)

        assert classify_orientation(
            magnification
        ) == "Upright"

    def test_same_size_inverted_image(self):
        magnification = calculate_magnification(
            20.0,
            20.0,
        )

        assert magnification == pytest.approx(-1.0)

        assert classify_orientation(
            magnification
        ) == "Inverted"

    def test_negative_object_distance(self):
        magnification = calculate_magnification(
            10.0,
            -5.0,
        )

        assert magnification == pytest.approx(2.0)

        assert classify_orientation(
            magnification
        ) == "Upright"

    def test_negative_object_height(self):
        image_height = calculate_image_height(
            -1.0,
            -5.0,
        )

        assert image_height == pytest.approx(5.0)

    def test_zero_object_height(self):
        image_height = calculate_image_height(
            -1.0,
            0.0,
        )

        assert image_height == pytest.approx(0.0)
