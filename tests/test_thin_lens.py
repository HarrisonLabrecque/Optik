"""
Optik — Thin Lens Unit Tests
Version: 0.2.0
"""

import math

import pytest

from optics.thin_lens import (
    calculate_image_distance,
    calculate_focal_length,
    calculate_object_distance,
    calculate_thin_lens,
    classify_lens,
    classify_image,
)


class TestImageDistance:

    def test_converging_lens_real_image(self):
        result = calculate_image_distance(10.0, 30.0)

        assert result == pytest.approx(15.0)

    def test_converging_lens_virtual_image(self):
        result = calculate_image_distance(10.0, 5.0)

        assert result == pytest.approx(-10.0)

    def test_diverging_lens_virtual_image(self):
        result = calculate_image_distance(-10.0, 30.0)

        assert result == pytest.approx(-7.5)

    def test_object_at_focal_point(self):
        result = calculate_image_distance(10.0, 10.0)

        assert math.isinf(result)
        assert result > 0

    def test_virtual_object(self):
        result = calculate_image_distance(10.0, -20.0)

        assert result == pytest.approx(20.0 / 3.0)


class TestFocalLength:

    def test_calculate_focal_length(self):
        result = calculate_focal_length(30.0, 15.0)

        assert result == pytest.approx(10.0)

    def test_diverging_focal_length(self):
        result = calculate_focal_length(30.0, -7.5)

        assert result == pytest.approx(-10.0)

    def test_infinite_focal_length(self):
        with pytest.raises(ValueError):
            calculate_focal_length(10.0, -10.0)


class TestObjectDistance:

    def test_calculate_object_distance(self):
        result = calculate_object_distance(10.0, 15.0)

        assert result == pytest.approx(30.0)

    def test_object_at_infinity(self):
        result = calculate_object_distance(10.0, 10.0)

        assert math.isinf(result)


class TestClassification:

    def test_converging_lens(self):
        assert classify_lens(10.0) == "Converging"

    def test_diverging_lens(self):
        assert classify_lens(-10.0) == "Diverging"

    def test_real_image(self):
        assert classify_image(15.0) == "Real"

    def test_virtual_image(self):
        assert classify_image(-10.0) == "Virtual"

    def test_image_at_infinity(self):
        assert classify_image(math.inf) == "At Infinity"


class TestThinLens:

    def test_complete_calculation(self):
        result = calculate_thin_lens(10.0, 30.0)

        assert result.focal_length == 10.0
        assert result.object_distance == 30.0
        assert result.image_distance == pytest.approx(15.0)
        assert result.lens_type == "Converging"
        assert result.image_type == "Real"

    @pytest.mark.parametrize(
        "focal_length, object_distance",
        [
            (0.0, 10.0),
            (10.0, 0.0),
            (math.nan, 10.0),
            (math.inf, 10.0),
            (10.0, -math.inf),
            ("invalid", 10.0),
            (10.0, None),
        ],
    )
    def test_invalid_inputs(
        self,
        focal_length,
        object_distance,
    ):
        with pytest.raises(ValueError):
            calculate_thin_lens(
                focal_length,
                object_distance,
            )

    def test_boolean_input_rejected(self):
        with pytest.raises(ValueError):
            calculate_thin_lens(True, 30.0)