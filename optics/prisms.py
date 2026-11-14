
"""
Optik — Prism Optics
Version: 0.4.0

Geometrical optics calculations for triangular prisms.

Features:
    - Refraction at the first prism surface
    - Refraction at the second prism surface
    - Prism deviation angle
    - Minimum deviation angle
    - Total internal reflection detection
    - Input validation

Assumptions:
    - Prism surrounded by air (n = 1.0)
    - Homogeneous, isotropic prism material
    - Geometrical optics
    - Angles measured in degrees
    - Ray enters and exits through the intended prism faces
"""

from dataclasses import dataclass
import math


# ============================================================
# CONSTANTS
# ============================================================

AIR_REFRACTIVE_INDEX = 1.0

MIN_APEX_ANGLE = 0.0
MAX_APEX_ANGLE = 180.0

MIN_INCIDENT_ANGLE = 0.0
MAX_INCIDENT_ANGLE = 90.0

FLOAT_TOLERANCE = 1e-12


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass(frozen=True)
class PrismResult:
    """Results for a ray transmitted through a triangular prism."""

    apex_angle: float
    incident_angle: float
    refractive_index: float

    first_refracted_angle: float
    second_internal_angle: float

    emergent_angle: float
    deviation_angle: float


# ============================================================
# EXCEPTIONS
# ============================================================

class PrismError(ValueError):
    """Base exception for invalid prism calculations."""


class TotalInternalReflectionError(PrismError):
    """Raised when total internal reflection prevents emergence."""


# ============================================================
# VALIDATION
# ============================================================

def _validate_finite(value: float, name: str) -> float:
    """Validate that a numerical input is finite."""

    if isinstance(value, bool):
        raise PrismError(f"{name} must be a finite number.")

    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise PrismError(
            f"{name} must be a finite number."
        ) from exc

    if not math.isfinite(number):
        raise PrismError(
            f"{name} must be a finite number."
        )

    return number


def _validate_apex_angle(apex_angle: float) -> float:
    """Validate the prism apex angle."""

    angle = _validate_finite(apex_angle, "Apex angle")

    if not MIN_APEX_ANGLE < angle < MAX_APEX_ANGLE:
        raise PrismError(
            "Apex angle must be greater than 0 "
            "and less than 180 degrees."
        )

    return angle


def _validate_incident_angle(incident_angle: float) -> float:
    """Validate the incident angle."""

    angle = _validate_finite(
        incident_angle,
        "Incident angle",
    )

    if not MIN_INCIDENT_ANGLE <= angle < MAX_INCIDENT_ANGLE:
        raise PrismError(
            "Incident angle must be between "
            "0 (inclusive) and 90 (exclusive) degrees."
        )

    return angle


def _validate_refractive_index(
    refractive_index: float,
) -> float:
    """Validate the refractive index of the prism."""

    index = _validate_finite(
        refractive_index,
        "Refractive index",
    )

    if index <= AIR_REFRACTIVE_INDEX:
        raise PrismError(
            "Prism refractive index must be greater than 1.0."
        )

    return index


def _asin_degrees(value: float) -> float:
    """
    Calculate arcsine in degrees.

    Allow small floating-point deviations from [-1, 1].
    """

    if value < -1.0 - FLOAT_TOLERANCE:
        raise PrismError("Invalid arcsine argument.")

    if value > 1.0 + FLOAT_TOLERANCE:
        raise PrismError("Invalid arcsine argument.")

    value = max(-1.0, min(1.0, value))

    return math.degrees(math.asin(value))


# ============================================================
# PRISM REFRACTION
# ============================================================

