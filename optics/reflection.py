import math


def calculate_reflection(incident_angle: float) -> float:
    """
    Calculate the reflected angle using the law of reflection.

    Parameters
    ----------
    incident_angle : float
        Angle of incidence in degrees, measured from the normal.

    Returns
    -------
    float
        Reflected angle in degrees.

    Raises
    ------
    ValueError
        If the incident angle is outside the range [0, 90].
    """

    if not math.isfinite(incident_angle):
        raise ValueError("Incident angle must be finite.")

    if not 0 <= incident_angle <= 90:
        raise ValueError(
            "Incident angle must be between 0 and 90 degrees."
        )

    return float(incident_angle)