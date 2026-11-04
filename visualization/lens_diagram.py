"""
Optik — Thin Lens Ray Diagram
Version: 0.2.0

Visualizes:
    - Converging lenses
    - Diverging lenses
    - Real and virtual images
    - Object and image positions
    - Principal optical rays
    - Focal points
    - Image orientation and magnification

Sign convention:
    f > 0: Converging lens
    f < 0: Diverging lens

    do > 0: Real object
    di > 0: Real image
    di < 0: Virtual image

    m = -di / do

Dependencies:
    matplotlib
"""

import math

import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.axes import Axes

from optics.thin_lens import calculate_image_distance
from optics.magnification import calculate_magnification


class LensDiagram:
    """
    Generate ray diagrams for ideal thin lenses.

    The lens is positioned at x = 0.

    Objects are positioned to the left of the lens.
    Positive image distances appear to the right.
    Negative image distances appear to the left.
    """

    def __init__(
        self,
        figsize: tuple[float, float] = (10, 6),
    ) -> None:

        self.figure = Figure(figsize=figsize)

        self.ax: Axes = self.figure.add_subplot(111)

        self.focal_length: float | None = None
        self.object_distance: float | None = None
        self.object_height: float | None = None

        self.image_distance: float | None = None
        self.image_height: float | None = None
        self.magnification: float | None = None

    # ============================================================
    # VALIDATION
    # ============================================================

    @staticmethod
    def _validate_inputs(
        focal_length: float,
        object_distance: float,
        object_height: float,
    ) -> None:

        values = {
            "Focal length": focal_length,
            "Object distance": object_distance,
            "Object height": object_height,
        }

        for name, value in values.items():

            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"{name} must be a number."
                )

            if not math.isfinite(value):
                raise ValueError(
                    f"{name} must be finite."
                )

        if focal_length == 0:
            raise ValueError(
                "Focal length cannot be zero."
            )

        if object_distance <= 0:
            raise ValueError(
                "Object distance must be positive."
            )

        if object_height <= 0:
            raise ValueError(
                "Object height must be positive."
            )

    # ============================================================
    # CALCULATIONS
    # ============================================================

    def calculate(
        self,
        focal_length: float,
        object_distance: float,
        object_height: float,
    ) -> None:
        """
        Calculate the image position and magnification.
        """

        self._validate_inputs(
            focal_length,
            object_distance,
            object_height,
        )

        image_distance = calculate_image_distance(
            focal_length,
            object_distance,
        )

        self.focal_length = float(focal_length)
        self.object_distance = float(object_distance)
        self.object_height = float(object_height)

        self.image_distance = float(image_distance)

        if math.isinf(image_distance):
            self.magnification = math.inf
            self.image_height = math.inf

        else:
            self.magnification = calculate_magnification(
                image_distance,
                object_distance,
            )

            self.image_height = (
                self.magnification * object_height
            )

    # ============================================================
    # AXES
    # ============================================================

    def _setup_axes(self) -> None:
        """
        Configure the optical axis and plot limits.
        """

        assert self.focal_length is not None
        assert self.object_distance is not None
        assert self.object_height is not None
        assert self.image_distance is not None
        assert self.image_height is not None

        self.ax.clear()

        f = abs(self.focal_length)
        do = self.object_distance
        di = self.image_distance

        if math.isfinite(di):

            horizontal_extent = max(
                f * 2.5,
                do * 1.3,
                abs(di) * 1.3,
            )

        else:

            horizontal_extent = max(
                f * 3,
                do * 2,
            )

        if math.isfinite(self.image_height):

            vertical_extent = max(
                self.object_height * 2,
                abs(self.image_height) * 1.5,
                1.0,
            )

        else:

            vertical_extent = max(
                self.object_height * 3,
                1.0,
            )

        self.ax.set_xlim(
            -horizontal_extent,
            horizontal_extent,
        )

        self.ax.set_ylim(
            -vertical_extent,
            vertical_extent,
        )

        self.ax.axhline(
            0,
            color="gray",
            linewidth=1,
            linestyle="-",
        )

        self.ax.axvline(
            0,
            color="black",
            linewidth=1,
            linestyle="-",
        )

        self.ax.set_aspect(
            "auto",
        )

        self.ax.set_xlabel(
            "Distance from Lens"
        )

        self.ax.set_ylabel(
            "Height"
        )

        self.ax.grid(
            True,
            linestyle=":",
            alpha=0.3,
        )

    # ============================================================
    # LENS
    # ============================================================

    def _draw_lens(self) -> None:
        """
        Draw the ideal thin lens.
        """

        assert self.focal_length is not None

        ymin, ymax = self.ax.get_ylim()

        lens_height = max(
            abs(ymin),
            abs(ymax),
        ) * 0.75

        self.ax.plot(
            [0, 0],
            [-lens_height, lens_height],
            color="blue",
            linewidth=3,
            label="Lens",
        )

        if self.focal_length > 0:

            self.ax.plot(
                0,
                lens_height,
                marker="^",
                color="blue",
                markersize=10,
            )

            self.ax.plot(
                0,
                -lens_height,
                marker="v",
                color="blue",
                markersize=10,
            )

        else:

            self.ax.plot(
                0,
                lens_height,
                marker="v",
                color="blue",
                markersize=10,
            )

            self.ax.plot(
                0,
                -lens_height,
                marker="^",
                color="blue",
                markersize=10,
            )

    # ============================================================
    # FOCAL POINTS
    # ============================================================

    def _draw_focal_points(self) -> None:
        """
        Mark focal points on both sides of the lens.
        """

        assert self.focal_length is not None

        f = abs(self.focal_length)

        self.ax.scatter(
            [-f, f],
            [0, 0],
            color="purple",
            marker="o",
            s=35,
            zorder=5,
        )

        self.ax.annotate(
            "F",
            (-f, 0),
            xytext=(0, -18),
            textcoords="offset points",
            ha="center",
        )

        self.ax.annotate(
            "F'",
            (f, 0),
            xytext=(0, -18),
            textcoords="offset points",
            ha="center",
        )

    # ============================================================
    # OBJECT
    # ============================================================

    def _draw_object(self) -> None:
        """
        Draw the object as an upward arrow.
        """

        assert self.object_distance is not None
        assert self.object_height is not None

        x = -self.object_distance
        y = self.object_height

        self.ax.annotate(
            "",
            xy=(x, y),
            xytext=(x, 0),
            arrowprops={
                "arrowstyle": "->",
                "color": "green",
                "linewidth": 2.5,
            },
        )

        self.ax.text(
            x,
            y,
            " Object",
            color="green",
            va="bottom",
        )

    # ============================================================
    # IMAGE
    # ============================================================

    def _draw_image(self) -> None:
        """
        Draw the image as an arrow.

        Real images are red.
        Virtual images are orange.
        """

        assert self.image_distance is not None
        assert self.image_height is not None

        if math.isinf(self.image_distance):
            return

        x = self.image_distance
        y = self.image_height

        color = (
            "red"
            if self.image_distance > 0
            else "orange"
        )

        self.ax.annotate(
            "",
            xy=(x, y),
            xytext=(x, 0),
            arrowprops={
                "arrowstyle": "->",
                "color": color,
                "linewidth": 2.5,
            },
        )

        self.ax.text(
            x,
            y,
            " Image",
            color=color,
            va="bottom" if y >= 0 else "top",
        )

    # ============================================================
    # PRINCIPAL RAYS
    # ============================================================

    def _draw_principal_rays(self) -> None:
        """
        Draw three principal rays.

        Ray 1:
            Parallel to the optical axis, then refracted.

        Ray 2:
            Through the optical center, undeviated.

        Ray 3:
            Directed through the object-side focal point,
            then emerges parallel to the optical axis.

        For a diverging lens, the third ray is directed
        toward the image-side focal point.

        Dashed lines represent virtual extensions.
        """

        assert self.focal_length is not None
        assert self.object_distance is not None
        assert self.object_height is not None
        assert self.image_distance is not None

        f = self.focal_length
        do = self.object_distance
        ho = self.object_height

        x_object = -do

        xmin, xmax = self.ax.get_xlim()

        # --------------------------------------------------------
        # RAY 1 — PARALLEL RAY
        # --------------------------------------------------------

        self.ax.plot(
            [x_object, 0],
            [ho, ho],
            color="red",
            linewidth=1.5,
        )

        # After refraction:
        # y = ho * (1 - x / f)

        y_right = ho * (1 - xmax / f)

        self.ax.plot(
            [0, xmax],
            [ho, y_right],
            color="red",
            linewidth=1.5,
        )

        # --------------------------------------------------------
        # RAY 2 — OPTICAL CENTER
        # --------------------------------------------------------

        # Straight ray from the object tip through the origin.
        y_right_center = -ho * xmax / do

        self.ax.plot(
            [x_object, xmax],
            [ho, y_right_center],
            color="green",
            linewidth=1.5,
        )

        # --------------------------------------------------------
        # RAY 3 — FOCAL RAY
        # --------------------------------------------------------

        # At do == f, the ray directed through the
        # object-side focal point is parallel to the lens
        # plane, so this construction is omitted.

        denominator = do - f

        if not math.isclose(
            denominator,
            0.0,
            abs_tol=1e-12,
        ):

            # Height where the incoming ray meets the lens.
            y_lens = -ho * f / denominator

            self.ax.plot(
                [x_object, 0],
                [ho, y_lens],
                color="purple",
                linewidth=1.5,
            )

            self.ax.plot(
                [0, xmax],
                [y_lens, y_lens],
                color="purple",
                linewidth=1.5,
            )

        # --------------------------------------------------------
        # VIRTUAL RAY EXTENSIONS
        # --------------------------------------------------------

        if self.image_distance < 0:

            x_virtual = self.image_distance

            # Backward extension of the refracted parallel ray.
            y_virtual_parallel = ho * (
                1 - x_virtual / f
            )

            self.ax.plot(
                [x_virtual, 0],
                [y_virtual_parallel, ho],
                color="red",
                linestyle="--",
                linewidth=1.2,
            )

            # Backward extension of the central ray.
            y_virtual_center = (
                -ho * x_virtual / do
            )

            self.ax.plot(
                [x_virtual, 0],
                [y_virtual_center, 0],
                color="green",
                linestyle="--",
                linewidth=1.2,
            )

    # ============================================================
    # TITLE
    # ============================================================

    def _set_title(self) -> None:

        assert self.focal_length is not None
        assert self.image_distance is not None
        assert self.magnification is not None

        lens_type = (
            "Converging"
            if self.focal_length > 0
            else "Diverging"
        )

        if math.isinf(self.image_distance):

            image_type = "Image at Infinity"
            magnification_text = "Undefined (image at infinity)"

        else:

            image_type = (
                "Real"
                if self.image_distance > 0
                else "Virtual"
            )

            magnification_text = (
                f"{self.magnification:.2f}"
            )

        self.ax.set_title(
            f"{lens_type} Lens — {image_type} Image\n"
            f"Magnification: {magnification_text}"
        )

    # ============================================================
    # PUBLIC DRAW METHOD
    # ============================================================

    def draw(
        self,
        focal_length: float,
        object_distance: float,
        object_height: float = 2.0,
    ) -> Figure:
        """
        Generate a complete thin lens ray diagram.

        Parameters
        ----------
        focal_length : float
            Signed focal length.

        object_distance : float
            Positive distance to the real object.

        object_height : float
            Positive object height.

        Returns
        -------
        matplotlib.figure.Figure
            Generated Matplotlib figure.
        """

        self.calculate(
            focal_length,
            object_distance,
            object_height,
        )

        self._setup_axes()

        self._draw_lens()
        self._draw_focal_points()
        self._draw_object()
        self._draw_image()
        self._draw_principal_rays()
        self._set_title()

        self.figure.tight_layout()

        return self.figure

    # ============================================================
    # CLEAR
    # ============================================================

    def clear(self) -> None:
        """
        Clear the diagram and reset calculated values.
        """

        self.ax.clear()

        self.focal_length = None
        self.object_distance = None
        self.object_height = None

        self.image_distance = None
        self.image_height = None
        self.magnification = None

    # ============================================================
    # SAVE
    # ============================================================

    def save(
        self,
        filename: str,
        dpi: int = 150,
    ) -> None:
        """
        Save the current diagram to an image file.
        """

        self.figure.savefig(
            filename,
            dpi=dpi,
            bbox_inches="tight",
        )


# ============================================================
# STANDALONE DEMONSTRATION
# ============================================================

if __name__ == "__main__":

    diagram = LensDiagram()

    diagram.draw(
        focal_length=10.0,
        object_distance=30.0,
        object_height=4.0,
    )

    plt.show()