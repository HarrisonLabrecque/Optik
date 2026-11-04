
"""
Optik — Thin Lens Page
Version: 0.2.0

Features:
    - Thin lens equation calculations
    - Signed magnification
    - Image height
    - Image orientation
    - Image size classification
    - Converging and diverging lenses
    - Interactive Matplotlib ray diagrams
    - Persistent default inputs
"""

import math

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QDoubleSpinBox,
    QMessageBox,
    QSizePolicy,
)

from optics.thin_lens import calculate_image_distance
from optics.magnification import calculate_image_properties

from visualization.lens_diagram import LensDiagram
from visualization.plot_manager import PlotManager


class LensPage(QWidget):
    """
    Thin lens calculation and visualization page.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings("Optik", "Optik")

        self.lens_diagram = LensDiagram()

        self._setup_ui()
        self.load_defaults()

    # ============================================================
    # USER INTERFACE
    # ============================================================

    def _setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # --------------------------------------------------------
        # PAGE HEADER
        # --------------------------------------------------------

        title = QLabel("Thin Lens Optics")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Calculate image formation using the thin lens equation "
            "and visualize principal optical rays."
        )
        description.setObjectName("pageDescription")
        description.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        # --------------------------------------------------------
        # MAIN CONTENT
        # --------------------------------------------------------

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # ========================================================
        # LEFT PANEL
        # ========================================================

        left_panel = QVBoxLayout()
        left_panel.setSpacing(16)

        # --------------------------------------------------------
        # INPUT GROUP
        # --------------------------------------------------------

        input_group = QGroupBox("Lens Parameters")
        input_layout = QFormLayout(input_group)

        input_layout.setSpacing(12)

        # Focal length
        self.focal_length_input = QDoubleSpinBox()
        self.focal_length_input.setRange(-10000.0, 10000.0)
        self.focal_length_input.setDecimals(2)
        self.focal_length_input.setSingleStep(1.0)
        self.focal_length_input.setSuffix(" cm")

        # Object distance
        self.object_distance_input = QDoubleSpinBox()
        self.object_distance_input.setRange(0.01, 10000.0)
        self.object_distance_input.setDecimals(2)
        self.object_distance_input.setSingleStep(1.0)
        self.object_distance_input.setSuffix(" cm")

        # Object height
        self.object_height_input = QDoubleSpinBox()
        self.object_height_input.setRange(0.01, 10000.0)
        self.object_height_input.setDecimals(2)
        self.object_height_input.setSingleStep(0.5)
        self.object_height_input.setSuffix(" cm")

        input_layout.addRow(
            "Focal Length (f):",
            self.focal_length_input,
        )

        input_layout.addRow(
            "Object Distance (dₒ):",
            self.object_distance_input,
        )

        input_layout.addRow(
            "Object Height (hₒ):",
            self.object_height_input,
        )

        self.calculate_button = QPushButton("Calculate Lens")
        self.calculate_button.setObjectName("primaryButton")

        self.calculate_button.clicked.connect(
            self.calculate
        )

        input_layout.addRow(self.calculate_button)

        left_panel.addWidget(input_group)

        # --------------------------------------------------------
        # RESULTS GROUP
        # --------------------------------------------------------

        results_group = QGroupBox("Image Properties")
        results_layout = QVBoxLayout(results_group)
        results_layout.setSpacing(10)

        self.image_distance_result = QLabel(
            "Image Distance: —"
        )

        self.magnification_result = QLabel(
            "Magnification: —"
        )

        self.image_height_result = QLabel(
            "Image Height: —"
        )

        self.orientation_result = QLabel(
            "Orientation: —"
        )

        self.image_size_result = QLabel(
            "Image Size: —"
        )

        self.lens_type_result = QLabel(
            "Lens Type: —"
        )

        for label in (
            self.image_distance_result,
            self.magnification_result,
            self.image_height_result,
            self.orientation_result,
            self.image_size_result,
            self.lens_type_result,
        ):
            label.setObjectName("resultLabel")
            results_layout.addWidget(label)

        left_panel.addWidget(results_group)
        left_panel.addStretch()

        # ========================================================
        # RIGHT PANEL — RAY DIAGRAM
        # ========================================================

        diagram_group = QGroupBox("Thin Lens Ray Diagram")
        diagram_layout = QVBoxLayout(diagram_group)

        self.plot_manager = PlotManager(
            theme=self._get_theme(),
            show_toolbar=True,
        )

        self.plot_manager.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        diagram_layout.addWidget(self.plot_manager)

        # --------------------------------------------------------
        # ASSEMBLE CONTENT
        # --------------------------------------------------------

        content_layout.addLayout(left_panel, 1)
        content_layout.addWidget(diagram_group, 2)

        main_layout.addLayout(content_layout, 1)

    # ============================================================
    # SETTINGS
    # ============================================================

    def _get_theme(self) -> str:
        """
        Read the current Optik theme.
        """

        theme = self.settings.value(
            "appearance/theme",
            "dark",
            type=str,
        )

        if theme not in ("light", "dark"):
            return "dark"

        return theme

    def load_defaults(self):
        """
        Load saved lens input values.
        """

        focal_length = self.settings.value(
            "calculations/lens_focal_length",
            10.0,
            type=float,
        )

        object_distance = self.settings.value(
            "calculations/lens_object_distance",
            30.0,
            type=float,
        )

        object_height = self.settings.value(
            "calculations/lens_object_height",
            4.0,
            type=float,
        )

        self.focal_length_input.setValue(focal_length)
        self.object_distance_input.setValue(object_distance)
        self.object_height_input.setValue(object_height)

        self.calculate()

    def save_defaults(self):
        """
        Save the current lens input values.
        """

        self.settings.setValue(
            "calculations/lens_focal_length",
            self.focal_length_input.value(),
        )

        self.settings.setValue(
            "calculations/lens_object_distance",
            self.object_distance_input.value(),
        )

        self.settings.setValue(
            "calculations/lens_object_height",
            self.object_height_input.value(),
        )

        self.settings.sync()

    # ============================================================
    # CALCULATIONS
    # ============================================================

    def calculate(self):
        """
        Calculate lens properties and update the diagram.
        """

        focal_length = self.focal_length_input.value()
        object_distance = self.object_distance_input.value()
        object_height = self.object_height_input.value()

        try:

            if focal_length == 0:
                raise ValueError(
                    "Focal length cannot be zero."
                )

            # ----------------------------------------------------
            # THIN LENS EQUATION
            # ----------------------------------------------------

            image_distance = calculate_image_distance(
                focal_length,
                object_distance,
            )

            lens_type = (
                "Converging"
                if focal_length > 0
                else "Diverging"
            )

            # ----------------------------------------------------
            # IMAGE AT INFINITY
            # ----------------------------------------------------

            if math.isinf(image_distance):

                self.image_distance_result.setText(
                    "Image Distance: Infinity"
                )

                self.magnification_result.setText(
                    "Magnification: Undefined"
                )

                self.image_height_result.setText(
                    "Image Height: Undefined"
                )

                self.orientation_result.setText(
                    "Orientation: Undefined"
                )

                self.image_size_result.setText(
                    "Image Size: Undefined"
                )

            else:

                # ------------------------------------------------
                # MAGNIFICATION
                # ------------------------------------------------

                result = calculate_image_properties(
                    image_distance=image_distance,
                    object_distance=object_distance,
                    object_height=object_height,
                )

                self.image_distance_result.setText(
                    f"Image Distance: {result.image_distance:.2f} cm"
                )

                self.magnification_result.setText(
                    f"Magnification: {result.magnification:.2f}"
                )

                self.image_height_result.setText(
                    f"Image Height: {result.image_height:.2f} cm"
                )

                self.orientation_result.setText(
                    f"Orientation: {result.orientation}"
                )

                self.image_size_result.setText(
                    f"Image Size: {result.image_size}"
                )

            self.lens_type_result.setText(
                f"Lens Type: {lens_type}"
            )

            # ----------------------------------------------------
            # UPDATE RAY DIAGRAM
            # ----------------------------------------------------

            self.lens_diagram.draw(
                focal_length=focal_length,
                object_distance=object_distance,
                object_height=object_height,
            )

            self.plot_manager.display_diagram(
                self.lens_diagram
            )

            self.save_defaults()

        except (ValueError, ZeroDivisionError) as error:

            QMessageBox.warning(
                self,
                "Lens Calculation Error",
                str(error),
            )

    # ============================================================
    # THEME UPDATE
    # ============================================================

    def update_theme(self, theme: str):
        """
        Update the plotting theme.
        """

        self.plot_manager.apply_theme(theme)
