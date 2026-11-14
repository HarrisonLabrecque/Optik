
"""
Optik — Prism Ray Diagram
Version: 0.4.0

Matplotlib visualization for triangular prism optics.

Features:
    - Triangular prism geometry
    - Incident, internal, and emergent rays
    - Snell's law integration
    - Total internal reflection visualization
    - Light and dark themes
    - Diagram export and clearing

Assumptions:
    - Prism surrounded by air
    - Angles in degrees
    - Geometrical optics
    - Apex points upward
    - Ray enters the left sloping face

Dependencies:
    matplotlib
    numpy
"""

from __future__ import annotations

import math
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Polygon, FancyArrowPatch
import numpy as np

from optics.prisms import (
    PrismResult,
    PrismError,
    TotalInternalReflectionError,
    calculate_prism_refraction,
)


# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_APEX_ANGLE = 60.0
DEFAULT_INCIDENT_ANGLE = 45.0
DEFAULT_REFRACTIVE_INDEX = 1.5

DEFAULT_OBJECT_HEIGHT = 4.0

LIGHT_BACKGROUND = "#FFFFFF"
DARK_BACKGROUND = "#1E1E1E"

LIGHT_FOREGROUND = "#202020"
DARK_FOREGROUND = "#F0F0F0"

PRISM_COLOR = "#66B3FF"
INCIDENT_RAY_COLOR = "#E69F00"
INTERNAL_RAY_COLOR = "#009E73"
EMERGENT_RAY_COLOR = "#D55E00"
REFLECTED_RAY_COLOR = "#CC79A7"


# ============================================================
# PRISM DIAGRAM
# ============================================================

