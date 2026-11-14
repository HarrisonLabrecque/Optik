
"""
Optik - Home Page
Version: 0.4.0

Main application dashboard.

Features:
    - Application introduction
    - Reflection calculator navigation
    - Refraction calculator navigation
    - Thin lens calculator navigation
    - Mirror optics calculator navigation
    - Prism optics and dispersion navigation
    - Responsive feature cards
    - Light and dark themes
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QSizePolicy,
)


# ============================================================
# FEATURE CARD
# ============================================================

class FeatureCard(QFrame):
    """Reusable dashboard card for an Optik calculator."""

    clicked = Signal(int)

    def __init__(
        self,
        title: str,
        description: str,
        page_index: int,
        icon: str = "",
        parent=None,
    ):
        super().__init__(parent)

        self.page_index = page_index

        self.setObjectName("featureCard")
        self.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        self.setMinimumHeight(180)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        if icon:
            icon_label = QLabel(icon)
            icon_label.setObjectName("featureIcon")
            layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setObjectName("featureTitle")

        title_font = title_label.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)

        description_label = QLabel(description)
        description_label.setObjectName(
            "featureDescription"
        )
        description_label.setWordWrap(True)

        open_button = QPushButton("Open Calculator")
        open_button.setObjectName("featureButton")
        open_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        open_button.clicked.connect(
            lambda checked=False:
            self.clicked.emit(self.page_index)
        )

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(open_button)


# ============================================================
# HOME PAGE
# ============================================================

class HomePage(QWidget):
    """Main Optik dashboard."""

    navigate_to = Signal(int)

    HOME = 0
    REFLECTION = 1
    REFRACTION = 2
    LENS = 3
    MIRROR = 4
    PRISM = 5
    SETTINGS = 6

    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_theme = "light"
        self.cards = []

        self._setup_ui()
        self.set_theme(self.current_theme)

    # ========================================================
    # USER INTERFACE
    # ========================================================

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.content = QWidget()
        self.content_layout = QVBoxLayout(
            self.content
        )
        self.content_layout.setContentsMargins(
            30, 30, 30, 30
        )
        self.content_layout.setSpacing(22)

        self._create_header()
        self._create_feature_cards()
        self._create_footer()

        self.content_layout.addStretch()

        self.scroll_area.setWidget(self.content)
        main_layout.addWidget(self.scroll_area)

    # ========================================================
    # HEADER
    # ========================================================

    def _create_header(self):
        self.title_label = QLabel(
            "Welcome to Optik"
        )
        self.title_label.setObjectName("homeTitle")

        title_font = self.title_label.font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.title_label.setFont(title_font)

        self.subtitle_label = QLabel(
            "Explore optics and photonics through "
            "interactive calculations and ray diagrams."
        )
        self.subtitle_label.setObjectName(
            "homeSubtitle"
        )
        self.subtitle_label.setWordWrap(True)

        self.version_label = QLabel(
            "Optik v0.4.0 — Prism Optics & Dispersion"
        )
        self.version_label.setObjectName(
            "homeVersion"
        )

        self.content_layout.addWidget(
            self.title_label
        )
        self.content_layout.addWidget(
            self.subtitle_label
        )
        self.content_layout.addWidget(
            self.version_label
        )

    # ========================================================
    # FEATURE CARDS
    # ========================================================

    def _create_feature_cards(self):
        self.section_label = QLabel(
            "Optical Calculators"
        )
        self.section_label.setObjectName(
            "sectionTitle"
        )

        section_font = self.section_label.font()
        section_font.setPointSize(17)
        section_font.setBold(True)
        self.section_label.setFont(section_font)

        self.content_layout.addWidget(
            self.section_label
        )

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(
            self.cards_container
        )
        self.cards_layout.setSpacing(18)

        features = [
            (
                "Reflection",
                "Calculate reflected angles and explore "
                "the law of reflection.",
                self.REFLECTION,
                "↗",
            ),
            (
                "Refraction",
                "Apply Snell's law, calculate critical "
                "angles, and explore total internal "
                "reflection.",
                self.REFRACTION,
                "↘",
            ),
            (
                "Thin Lenses",
                "Calculate image distance, magnification, "
                "and image formation for converging "
                "and diverging lenses.",
                self.LENS,
                "◉",
            ),
            (
                "Mirror Optics",
                "Explore concave and convex mirrors, "
                "image formation, magnification, "
                "and spherical mirror ray diagrams.",
                self.MIRROR,
                "◖",
            ),
            (
                "Prism Optics & Dispersion",
                "Explore prism refraction, minimum "
                "deviation, wavelength-dependent "
                "refractive index, and visible-light "
                "dispersion.",
                self.PRISM,
                "△",
            ),
        ]

        for index, (
            title,
            description,
            page_index,
            icon,
        ) in enumerate(features):

            card = FeatureCard(
                title=title,
                description=description,
                page_index=page_index,
                icon=icon,
            )

            card.clicked.connect(
                self.navigate_to.emit
            )

            row = index // 2
            column = index % 2

            self.cards_layout.addWidget(
                card,
                row,
                column,
            )

            self.cards.append(card)

        self.cards_layout.setColumnStretch(0, 1)
        self.cards_layout.setColumnStretch(1, 1)

        self.content_layout.addWidget(
            self.cards_container
        )

    # ========================================================
    # FOOTER
    # ========================================================

    def _create_footer(self):
        self.footer_label = QLabel(
            "Optik — Open-Source Optics & "
            "Photonics Software"
        )

        self.footer_label.setObjectName(
            "homeFooter"
        )
        self.footer_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.content_layout.addWidget(
            self.footer_label
        )

    # ========================================================
    # THEMES
    # ========================================================

    def set_theme(self, theme: str):
        """Apply light or dark styling."""

        self.current_theme = (
            "dark"
            if str(theme).lower() == "dark"
            else "light"
        )

        if self.current_theme == "dark":
            background = "#111827"
            card_background = "#1e293b"
            foreground = "#f8fafc"
            muted = "#94a3b8"
            border = "#334155"
            button_background = "#2563eb"
            hover_background = "#1d4ed8"

        else:
            background = "#f8fafc"
            card_background = "#ffffff"
            foreground = "#0f172a"
            muted = "#64748b"
            border = "#e2e8f0"
            button_background = "#2563eb"
            hover_background = "#1d4ed8"

        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {background};
                color: {foreground};
            }}

            QFrame#featureCard {{
                background-color: {card_background};
                border: 1px solid {border};
                border-radius: 12px;
            }}

            QLabel#homeTitle {{
                font-size: 26px;
                font-weight: bold;
            }}

            QLabel#homeSubtitle {{
                color: {muted};
                font-size: 13px;
            }}

            QLabel#homeVersion {{
                color: {button_background};
                font-weight: bold;
            }}

            QLabel#featureTitle {{
                font-size: 15px;
                font-weight: bold;
                background: transparent;
            }}

            QLabel#featureDescription {{
                color: {muted};
                background: transparent;
            }}

            QLabel#featureIcon {{
                font-size: 25px;
                color: {button_background};
                background: transparent;
            }}

            QPushButton#featureButton {{
                background-color: {button_background};
                color: white;
                border: none;
                border-radius: 7px;
                padding: 10px;
                font-weight: bold;
            }}

            QPushButton#featureButton:hover {{
                background-color: {hover_background};
            }}

            QLabel#homeFooter {{
                color: {muted};
                font-size: 11px;
            }}
            """
        )


# ============================================================
# STANDALONE PREVIEW
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = HomePage()
    window.setWindowTitle(
        "Optik v0.4.0 - Home"
    )
    window.resize(1000, 750)
    window.show()

    sys.exit(app.exec())
