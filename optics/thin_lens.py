"""
Optik — Thin Lens Calculations
Version: 0.2.0

Implements the thin lens equation for paraxial geometrical optics.

Sign convention:
    f > 0: Converging lens
    f < 0: Diverging lens

    do > 0: Real object
    do < 0: Virtual object

    di > 0: Real image
    di < 0: Virtual image

Distances must use consistent units.
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ThinLensResult:
    """Results of a thin lens calculation."""

    focal_length: float
    object_distance: float
    image_distance: float

    lens_type: str
    image_type: str


def _validate_number(value: float, name: str) -> float:
    """Validate a finite numeric input."""

    if isinstance(value, bool):
        raise ValueError(f"{name} must be a number.")

    try:
        value = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"{name} must be a number."
        ) from exc

    if not math.isfinite(value):
        raise ValueError(
            f"{name} must be finite."
        )

    return value


def _validate_nonzero(value: float, name: str) -> float:
    """Validate that a numeric value is nonzero."""

    value = _validate_number(value, name)

    if value == 0.0:
        raise ValueError(
            f"{name} cannot be zero."
        )

    return value


def calculate_image_distance(
    focal_length: float,
    object_distance: float,
) -> float:
    """
    Calculate image distance using the thin lens equation.

    1/f = 1/do + 1/di

    Rearranged:

    di = (f * do) / (do - f)

    Returns:
        Positive: Real image
        Negative: Virtual image
        math.inf: Image at positive infinity
        -math.inf: Image at negative infinity
    """

    f = _validate_nonzero(
        focal_length,
        "Focal length",
    )

    do = _validate_nonzero(
        object_distance,
        "Object distance",
    )

    denominator = (1.0 / f) - (1.0 / do)

    if denominator == 0.0:
        return math.inf

    return 1.0 / denominator


def calculate_focal_length(
    object_distance: float,
    image_distance: float,
) -> float:
    """
    Calculate focal length from object and image distances.

    f = (do * di) / (do + di)
    """

    do = _validate_nonzero(
        object_distance,
        "Object distance",
    )

    di = _validate_nonzero(
        image_distance,
        "Image distance",
    )

    denominator = (1.0 / do) + (1.0 / di)

    if denominator == 0.0:
        raise ValueError(
            "The supplied distances describe zero optical power "
            "(infinite focal length), not a finite thin lens."
        )

    return 1.0 / denominator


def calculate_object_distance(
    focal_length: float,
    image_distance: float,
) -> float:
    """
    Calculate object distance from focal length
    and image distance.

    do = (f * di) / (di - f)
    """

    f = _validate_nonzero(
        focal_length,
        "Focal length",
    )

    di = _validate_nonzero(
        image_distance,
        "Image distance",
    )

    denominator = (1.0 / f) - (1.0 / di)

    if denominator == 0.0:
        return math.inf

    return 1.0 / denominator


def classify_lens(focal_length: float) -> str:
    """Identify a converging or diverging lens."""

    f = _validate_nonzero(
        focal_length,
        "Focal length",
    )

    if f > 0:
        return "Converging"

    return "Diverging"


def classify_image(image_distance: float) -> str:
    """Identify the image as real, virtual, or at infinity."""

    if not isinstance(image_distance, (int, float)):
        raise ValueError(
            "Image distance must be numeric."
        )

    di = float(image_distance)

    if math.isnan(di):
        raise ValueError(
            "Image distance cannot be NaN."
        )

    if math.isinf(di):
        return "At Infinity"

    if di > 0:
        return "Real"

    if di < 0:
        return "Virtual"

    raise ValueError(
        "Image distance cannot be zero."
    )


def calculate_thin_lens(
    focal_length: float,
    object_distance: float,
) -> ThinLensResult:
    """
    Perform a complete thin lens calculation.

    Args:
        focal_length:
            Lens focal length.

        object_distance:
            Distance between the object and lens.

    Returns:
        ThinLensResult containing calculated values
        and image classification.
    """

    f = _validate_nonzero(
        focal_length,
        "Focal length",
    )

    do = _validate_nonzero(
        object_distance,
        "Object distance",
    )

    di = calculate_image_distance(
        focal_length=f,
        object_distance=do,
    )

    return ThinLensResult(
        focal_length=f,
        object_distance=do,
        image_distance=di,
        lens_type=classify_lens(f),
        image_type=classify_image(di),
    )