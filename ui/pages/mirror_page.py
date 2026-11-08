
"""
Optik - Mirror Calculator Page
Version: 0.3.0

PySide6 interface for concave and convex spherical mirrors.

Features:
    - Mirror type selection
    - Focal length, object distance, object height
    - Image distance and magnification
    - Image height and orientation
    - Real / virtual image classification
    - Radius of curvature
    - Embedded Matplotlib ray diagram
    - Light and dark themes
"""

from __future__ import annotations

from math import isfinite

from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
    QMessageBox,
    QScrollArea,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from optics.mirrors import calculate_mirror_properties
from visualization.mirror_diagram import MirrorDiagram


class MirrorPage(QWidget):
    """Interactive spherical mirror calculator."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings("Optik", "Optik")
        self.diagram = MirrorDiagram()
        self.current_theme = "light"

        self._setup_ui()
        self._load_settings()
        self.calculate()

    # ---------------------------------------------------------
    # User Interface
    # ---------------------------------------------------------

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(18)

        self._create_header()
        self._create_inputs()
        self._create_results()
        self._create_diagram()

        self.content_layout.addStretch()

        self.scroll_area.setWidget(self.content)
        self.main_layout.addWidget(self.scroll_area)

    def _create_header(self):
        self.title_label = QLabel("Mirror Optics")
        self.title_label.setObjectName("pageTitle")

        font = self.title_label.font()
        font.setPointSize(20)
        font.setBold(True)
        self.title_label.setFont(font)

        self.description_label = QLabel(
            "Calculate image formation using concave "
            "and convex spherical mirrors."
        )
        self.description_label.setWordWrap(True)

        self.content_layout.addWidget(self.title_label)
        self.content_layout.addWidget(self.description_label)

    def _create_inputs(self):
        self.input_group = QGroupBox("Mirror Parameters")
        form = QFormLayout(self.input_group)

        self.mirror_type_combo = QComboBox()
        self.mirror_type_combo.addItems([
            "Concave Mirror",
            "Convex Mirror",
        ])

        self.focal_length_input = self._create_spinbox(
            value=10.0,
            minimum=0.01,
            maximum=100000.0,
        )

        self.object_distance_input = self._create_spinbox(
            value=30.0,
            minimum=0.01,
            maximum=100000.0,
        )

        self.object_height_input = self._create_spinbox(
            value=5.0,
            minimum=0.01,
            maximum=100000.0,
        )

        form.addRow("Mirror Type:", self.mirror_type_combo)
        form.addRow("Focal Length Magnitude:", self.focal_length_input)
        form.addRow("Object Distance:", self.object_distance_input)
        form.addRow("Object Height:", self.object_height_input)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setMinimumHeight(36)
        self.calculate_button.clicked.connect(self.calculate)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_inputs)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.reset_button)

        form.addRow(button_layout)

        self.content_layout.addWidget(self.input_group)

    def _create_spinbox(
        self,
        value: float,
        minimum: float,
        maximum: float,
    ) -> QDoubleSpinBox:
        spinbox = QDoubleSpinBox()
        spinbox.setDecimals(2)
        spinbox.setRange(minimum, maximum)
        spinbox.setSingleStep(1.0)
        spinbox.setValue(value)
        return spinbox

    def _create_results(self):
        self.results_group = QGroupBox("Calculated Results")
        form = QFormLayout(self.results_group)

        self.mirror_type_result = QLabel("—")
        self.image_distance_result = QLabel("—")
        self.radius_result = QLabel("—")
        self.magnification_result = QLabel("—")
        self.image_height_result = QLabel("—")
        self.image_type_result = QLabel("—")
        self.orientation_result = QLabel("—")
        self.image_size_result = QLabel("—")

        form.addRow("Mirror Type:", self.mirror_type_result)
        form.addRow("Image Distance:", self.image_distance_result)
        form.addRow("Radius of Curvature:", self.radius_result)
        form.addRow("Magnification:", self.magnification_result)
        form.addRow("Image Height:", self.image_height_result)
        form.addRow("Image Type:", self.image_type_result)
        form.addRow("Orientation:", self.orientation_result)
        form.addRow("Image Size:", self.image_size_result)

        self.content_layout.addWidget(self.results_group)

    def _create_diagram(self):
        self.diagram_group = QGroupBox("Mirror Ray Diagram")
        layout = QVBoxLayout(self.diagram_group)

        self.canvas = FigureCanvasQTAgg(self.diagram.figure)
        self.canvas.setMinimumHeight(350)

        self.toolbar = NavigationToolbar2QT(
            self.canvas,
            self.diagram_group,
        )

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.content_layout.addWidget(self.diagram_group)

    # ---------------------------------------------------------
    # Calculations
    # ---------------------------------------------------------

    def calculate(self):
        """Calculate mirror properties and update the diagram."""
        try:
            focal_magnitude = self.focal_length_input.value()
            object_distance = self.object_distance_input.value()
            object_height = self.object_height_input.value()

            is_convex = (
                self.mirror_type_combo.currentIndex() == 1
            )

            focal_length = (
                -focal_magnitude
                if is_convex
                else focal_magnitude
            )

            result = calculate_mirror_properties(
                focal_length,
                object_distance,
            )

            image_distance = result.image_distance

            self.mirror_type_result.setText(result.mirror_type)

            self.radius_result.setText(
                f"{result.radius_of_curvature:.2f}"
            )

            self.image_type_result.setText(result.image_type)

            if not isfinite(image_distance):
                self._show_infinite_image()
            else:
                magnification = (
                    -image_distance / object_distance
                )

                image_height = magnification * object_height

                if not (
                    isfinite(magnification)
                    and isfinite(image_height)
                ):
                    raise ValueError(
                        "Calculated image dimensions are "
                        "outside the supported range."
                    )

                self.image_distance_result.setText(
                    f"{image_distance:.2f}"
                )

                self.magnification_result.setText(
                    f"{magnification:.3f}"
                )

                self.image_height_result.setText(
                    f"{image_height:.2f}"
                )

                self.orientation_result.setText(
                    "Upright" if magnification > 0
                    else "Inverted"
                )

                magnitude = abs(magnification)

                if abs(magnitude - 1.0) < 1e-9:
                    image_size = "Same Size"
                elif magnitude > 1.0:
                    image_size = "Enlarged"
                else:
                    image_size = "Reduced"

                self.image_size_result.setText(image_size)

            self.diagram.draw(
                focal_length=focal_length,
                object_distance=object_distance,
                object_height=object_height,
            )

            self._apply_plot_theme()
            self.canvas.draw_idle()
            self._save_settings()

        except (ValueError, OverflowError, ZeroDivisionError) as error:
            QMessageBox.warning(
                self,
                "Mirror Calculation Error",
                str(error),
            )

    def _show_infinite_image(self):
        """Handle an object located at a concave mirror's focus."""
        self.image_distance_result.setText("Infinity")
        self.magnification_result.setText("Undefined")
        self.image_height_result.setText("Undefined")
        self.orientation_result.setText("Not Applicable")
        self.image_size_result.setText("Not Applicable")

    # ---------------------------------------------------------
    # Settings
    # ---------------------------------------------------------

    def _save_settings(self):
        self.settings.setValue(
            "mirror/type",
            self.mirror_type_combo.currentIndex(),
        )
        self.settings.setValue(
            "mirror/focal_length",
            self.focal_length_input.value(),
        )
        self.settings.setValue(
            "mirror/object_distance",
            self.object_distance_input.value(),
        )
        self.settings.setValue(
            "mirror/object_height",
            self.object_height_input.value(),
        )

    def _load_settings(self):
        mirror_type = self.settings.value(
            "mirror/type", 0, type=int
        )

        self.mirror_type_combo.setCurrentIndex(
            mirror_type if mirror_type in (0, 1) else 0
        )

        self.focal_length_input.setValue(
            self.settings.value(
                "mirror/focal_length", 10.0, type=float
            )
        )

        self.object_distance_input.setValue(
            self.settings.value(
                "mirror/object_distance", 30.0, type=float
            )
        )

        self.object_height_input.setValue(
            self.settings.value(
                "mirror/object_height", 5.0, type=float
            )
        )

    def reset_inputs(self):
        """Restore default mirror parameters."""
        self.mirror_type_combo.setCurrentIndex(0)
        self.focal_length_input.setValue(10.0)
        self.object_distance_input.setValue(30.0)
        self.object_height_input.setValue(5.0)
        self.calculate()

    # ---------------------------------------------------------
    # Themes
    # ---------------------------------------------------------

    def set_theme(self, theme: str):
        """Apply the selected application theme."""
        self.current_theme = (
            "dark" if str(theme).lower() == "dark"
            else "light"
        )

        self._apply_plot_theme()
        self.canvas.draw_idle()

    def _apply_plot_theme(self):
        """Update Matplotlib background and text colors."""
        dark = self.current_theme == "dark"

        background = "#182338" if dark else "#ffffff"
        foreground = "#f8fafc" if dark else "#202020"

        self.diagram.figure.set_facecolor(background)
        self.diagram.ax.set_facecolor(background)

        self.diagram.ax.title.set_color(foreground)
        self.diagram.ax.xaxis.label.set_color(foreground)
        self.diagram.ax.yaxis.label.set_color(foreground)

        self.diagram.ax.tick_params(
            axis="both",
            colors=foreground,
        )

        for spine in self.diagram.ax.spines.values():
            spine.set_color(foreground)

        for item in self.diagram.ax.texts:
            if item.get_color() in ("black", "0.0"):
                item.set_color(foreground)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = MirrorPage()
    window.setWindowTitle("Optik v0.3.0 - Mirror Optics")
    window.resize(1100, 850)
    window.show()

    sys.exit(app.exec())
