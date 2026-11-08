
"""Optik v0.3.0: paraxial spherical-mirror ray diagrams.

Coordinate convention
---------------------
Mirror vertex: x = 0; real objects and reflected rays: x < 0.
Concave mirror: f > 0, focus at x = -f.
Convex mirror: f < 0, virtual focus at x = -f > 0.
Real images: x = -di; virtual images: x = -di > 0.

Uses optics.mirrors.calculate_mirror_properties for the physics model.
"""

from __future__ import annotations

from math import isfinite
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from optics.mirrors import calculate_mirror_properties


class MirrorDiagram:
    """Matplotlib figure illustrating ideal paraxial mirror ray construction."""

    def __init__(self, figsize: tuple[float, float] = (9, 5)) -> None:
        self.figure = Figure(figsize=figsize, tight_layout=True)
        self.ax = self.figure.add_subplot(111)
        self.axes = self.ax
        self._last_parameters: tuple[float, float, float] | None = None

    def clear(self) -> None:
        self.ax.clear()
        self._last_parameters = None
        self.figure.canvas.draw_idle() if self.figure.canvas else None

    def save(self, filename: str | Path, dpi: int = 150) -> None:
        self.figure.savefig(filename, dpi=dpi, bbox_inches="tight")

    def draw(
        self,
        focal_length: float,
        object_distance: float,
        object_height: float = 2.0,
    ) -> Figure:
        """Draw a mirror diagram and return its Matplotlib figure.

        Distances and height must use consistent units. Positive object height
        is required. At do=f for a concave mirror, the image is at infinity.
        """
        props = calculate_mirror_properties(focal_length, object_distance)
        f = props.focal_length
        do = props.object_distance

        try:
            ho = float(object_height)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("Object height must be a number.") from exc

        if not isfinite(ho) or ho <= 0:
            raise ValueError(
                "Object height must be finite and greater than zero."
            )

        di = props.image_distance
        infinite_image = not isfinite(di)
        m = float("-inf") if infinite_image else -di / do
        hi = float("-inf") if infinite_image else m * ho

        if not infinite_image and (
            not isfinite(m) or not isfinite(hi)
        ):
            raise ValueError(
                "Calculated image height is outside the supported range."
            )

        ax = self.ax
        ax.clear()

        ax.set_title(
            f"{props.mirror_type} Mirror — {props.image_type} Image"
        )
        ax.set_xlabel("Optical axis (distance units)")
        ax.set_ylabel("Height (distance units)")
        ax.grid(True, alpha=0.18)
        ax.axhline(0, color="0.4", lw=1)

        # Mirror is a vertical segment at the vertex.
        # Subtle bowing identifies the surface, but all
        # principal rays use the paraxial x=0 plane.
        extent = max(
            abs(f),
            do,
            abs(di) if isfinite(di) else 0.0,
            ho,
            1.0,
        )

        yspan = max(
            2.3 * ho,
            abs(hi) * 1.25 if isfinite(hi) else 0.0,
            0.4 * extent,
        )
        yspan = min(yspan, 3.0 * extent)

        ys = [
            (-1 + i / 100) * yspan
            for i in range(201)
        ]

        curvature = 0.06 * min(abs(f), extent)

        # Concave surface opens toward the object (left).
        # Convex surface opens toward the right.
        sign = 1 if f > 0 else -1

        xs = [
            sign * curvature * (y / yspan) ** 2
            for y in ys
        ]

        ax.plot(
            xs,
            ys,
            color="steelblue",
            lw=3,
            label="Mirror",
        )
        ax.plot(
            0,
            0,
            marker="o",
            color="black",
            markersize=4,
        )

        # F and C are physically in front of concave
        # mirrors and behind convex mirrors.
        fx, cx = -f, -2 * f

        ax.scatter(
            [fx, cx],
            [0, 0],
            color="purple",
            zorder=5,
            s=26,
        )

        ax.annotate(
            "F",
            (fx, 0),
            xytext=(0, -17),
            textcoords="offset points",
            ha="center",
        )

        ax.annotate(
            "C",
            (cx, 0),
            xytext=(0, -17),
            textcoords="offset points",
            ha="center",
        )

        ox, oy = -do, ho

        ax.annotate(
            "",
            xy=(ox, oy),
            xytext=(ox, 0),
            arrowprops={
                "arrowstyle": "-|>",
                "color": "forestgreen",
                "lw": 2.5,
            },
        )

        ax.text(
            ox,
            oy + 0.06 * yspan,
            "Object",
            color="forestgreen",
            ha="center",
        )

        if not infinite_image:
            ix = -di

            ax.annotate(
                "",
                xy=(ix, hi),
                xytext=(ix, 0),
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": "darkorange",
                    "lw": 2.5,
                },
            )

            ax.text(
                ix,
                hi + (
                    0.06 * yspan
                    if hi >= 0
                    else -0.10 * yspan
                ),
                "Image",
                color="darkorange",
                ha="center",
            )

        # Ray 1: parallel to optical axis, striking
        # the mirror at (0, ho).
        #
        # Reflected slope: ho / f.
        #
        # Ray 2: from object tip to mirror vertex.
        #
        # Reflected slope: ho / do.
        #
        # Their intersection is (-di, hi).

        hit1 = (0.0, ho)
        hit2 = (0.0, 0.0)

        ax.plot(
            [ox, hit1[0]],
            [oy, hit1[1]],
            color="crimson",
            lw=1.8,
        )

        ax.plot(
            [ox, hit2[0]],
            [oy, hit2[1]],
            color="royalblue",
            lw=1.8,
        )

        # Reflected rays extend to the left.
        # For virtual images, dashed extensions
        # appear behind the mirror.

        left_reach = max(
            do * 1.25,
            abs(f) * 2.5,
            abs(di) * 1.2 if isfinite(di) else 0,
        )

        left_x = -left_reach

        ax.plot(
            [0, left_x],
            [ho, ho + (ho / f) * left_x],
            color="crimson",
            lw=1.8,
        )

        ax.plot(
            [0, left_x],
            [0, (ho / do) * left_x],
            color="royalblue",
            lw=1.8,
        )

        if not infinite_image and di < 0:
            virtual_x = -di

            ax.plot(
                [0, virtual_x],
                [ho, ho + (ho / f) * virtual_x],
                color="crimson",
                lw=1.5,
                ls="--",
                alpha=0.8,
            )

            ax.plot(
                [0, virtual_x],
                [0, (ho / do) * virtual_x],
                color="royalblue",
                lw=1.5,
                ls="--",
                alpha=0.8,
            )

        if infinite_image:
            ax.text(
                0.02,
                0.98,
                "Image at infinity (parallel reflected rays)",
                transform=ax.transAxes,
                va="top",
                fontsize=9,
            )

        xmin = min(ox, left_x, fx, cx) * 1.12

        xmax = max(
            0.0,
            fx,
            cx,
            -di if isfinite(di) else 0.0,
        ) + 0.15 * extent

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(
            -yspan * 1.15,
            yspan * 1.15,
        )
        ax.set_aspect("auto")

        self._last_parameters = (f, do, ho)

        if self.figure.canvas:
            self.figure.canvas.draw_idle()

        return self.figure


if __name__ == "__main__":
    diagram = MirrorDiagram()

    diagram.draw(
        focal_length=10,
        object_distance=30,
        object_height=5,
    )

    plt.show()
