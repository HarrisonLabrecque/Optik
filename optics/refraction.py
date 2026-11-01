from optics.snells_law import calculate_snells_law


def calculate_refraction(
    n1: float,
    n2: float,
    incident_angle: float
) -> float:
    """Calculate the refracted angle in degrees."""

    return calculate_snells_law(n1, n2, incident_angle)