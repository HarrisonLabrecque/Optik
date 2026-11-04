
"""
Optik — Home Page
Version: 0.2.0

Features:
    - Welcome dashboard
    - Reflection calculator card
    - Refraction calculator card
    - Thin lens calculator card
    - Quick-start instructions
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QGridLayout,
    QPushButton,
)


class FeatureCard(QFrame):
    """A card describing an Optik feature."""

    def __init__(
        self,
        title: str,
        description: str,
        button_text: str,
        page_name: str,
    ):
        super().__init__()

        self.page_name = page_name

        self.setObjectName("featureCard")
        self.setMinimumHeight(190)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setObjectName("featureTitle")

        description_label = QLabel(description)
        description_label.setObjectName(
            "featureDescription"
        )
        description_label.setWordWrap(True)

        self.open_button = QPushButton(button_text)
        self.open_button.setObjectName("primaryButton")
        self.open_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(self.open_button)


class HomePage(QWidget):
    """Optik application dashboard."""

    def __init__(self):
        super().__init__()

        self._setup_ui()

    def _setup_ui(self):
        """Build the home dashboard."""

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(24)

        # ====================================================
        # WELCOME SECTION
        # ====================================================

        welcome = QLabel("Welcome to Optik")
        welcome.setObjectName("pageTitle")

        subtitle = QLabel(
            "Explore optics and photonics through "
            "interactive calculations and visualization."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(welcome)
        layout.addWidget(subtitle)

        # ====================================================
        # OVERVIEW
        # ====================================================

        overview = QFrame()
        overview.setObjectName("dashboardPanel")

        overview_layout = QVBoxLayout(overview)
        overview_layout.setContentsMargins(
            24, 22, 24, 22
        )
        overview_layout.setSpacing(12)

        overview_title = QLabel(
            "Optics Made Interactive"
        )
        overview_title.setObjectName("sectionTitle")

        overview_text = QLabel(
            "Optik provides scientific tools for understanding "
            "the behavior of light. Calculate reflection and "
            "refraction angles, investigate critical angles, "
            "explore thin lens image formation, and visualize "
            "optical rays in two dimensions."
        )
        overview_text.setWordWrap(True)
        overview_text.setObjectName("bodyText")

        overview_layout.addWidget(overview_title)
        overview_layout.addWidget(overview_text)

        layout.addWidget(overview)

        # ====================================================
        # FEATURE CARDS
        # ====================================================

        features_title = QLabel(
            "Explore Calculators"
        )
        features_title.setObjectName("sectionTitle")

        layout.addWidget(features_title)

        feature_grid = QGridLayout()
        feature_grid.setSpacing(18)

        # Reflection
        self.reflection_card = FeatureCard(
            "Reflection",
            "Explore the law of reflection and visualize "
            "incident and reflected light rays.",
            "Open Reflection Calculator",
            "reflection",
        )

        # Refraction
        self.refraction_card = FeatureCard(
            "Refraction",
            "Apply Snell's law, calculate critical angles, "
            "and investigate total internal reflection.",
            "Open Refraction Calculator",
            "refraction",
        )

        # Thin Lens
        self.lens_card = FeatureCard(
            "Thin Lens",
            "Calculate image distance, magnification, "
            "image height, and orientation using the "
            "thin lens equation. Visualize converging "
            "and diverging lens ray diagrams.",
            "Open Thin Lens Calculator",
            "lens",
        )

        feature_grid.addWidget(
            self.reflection_card, 0, 0
        )
        feature_grid.addWidget(
            self.refraction_card, 0, 1
        )
        feature_grid.addWidget(
            self.lens_card, 1, 0, 1, 2
        )

        layout.addLayout(feature_grid)

        # ====================================================
        # QUICK START
        # ====================================================

        quick_start = QFrame()
        quick_start.setObjectName("dashboardPanel")

        quick_layout = QVBoxLayout(quick_start)
        quick_layout.setContentsMargins(
            24, 22, 24, 22
        )
        quick_layout.setSpacing(12)

        quick_title = QLabel("Quick Start")
        quick_title.setObjectName("sectionTitle")

        instructions = QLabel(
            "1. Select an optical calculator.\n"
            "2. Enter the required parameters.\n"
            "3. Click Calculate.\n"
            "4. Review the results and optical ray diagram."
        )
        instructions.setObjectName("bodyText")
        instructions.setWordWrap(True)

        quick_layout.addWidget(quick_title)
        quick_layout.addWidget(instructions)

        layout.addWidget(quick_start)

        # ====================================================
        # FOOTER
        # ====================================================

        footer = QLabel(
            "Optik v0.2.0  •  Open-Source Optics & Photonics"
        )
        footer.setObjectName("dashboardFooter")
        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(footer)
        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