class PrismDiagram:
    """
    Matplotlib-based triangular prism ray diagram.

    Parameters
    ----------
    figure : Figure, optional
        Existing Matplotlib figure.

    dark_mode : bool
        Enable dark appearance.
    """

    def __init__(
        self,
        figure: Optional[Figure] = None,
        dark_mode: bool = False,
    ) -> None:

        self.figure = figure or Figure(figsize=(9, 6))
        self.ax = self.figure.add_subplot(111)

        self.dark_mode = bool(dark_mode)

        self.last_result: Optional[PrismResult] = None

        self._apply_theme()

    # ========================================================
    # THEME
    # ========================================================

    def _apply_theme(self) -> None:
        """Apply light or dark colors."""

        background = (
            DARK_BACKGROUND
            if self.dark_mode
            else LIGHT_BACKGROUND
        )

        foreground = (
            DARK_FOREGROUND
            if self.dark_mode
            else LIGHT_FOREGROUND
        )

        self.figure.patch.set_facecolor(background)
        self.ax.set_facecolor(background)

        self.ax.tick_params(colors=foreground)

        for spine in self.ax.spines.values():
            spine.set_color(foreground)

        self.ax.xaxis.label.set_color(foreground)
        self.ax.yaxis.label.set_color(foreground)
        self.ax.title.set_color(foreground)

    def set_dark_mode(self, enabled: bool) -> None:
        """Change the diagram theme."""

        self.dark_mode = bool(enabled)
        self._apply_theme()

        if self.figure.canvas is not None:
            self.figure.canvas.draw_idle()

    # ========================================================
    # GEOMETRY HELPERS
    # ========================================================

    @staticmethod
    def _normalize(vector: np.ndarray) -> np.ndarray:
        """Return a normalized 2D vector."""

        magnitude = np.linalg.norm(vector)

        if magnitude == 0:
            raise PrismError(
                "Cannot normalize a zero-length vector."
            )

        return vector / magnitude

    @staticmethod
    def _rotate(
        vector: np.ndarray,
        angle_degrees: float,
    ) -> np.ndarray:
        """Rotate a 2D vector counterclockwise."""

        angle = math.radians(angle_degrees)

        rotation = np.array([
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ])

        return rotation @ vector

    @staticmethod
    def _ray_intersection(
        origin: np.ndarray,
        direction: np.ndarray,
        point_a: np.ndarray,
        point_b: np.ndarray,
    ) -> Optional[np.ndarray]:
        """
        Intersect a ray with a line segment.

        Returns None when no forward intersection exists.
        """

        segment = point_b - point_a

        matrix = np.column_stack(
            (direction, -segment)
        )

        determinant = np.linalg.det(matrix)

        if abs(determinant) < 1e-12:
            return None

        parameters = np.linalg.solve(
            matrix,
            point_a - origin,
        )

        ray_parameter = parameters[0]
        segment_parameter = parameters[1]

        if (
            ray_parameter >= 0
            and 0 <= segment_parameter <= 1
        ):
            return origin + ray_parameter * direction

        return None

    # ========================================================
    # PRISM GEOMETRY
    # ========================================================

    def _create_prism_vertices(
        self,
        apex_angle: float,
        height: float = DEFAULT_OBJECT_HEIGHT,
    ) -> np.ndarray:
        """
        Create an isosceles triangular prism.

        The apex is centered above the base.
        """

        half_angle = math.radians(apex_angle / 2)

        half_width = height * math.tan(half_angle)

        return np.array([
            [-half_width, 0.0],
            [half_width, 0.0],
            [0.0, height],
        ], dtype=float)

    # ========================================================
    # DRAWING HELPERS
    # ========================================================

    def _draw_ray(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: str,
        label: str,
    ) -> None:
        """Draw a directional ray."""

        arrow = FancyArrowPatch(
            posA=start,
            posB=end,
            arrowstyle="->",
            mutation_scale=14,
            linewidth=2.2,
            color=color,
            label=label,
        )

        self.ax.add_patch(arrow)

    def _draw_prism(self, vertices: np.ndarray) -> None:
        """Draw the triangular prism."""

        polygon = Polygon(
            vertices,
            closed=True,
            facecolor=PRISM_COLOR,
            edgecolor="#2874A6",
            alpha=0.22,
            linewidth=2.0,
        )

        self.ax.add_patch(polygon)

    # ========================================================
    # MAIN DRAW METHOD
    # ========================================================

    def draw(
        self,
        apex_angle: float = DEFAULT_APEX_ANGLE,
        incident_angle: float = DEFAULT_INCIDENT_ANGLE,
        refractive_index: float = DEFAULT_REFRACTIVE_INDEX,
    ) -> Optional[PrismResult]:
        """
        Draw a prism ray diagram.

        Parameters
        ----------
        apex_angle : float
            Prism apex angle in degrees.

        incident_angle : float
            Incident angle at the first surface.

        refractive_index : float
            Prism refractive index.

        Returns
        -------
        PrismResult or None
            Result for transmitted rays, or None for TIR.
        """

        self.clear()

        vertices = self._create_prism_vertices(
            apex_angle
        )

        left_base = vertices[0]
        right_base = vertices[1]
        apex = vertices[2]

        self._draw_prism(vertices)

        # ----------------------------------------------------
        # ENTRY POINT
        # ----------------------------------------------------

        entry_point = (
            left_base + apex
        ) / 2.0

        left_face = apex - left_base

        left_normal = self._normalize(
            np.array([
                left_face[1],
                -left_face[0],
            ])
        )

        # ----------------------------------------------------
        # INCIDENT DIRECTION
        # ----------------------------------------------------

        incident_direction = self._rotate(
            left_normal,
            incident_angle,
        )

        incident_start = (
            entry_point - incident_direction * 3.0
        )

        self._draw_ray(
            incident_start,
            entry_point,
            INCIDENT_RAY_COLOR,
            "Incident Ray",
        )

        # ----------------------------------------------------
        # FIRST REFRACTION
        # ----------------------------------------------------

        incident_radians = math.radians(
            incident_angle
        )

        refracted_angle = math.degrees(
            math.asin(
                math.sin(incident_radians)
                / refractive_index
            )
        )

        internal_direction = self._rotate(
            left_normal,
            refracted_angle,
        )

        # ----------------------------------------------------
        # INTERSECTION WITH SECOND SURFACE
        # ----------------------------------------------------

        exit_point = self._ray_intersection(
            entry_point,
            internal_direction,
            apex,
            right_base,
        )

        if exit_point is None:
            raise PrismError(
                "Internal ray does not intersect "
                "the second prism surface."
            )

        self._draw_ray(
            entry_point,
            exit_point,
            INTERNAL_RAY_COLOR,
            "Internal Ray",
        )

        # ----------------------------------------------------
        # PRISM CALCULATION
        # ----------------------------------------------------

        try:
            result = calculate_prism_refraction(
                apex_angle,
                incident_angle,
                refractive_index,
            )

        except TotalInternalReflectionError:
            # Draw a schematic reflected ray.
            reflected_direction = self._rotate(
                internal_direction,
                -60.0,
            )

            reflected_end = (
                exit_point + reflected_direction * 2.5
            )

            self._draw_ray(
                exit_point,
                reflected_end,
                REFLECTED_RAY_COLOR,
                "Total Internal Reflection",
            )

            self.ax.set_title(
                "Prism Ray Diagram — Total Internal Reflection"
            )

            self._finalize()
            self.last_result = None

            return None

        # ----------------------------------------------------
        # EMERGENT RAY
        # ----------------------------------------------------

        right_face = right_base - apex

        right_normal = self._normalize(
            np.array([
                right_face[1],
                -right_face[0],
            ])
        )

        emergent_direction = self._rotate(
            right_normal,
            -result.emergent_angle,
        )

        emergent_end = (
            exit_point + emergent_direction * 3.0
        )

        self._draw_ray(
            exit_point,
            emergent_end,
            EMERGENT_RAY_COLOR,
            "Emergent Ray",
        )

        self.ax.set_title(
            "Prism Ray Diagram\n"
            f"Deviation: {result.deviation_angle:.2f}°"
        )

        self.last_result = result

        self._finalize()

        return result

    # ========================================================
    # FINALIZE
    # ========================================================

    def _finalize(self) -> None:
        """Apply axes, scaling, legend, and canvas refresh."""

        self.ax.set_aspect("equal", adjustable="datalim")
        self.ax.autoscale_view()

        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")

        self.ax.grid(
            True,
            linestyle="--",
            alpha=0.15,
        )

        self.ax.legend(
            loc="upper right",
            fontsize=9,
        )

        self._apply_theme()

        self.figure.tight_layout()

        if self.figure.canvas is not None:
            self.figure.canvas.draw_idle()

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self) -> None:
        """Clear the diagram."""

        self.ax.clear()
        self.last_result = None
        self._apply_theme()

        if self.figure.canvas is not None:
            self.figure.canvas.draw_idle()

    # ========================================================
    # SAVE
    # ========================================================

    def save(
        self,
        filename: str,
        dpi: int = 150,
    ) -> None:
        """Export the diagram to an image file."""

        self.figure.savefig(
            filename,
            dpi=dpi,
            bbox_inches="tight",
        )


# ============================================================
# STANDALONE PREVIEW
# ============================================================

if __name__ == "__main__":

    diagram = PrismDiagram()

    diagram.draw(
        apex_angle=60.0,
        incident_angle=45.0,
        refractive_index=1.5,
    )

    plt.show()
