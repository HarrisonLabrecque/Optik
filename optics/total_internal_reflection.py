import math


def calculate_critical_angle(
    n1: float,
    n2: float
) -> float:
    """Calculate the critical angle in degrees."""

    # Validate refractive indices
    if not math.isfinite(n1) or not math.isfinite(n2):
        raise ValueError("Refractive indices must be finite.")

    if n1 <= 0 or n2 <= 0:
        raise ValueError("Refractive indices must be positive.")

    # Critical angle requires n1 > n2
    if n1 <= n2:
        raise ValueError(
            "Critical angle requires n1 to be greater than n2."
        )

    # Calculate critical angle
    critical_angle = math.asin(n2 / n1)

    return math.degrees(critical_angle)


def is_total_internal_reflection(
    n1: float,
    n2: float,
    incident_angle: float
) -> bool:
    """Determine whether total internal reflection occurs."""

    # Validate refractive indices
    if not math.isfinite(n1) or not math.isfinite(n2):
        raise ValueError("Refractive indices must be finite.")

    if n1 <= 0 or n2 <= 0:
        raise ValueError("Refractive indices must be positive.")

    # Validate incident angle
    if not math.isfinite(incident_angle):
        raise ValueError("Incident angle must be finite.")

    if not 0 <= incident_angle <= 90:
        raise ValueError(
            "Incident angle must be between 0 and 90 degrees."
        )

    # Total internal reflection requires n1 > n2
    if n1 <= n2:
        return False

    # Calculate critical angle
    critical_angle = calculate_critical_angle(n1, n2)

    # Determine whether total internal reflection occurs
    return incident_angle > critical_angle