def calculate_prism_refraction(
    apex_angle: float,
    incident_angle: float,
    refractive_index: float,
) -> PrismResult:
    """
    Calculate the refraction of light through a triangular prism.

    Parameters
    ----------
    apex_angle : float
        Prism apex angle in degrees.

    incident_angle : float
        Incident angle at the first surface in degrees.

    refractive_index : float
        Refractive index of the prism material.

    Returns
    -------
    PrismResult
        Calculated refraction and deviation properties.

    Raises
    ------
    PrismError
        If the input values or ray geometry are invalid.

    TotalInternalReflectionError
        If the ray undergoes total internal reflection at
        the second surface.

    Notes
    -----
    Snell's law at the first surface:

        sin(i1) = n * sin(r1)

    Internal prism geometry:

        r1 + r2 = A

    Snell's law at the second surface:

        n * sin(r2) = sin(i2)

    Total deviation:

        deviation = i1 + i2 - A
    """

    apex_angle = _validate_apex_angle(apex_angle)

    incident_angle = _validate_incident_angle(
        incident_angle
    )

    refractive_index = _validate_refractive_index(
        refractive_index
    )

    # --------------------------------------------------------
    # FIRST SURFACE REFRACTION
    # --------------------------------------------------------

    incident_radians = math.radians(incident_angle)

    sin_r1 = (
        AIR_REFRACTIVE_INDEX
        * math.sin(incident_radians)
        / refractive_index
    )

    first_refracted_angle = _asin_degrees(sin_r1)

    # --------------------------------------------------------
    # INTERNAL PRISM GEOMETRY
    # --------------------------------------------------------

    second_internal_angle = (
        apex_angle - first_refracted_angle
    )

    if not 0.0 <= second_internal_angle < 90.0:
        raise PrismError(
            "The ray does not intersect the second prism "
            "surface with valid transmission geometry."
        )

    # --------------------------------------------------------
    # SECOND SURFACE REFRACTION
    # --------------------------------------------------------

    second_internal_radians = math.radians(
        second_internal_angle
    )

    sin_emergent = (
        refractive_index
        * math.sin(second_internal_radians)
        / AIR_REFRACTIVE_INDEX
    )

    if sin_emergent > 1.0 + FLOAT_TOLERANCE:
        raise TotalInternalReflectionError(
            "Total internal reflection occurs at the "
            "second prism surface."
        )

    emergent_angle = _asin_degrees(sin_emergent)

    # --------------------------------------------------------
    # TOTAL DEVIATION
    # --------------------------------------------------------

    deviation_angle = (
        incident_angle
        + emergent_angle
        - apex_angle
    )

    return PrismResult(
        apex_angle=apex_angle,
        incident_angle=incident_angle,
        refractive_index=refractive_index,
        first_refracted_angle=first_refracted_angle,
        second_internal_angle=second_internal_angle,
        emergent_angle=emergent_angle,
        deviation_angle=deviation_angle,
    )


# ============================================================
# MINIMUM DEVIATION
# ============================================================

def calculate_minimum_deviation(
    apex_angle: float,
    refractive_index: float,
) -> float:
    """
    Calculate the minimum deviation of a triangular prism.

    Parameters
    ----------
    apex_angle : float
        Prism apex angle in degrees.

    refractive_index : float
        Prism refractive index.

    Returns
    -------
    float
        Minimum deviation angle in degrees.

    Raises
    ------
    PrismError
        If the prism cannot support a transmitted
        symmetric ray.

    Notes
    -----
    At minimum deviation:

        r1 = r2 = A / 2

        i1 = i2

    Therefore:

        delta_min = 2 * asin(n * sin(A / 2)) - A
    """

    apex_angle = _validate_apex_angle(apex_angle)

    refractive_index = _validate_refractive_index(
        refractive_index
    )

    half_apex_radians = math.radians(
        apex_angle / 2.0
    )

    sin_incident = (
        refractive_index
        * math.sin(half_apex_radians)
        / AIR_REFRACTIVE_INDEX
    )

    if sin_incident >= 1.0:
        raise PrismError(
            "Minimum deviation is not defined for a "
            "transmitted symmetric ray with these parameters."
        )

    incident_angle = _asin_degrees(sin_incident)

    minimum_deviation = (
        2.0 * incident_angle - apex_angle
    )

    return minimum_deviation


# ============================================================
# TOTAL INTERNAL REFLECTION
# ============================================================

def calculate_prism_critical_angle(
    refractive_index: float,
) -> float:
    """
    Calculate the critical angle at the prism-air interface.

    Returns
    -------
    float
        Critical angle in degrees.
    """

    refractive_index = _validate_refractive_index(
        refractive_index
    )

    return _asin_degrees(
        AIR_REFRACTIVE_INDEX / refractive_index
    )


def is_total_internal_reflection(
    internal_angle: float,
    refractive_index: float,
) -> bool:
    """
    Determine whether total internal reflection occurs
    at the prism-air interface.

    Parameters
    ----------
    internal_angle : float
        Angle of incidence inside the prism, in degrees.

    refractive_index : float
        Prism refractive index.

    Returns
    -------
    bool
        True if total internal reflection occurs.
    """

    internal_angle = _validate_finite(
        internal_angle,
        "Internal angle",
    )

    refractive_index = _validate_refractive_index(
        refractive_index
    )

    if not 0.0 <= internal_angle < 90.0:
        raise PrismError(
            "Internal angle must be between "
            "0 (inclusive) and 90 (exclusive) degrees."
        )

    critical_angle = calculate_prism_critical_angle(
        refractive_index
    )

    return internal_angle > critical_angle


# ============================================================
# MODULE EXPORTS
# ============================================================

__all__ = [
    "PrismResult",
    "PrismError",
    "TotalInternalReflectionError",
    "calculate_prism_refraction",
    "calculate_minimum_deviation",
    "calculate_prism_critical_angle",
    "is_total_internal_reflection",
]
