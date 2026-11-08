
"""
Optik - Mirror Magnification Calculations
Version: 0.3.0

Calculates image magnification and image properties for
concave and convex spherical mirrors.

Equations:
    m = -di / do
    hi = m * ho

Sign convention:
    do > 0 : Real object distance
    di > 0 : Real image
    di < 0 : Virtual image
    m > 0  : Upright image
    m < 0  : Inverted image

The model assumes ideal paraxial spherical mirrors.
"""

from dataclasses import dataclass
from math import isfinite, inf

from optics.mirrors import calculate_mirror_image_distance


@dataclass(frozen=True)
class MirrorMagnificationResult:
    """Stores calculated mirror image properties."""

    object_distance: float
    image_distance: float
    object_height: float
    magnification: float
    image_height: float
    orientation: str
    image_size: str


def _validate_finite(value: float, name: str) -> float:
    """Validate that a value is a finite number."""
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a number.") from exc

    if not isfinite(number):
        raise ValueError(f"{name} must be finite.")

    return number


def calculate_mirror_magnification(
    image_distance: float,
    object_distance: float,
) -> float:
    """
    Calculate lateral magnification.

    m = -di / do

    Positive magnification indicates an upright image.
    Negative magnification indicates an inverted image.
    """
    di = _validate_finite(image_distance, "Image distance")
    do = _validate_finite(object_distance, "Object distance")

    if do <= 0:
        raise ValueError("Object distance must be greater than zero.")

    magnification = -di / do

    if not isfinite(magnification):
        raise ValueError("Magnification is outside the supported range.")

    return magnification


def calculate_mirror_image_height(
    magnification: float,
    object_height: float,
) -> float:
    """
    Calculate signed image height.

    hi = m * ho
    """
    m = _validate_finite(magnification, "Magnification")
    ho = _validate_finite(object_height, "Object height")

    if ho <= 0:
        raise ValueError("Object height must be greater than zero.")

    image_height = m * ho

    if not isfinite(image_height):
        raise ValueError("Image height is outside the supported range.")

    return image_height


def classify_mirror_orientation(magnification: float) -> str:
    """Classify the image as upright or inverted."""
    m = _validate_finite(magnification, "Magnification")

    if m > 0:
        return "Upright"

    if m < 0:
        return "Inverted"

    return "Undefined"


def classify_mirror_image_size(magnification: float) -> str:
    """Classify the image size relative to the object."""
    m = _validate_finite(magnification, "Magnification")
    magnitude = abs(m)

    if magnitude == 1.0:
        return "Same Size"

    if magnitude > 1.0:
        return "Enlarged"

    return "Reduced"


def calculate_mirror_magnification_properties(
    focal_length: float,
    object_distance: float,
    object_height: float,
) -> MirrorMagnificationResult:
    """
    Calculate all magnification-related mirror properties.

    Raises:
        ValueError: For invalid inputs or an image at infinity,
                    where finite magnification is undefined.
    """
    do = _validate_finite(object_distance, "Object distance")
    ho = _validate_finite(object_height, "Object height")

    if do <= 0:
        raise ValueError("Object distance must be greater than zero.")

    if ho <= 0:
        raise ValueError("Object height must be greater than zero.")

    di = calculate_mirror_image_distance(
        focal_length,
        do,
    )

    if di == inf:
        raise ValueError(
            "Magnification is undefined when the image is at infinity."
        )

    magnification = calculate_mirror_magnification(di, do)
    image_height = calculate_mirror_image_height(magnification, ho)

    return MirrorMagnificationResult(
        object_distance=do,
        image_distance=di,
        object_height=ho,
        magnification=magnification,
        image_height=image_height,
        orientation=classify_mirror_orientation(magnification),
        image_size=classify_mirror_image_size(magnification),
    )


if __name__ == "__main__":
    examples = [
        ("Concave mirror", 10.0, 30.0, 5.0),
        ("Convex mirror", -10.0, 30.0, 5.0),
        ("Concave virtual image", 10.0, 5.0, 5.0),
    ]

    for name, focal_length, object_distance, object_height in examples:
        result = calculate_mirror_magnification_properties(
            focal_length,
            object_distance,
            object_height,
        )

        print(f"\n{name}")
        print(f"Image distance: {result.image_distance:.2f}")
        print(f"Magnification: {result.magnification:.3f}")
        print(f"Image height: {result.image_height:.2f}")
        print(f"Orientation: {result.orientation}")
        print(f"Image size: {result.image_size}")
