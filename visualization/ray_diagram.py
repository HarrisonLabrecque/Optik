"""
Optik — Optical Ray Visualization
Version: 0.1.0

Provides 2D visualization of:
    - Incident rays
    - Reflected rays
    - Refracted rays
    - Total internal reflection
    - Optical interface and surface normal
"""

import math

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from PySide6.QtWidgets import QWidget, QVBoxLayout

from optics.reflection import calculate_reflection
from optics.snells_law import calculate_snells_law
from optics.total_internal_reflection import (
    is_total_internal_reflection,
)


class RayDiagram(QWidget):
    """Matplotlib-based optical ray diagram widget."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure(
            figsize=(6, 5),
            facecolor="#0b1220"
        )

        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axes = self.figure.add_subplot(111)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.draw_reflection(45.0)

    def _setup_axes(self, title: str):
        """Configure the optical diagram appearance."""

        self.axes.clear()

        self.axes.set_facecolor("#111c30")

        self.axes.set_xlim(-1.2, 1.2)
        self.axes.set_ylim(-1.2, 1.2)

        self.axes.set_aspect("equal")

        self.axes.set_title(
            title,
            color="#f8fafc",
            fontsize=13,
            pad=15
        )

        self.axes.set_xlabel("Horizontal Position", color="#cbd5e1")
        self.axes.set_ylabel("Vertical Position", color="#cbd5e1")

        self.axes.tick_params(colors="#94a3b8")

        for spine in self.axes.spines.values():
            spine.set_color("#475569")

        # Optical interface
        self.axes.axhline(
            0,
            color="#94a3b8",
            linewidth=2,
            label="Optical Interface"
        )

        # Surface normal
        self.axes.axvline(
            0,
            color="#64748b",
            linestyle="--",
            linewidth=1.5,
            label="Surface Normal"
        )

        self.axes.grid(
            True,
            alpha=0.12
        )

    def _draw_ray(
        self,
        start: tuple,
        end: tuple,
        color: str,
        label: str
    ):
        """Draw a directional optical ray."""

        dx = end[0] - start[0]
        dy = end[1] - start[1]

        self.axes.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={
                "arrowstyle": "->",
                "color": color,
                "linewidth": 2.5,
                "mutation_scale": 15,
            }
        )

        # Invisible line for legend
        self.axes.plot(
            [],
            [],
            color=color,
            linewidth=2.5,
            label=label
        )

    def draw_reflection(self, incident_angle: float):
        """Draw an incident and reflected ray."""

        reflected_angle = calculate_reflection(incident_angle)

        self._setup_axes("Law of Reflection")

        incident_rad = math.radians(incident_angle)
        reflected_rad = math.radians(reflected_angle)

        # Incident ray travels toward the interface
        incident_start = (
            -math.sin(incident_rad),
            math.cos(incident_rad)
        )

        # Reflected ray travels away from the interface
        reflected_end = (
            math.sin(reflected_rad),
            math.cos(reflected_rad)
        )

        self._draw_ray(
            incident_start,
            (0, 0),
            "#38bdf8",
            "Incident Ray"
        )

        self._draw_ray(
            (0, 0),
            reflected_end,
            "#f97316",
            "Reflected Ray"
        )

        self.axes.scatter(
            0,
            0,
            color="#f8fafc",
            s=35,
            zorder=5
        )

        self.axes.legend(
            loc="upper right",
            facecolor="#1e293b",
            labelcolor="white",
            fontsize=9
        )

        self.figure.tight_layout()
        self.canvas.draw_idle()

    def draw_refraction(
        self,
        n1: float,
        n2: float,
        incident_angle: float
    ):
        """Draw incident, reflected, and refracted rays."""

        tir = is_total_internal_reflection(
            n1,
            n2,
            incident_angle
        )

        self._setup_axes("Snell's Law — Refraction")

        incident_rad = math.radians(incident_angle)

        incident_start = (
            -math.sin(incident_rad),
            math.cos(incident_rad)
        )

        reflected_end = (
            math.sin(incident_rad),
            math.cos(incident_rad)
        )

        # Incident ray
        self._draw_ray(
            incident_start,
            (0, 0),
            "#38bdf8",
            "Incident Ray"
        )

        # Reflected ray
        self._draw_ray(
            (0, 0),
            reflected_end,
            "#f97316",
            "Reflected Ray"
        )

        if not tir:
            refracted_angle = calculate_snells_law(
                n1,
                n2,
                incident_angle
            )

            refracted_rad = math.radians(refracted_angle)

            refracted_end = (
                math.sin(refracted_rad),
                -math.cos(refracted_rad)
            )

            self._draw_ray(
                (0, 0),
                refracted_end,
                "#22c55e",
                "Refracted Ray"
            )

        else:
            self.axes.text(
                0,
                -0.65,
                "TOTAL INTERNAL REFLECTION",
                color="#ef4444",
                fontsize=11,
                fontweight="bold",
                ha="center"
            )

        self.axes.text(
            -1.1,
            0.95,
            f"n₁ = {n1:.3f}",
            color="#f8fafc",
            fontsize=10
        )

        self.axes.text(
            -1.1,
            -1.05,
            f"n₂ = {n2:.3f}",
            color="#f8fafc",
            fontsize=10
        )

        self.axes.scatter(
            0,
            0,
            color="#f8fafc",
            s=35,
            zorder=5
        )

        self.axes.legend(
            loc="upper right",
            facecolor="#1e293b",
            labelcolor="white",
            fontsize=9
        )

        self.figure.tight_layout()
        self.canvas.draw_idle()