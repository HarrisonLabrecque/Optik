"""
Optik — Magnification Calculations
Version: 0.2.0

Calculates linear magnification and image height
for thin optical lenses.
"""

import math

from dataclasses import dataclass


@dataclass(frozen=True)
class MagnificationResult:
    image_distance: float
    object_distance: float
    object_height: float
    magnification: float
    image_height: float
    orientation: str
    image_size: str

def calculate_magnification(
    image_distance: float,
    object_distance: float,
) -> float:
    """
    Calculate signed linear magnification.

    m = -di / do

    Positive: Upright image
    Negative: Inverted image
    """

    if not math.isfinite(image_distance):
        raise ValueError("Image distance must be finite.")

    if not math.isfinite(object_distance):
        raise ValueError("Object distance must be finite.")

    if object_distance == 0:
        raise ValueError("Object distance cannot be zero.")

    return -(image_distance / object_distance)


def calculate_image_height(
    magnification: float,
    object_height: float,
) -> float:
    """
    Calculate signed image height.

    hi = m * ho
    """

    if not math.isfinite(magnification):
        raise ValueError("Magnification must be finite.")

    if not math.isfinite(object_height):
        raise ValueError("Object height must be finite.")

    return magnification * object_height

import math


def classify_orientation(magnification: float) -> str:
    """
    Classify image orientation using signed magnification.

    Positive magnification: Upright
    Negative magnification: Inverted
    Zero magnification: No defined orientation
    """

    if not math.isfinite(magnification):
        raise ValueError("Magnification must be finite.")

    if magnification > 0:
        return "Upright"

    elif magnification < 0:
        return "Inverted"

    return "Undefined"


def classify_image_size(magnification: float) -> str:
    """
    Classify image size using the magnitude of magnification.

    |m| > 1: Enlarged
    |m| < 1: Reduced
    |m| = 1: Same Size
    """

    if not math.isfinite(magnification):
        raise ValueError("Magnification must be finite.")

    magnitude = abs(magnification)

    if magnitude > 1:
        return "Enlarged"

    elif magnitude < 1:
        return "Reduced"

    return "Same Size"

def calculate_image_properties(
    image_distance: float,
    object_distance: float,
    object_height: float,
) -> MagnificationResult:
    """
    Calculate the image properties of a thin lens.

    Parameters
    ----------
    image_distance : float
        Distance from lens to image.

    object_distance : float
        Distance from lens to object.

    object_height : float
        Height of the object.

    Returns
    -------
    MagnificationResult
        Contains magnification, image height,
        image orientation, and relative image size.
    """

    magnification = calculate_magnification(
        image_distance=image_distance,
        object_distance=object_distance,
    )

    image_height = calculate_image_height(
        magnification=magnification,
        object_height=object_height,
    )

    orientation = classify_orientation(magnification)

    image_size = classify_image_size(magnification)

    return MagnificationResult(
        image_distance=image_distance,
        object_distance=object_distance,
        object_height=object_height,
        magnification=magnification,
        image_height=image_height,
        orientation=orientation,
        image_size=image_size,
    )