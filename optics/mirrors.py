
"""
Optik - Spherical Mirror Calculations
Version: 0.3.0

Physics calculations for concave and convex spherical mirrors.

Sign convention:
    f > 0: Concave mirror
    f < 0: Convex mirror
    do > 0: Real object
    di > 0: Real image
    di < 0: Virtual image

Equations:
    1/f = 1/do + 1/di
    di = (f * do) / (do - f)
    R = 2f

The calculations use the paraxial approximation.
"""

from dataclasses import dataclass
from math import isfinite, inf


@dataclass(frozen=True)
class MirrorResult:
    """Stores the results of a spherical mirror calculation."""

    focal_length: float
    object_distance: float
    image_distance: float
    radius_of_curvature: float
    mirror_type: str
    image_type: str


def _validate_finite(value: float, name: str) -> float:
    """Validate and return a finite numerical value."""
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a number.") from exc

    if not isfinite(number):
        raise ValueError(f"{name} must be finite.")

    return number


def classify_mirror(focal_length: float) -> str:
    """Classify a spherical mirror using its focal length."""
    focal_length = _validate_finite(focal_length, "Focal length")

    if focal_length == 0:
        raise ValueError("Focal length cannot be zero.")

    return "Concave" if focal_length > 0 else "Convex"


def calculate_radius_of_curvature(focal_length: float) -> float:
    """
    Calculate the signed radius of curvature.

    R = 2f
    """
    focal_length = _validate_finite(focal_length, "Focal length")

    if focal_length == 0:
        raise ValueError("Focal length cannot be zero.")

    radius = 2.0 * focal_length

    if not isfinite(radius):
        raise ValueError("Calculated radius is outside the supported range.")

    return radius


def calculate_mirror_image_distance(
    focal_length: float,
    object_distance: float,
) -> float:
    """
    Calculate image distance using the spherical mirror equation.

    di = (f * do) / (do - f)

    Returns positive infinity when a real object is located
    exactly at the focal point of a concave mirror.
    """
    focal_length = _validate_finite(focal_length, "Focal length")
    object_distance = _validate_finite(object_distance, "Object distance")

    if focal_length == 0:
        raise ValueError("Focal length cannot be zero.")

    if object_distance <= 0:
        raise ValueError("Object distance must be greater than zero.")

    if object_distance == focal_length:
        return inf

    # Reciprocal form avoids overflow in the f * do product.
    denominator = (1.0 / focal_length) - (1.0 / object_distance)

    if denominator == 0:
        return inf

    image_distance = 1.0 / denominator

    if not isfinite(image_distance):
        raise ValueError("Calculated image distance is outside the supported range.")

    return image_distance


def classify_mirror_image(image_distance: float) -> str:
    """Classify an image as real, virtual, or at infinity."""
    try:
        distance = float(image_distance)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Image distance must be a number.") from exc

    if distance == inf:
        return "At Infinity"

    if not isfinite(distance):
        raise ValueError("Image distance must be finite or positive infinity.")

    if distance > 0:
        return "Real"

    if distance < 0:
        return "Virtual"

    raise ValueError("Image distance cannot be zero.")


def calculate_mirror_properties(
    focal_length: float,
    object_distance: float,
) -> MirrorResult:
    """
    Calculate the main properties of a spherical mirror.

    Returns:
        MirrorResult containing mirror classification,
        radius of curvature, image distance, and image type.
    """
    focal_length = _validate_finite(focal_length, "Focal length")
    object_distance = _validate_finite(object_distance, "Object distance")

    mirror_type = classify_mirror(focal_length)
    radius = calculate_radius_of_curvature(focal_length)
    image_distance = calculate_mirror_image_distance(
        focal_length,
        object_distance,
    )
    image_type = classify_mirror_image(image_distance)

    return MirrorResult(
        focal_length=focal_length,
        object_distance=object_distance,
        image_distance=image_distance,
        radius_of_curvature=radius,
        mirror_type=mirror_type,
        image_type=image_type,
    )
