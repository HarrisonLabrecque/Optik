import math


def calculate_snells_law(
    n1: float,
    n2: float,
    incident_angle: float
) -> float:
    """
    Calculate the refracted angle using Snell's law.

    Parameters
    ----------
    n1 : float
        Refractive index of the first medium.

    n2 : float
        Refractive index of the second medium.

    incident_angle : float
        Incident angle in degrees, measured from the normal.

    Returns
    -------
    float
        Refracted angle in degrees.

    Raises
    ------
    ValueError
        If inputs are invalid or total internal reflection occurs.
    """

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

    # Convert degrees to radians
    angle_radians = math.radians(incident_angle)

    # Apply Snell's law
    sin_refracted = (n1 / n2) * math.sin(angle_radians)

    # Check for total internal reflection
    if sin_refracted > 1:
        raise ValueError(
            "Total internal reflection: no refracted angle exists."
        )

    # Calculate refracted angle
    refracted_angle = math.asin(sin_refracted)

    # Convert radians to degrees
    return math.degrees(refracted_angle)