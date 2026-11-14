
"""
Optik - Home Page Unit Tests
Version: 0.4.0

Tests:
    - HomePage initialization
    - Application version
    - Page navigation constants
    - FeatureCard initialization
    - FeatureCard click signals
    - Five calculator cards
    - Dashboard navigation
    - Light and dark themes
    - Theme normalization
    - Dashboard layout
    - Widget visibility
"""

from __future__ import annotations

import pytest

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QGridLayout,
    QScrollArea,
)

from ui.pages.home_page import (
    HomePage,
    FeatureCard,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def page(qtbot):
    """Create and register a HomePage instance."""

    widget = HomePage()
    qtbot.addWidget(widget)

    widget.show()

    return widget


@pytest.fixture
def feature_card(qtbot):
    """Create and register an individual FeatureCard."""

    card = FeatureCard(
        title="Test Calculator",
        description="A test feature card.",
        page_index=1,
        icon="◉",
    )

    qtbot.addWidget(card)

    card.show()

    return card


# ============================================================
# HOMEPAGE INITIALIZATION
# ============================================================

class TestHomePageInitialization:

    def test_home_page_creation(self, page):
        assert isinstance(page, HomePage)

    def test_default_theme(self, page):
        assert page.current_theme == "light"

    def test_home_title(self, page):
        assert page.title_label.text() == "Welcome to Optik"

    def test_subtitle_exists(self, page):
        assert isinstance(page.subtitle_label, QLabel)

        assert "optics and photonics" in (
            page.subtitle_label.text().lower()
        )

    def test_application_version(self, page):
        assert "v0.4.0" in page.version_label.text()

    def test_prism_version_description(self, page):
        assert "Prism Optics" in page.version_label.text()

    def test_section_title(self, page):
        assert page.section_label.text() == (
            "Optical Calculators"
        )

    def test_footer(self, page):
        assert "Open-Source" in page.footer_label.text()


# ============================================================
# PAGE CONSTANTS
# ============================================================

class TestHomePageConstants:

    @pytest.mark.parametrize(
        "attribute, expected",
        [
            ("HOME", 0),
            ("REFLECTION", 1),
            ("REFRACTION", 2),
            ("LENS", 3),
            ("MIRROR", 4),
            ("PRISM", 5),
            ("SETTINGS", 6),
        ],
    )
    def test_page_indices(
        self,
        attribute,
        expected,
    ):
        assert getattr(HomePage, attribute) == expected


# ============================================================
# FEATURE CARD TESTS
# ============================================================

class TestFeatureCard:

    def test_card_creation(self, feature_card):
        assert isinstance(feature_card, FeatureCard)

    def test_card_object_name(self, feature_card):
        assert feature_card.objectName() == "featureCard"

    def test_card_page_index(self, feature_card):
        assert feature_card.page_index == 1

    def test_card_minimum_height(self, feature_card):
        assert feature_card.minimumHeight() == 180

    def test_card_title(self, feature_card):
        labels = feature_card.findChildren(QLabel)

        assert any(
            label.text() == "Test Calculator"
            for label in labels
        )

    def test_card_description(self, feature_card):
        labels = feature_card.findChildren(QLabel)

        assert any(
            label.text() == "A test feature card."
            for label in labels
        )

    def test_card_icon(self, feature_card):
        labels = feature_card.findChildren(QLabel)

        assert any(
            label.text() == "◉"
            for label in labels
        )

    def test_card_without_icon(self, qtbot):
        card = FeatureCard(
            title="No Icon",
            description="A card without an icon.",
            page_index=2,
        )

        qtbot.addWidget(card)

        icons = card.findChildren(
            QLabel,
            "featureIcon",
        )

        assert len(icons) == 0

    def test_card_button_exists(self, feature_card):
        buttons = feature_card.findChildren(
            QPushButton
        )

        assert len(buttons) == 1

        assert buttons[0].text() == (
            "Open Calculator"
        )

    def test_card_click_emits_page_index(
        self,
        feature_card,
        qtbot,
    ):
        button = feature_card.findChild(
            QPushButton,
            "featureButton",
        )

        assert button is not None

        with qtbot.waitSignal(
            feature_card.clicked,
            timeout=1000,
        ) as signal:
            qtbot.mouseClick(
                button,
                Qt.MouseButton.LeftButton,
            )

        assert signal.args == [1]


# ============================================================
# DASHBOARD FEATURE CARDS
# ============================================================

class TestHomePageFeatureCards:

    def test_five_feature_cards(self, page):
        assert len(page.cards) == 5

    def test_all_cards_are_feature_cards(self, page):
        assert all(
            isinstance(card, FeatureCard)
            for card in page.cards
        )

    def test_feature_card_titles(self, page):
        expected_titles = {
            "Reflection",
            "Refraction",
            "Thin Lenses",
            "Mirror Optics",
            "Prism Optics & Dispersion",
        }

        actual_titles = set()

        for card in page.cards:
            title = card.findChild(
                QLabel,
                "featureTitle",
            )

            assert title is not None
            actual_titles.add(title.text())

        assert actual_titles == expected_titles

    def test_feature_card_page_indices(self, page):
        expected_indices = [1, 2, 3, 4, 5]

        actual_indices = [
            card.page_index
            for card in page.cards
        ]

        assert actual_indices == expected_indices

    def test_prism_card_exists(self, page):
        prism_cards = [
            card
            for card in page.cards
            if card.page_index == page.PRISM
        ]

        assert len(prism_cards) == 1

        prism_card = prism_cards[0]

        title = prism_card.findChild(
            QLabel,
            "featureTitle",
        )

        assert title is not None
        assert "Prism" in title.text()

    def test_prism_card_description(self, page):
        prism_card = next(
            card
            for card in page.cards
            if card.page_index == page.PRISM
        )

        description = prism_card.findChild(
            QLabel,
            "featureDescription",
        )

        assert description is not None

        text = description.text().lower()

        assert "dispersion" in text
        assert "refraction" in text

    def test_cards_have_buttons(self, page):
        for card in page.cards:
            button = card.findChild(
                QPushButton,
                "featureButton",
            )

            assert button is not None

    def test_cards_have_unique_page_indices(self, page):
        indices = [
            card.page_index
            for card in page.cards
        ]

        assert len(indices) == len(set(indices))


# ============================================================
# NAVIGATION TESTS
# ============================================================

class TestHomePageNavigation:

    @pytest.mark.parametrize(
        "page_index",
        [1, 2, 3, 4, 5],
    )
    def test_card_navigation(
        self,
        page,
        qtbot,
        page_index,
    ):
        card = next(
            card
            for card in page.cards
            if card.page_index == page_index
        )

        button = card.findChild(
            QPushButton,
            "featureButton",
        )

        assert button is not None

        with qtbot.waitSignal(
            page.navigate_to,
            timeout=1000,
        ) as signal:
            qtbot.mouseClick(
                button,
                Qt.MouseButton.LeftButton,
            )

        assert signal.args == [page_index]

    def test_prism_navigation(self, page, qtbot):
        prism_card = next(
            card
            for card in page.cards
            if card.page_index == page.PRISM
        )

        button = prism_card.findChild(
            QPushButton,
            "featureButton",
        )

        assert button is not None

        with qtbot.waitSignal(
            page.navigate_to,
            timeout=1000,
        ) as signal:
            qtbot.mouseClick(
                button,
                Qt.MouseButton.LeftButton,
            )

        assert signal.args == [5]


# ============================================================
# LAYOUT TESTS
# ============================================================

class TestHomePageLayout:

    def test_scroll_area_exists(self, page):
        assert isinstance(
            page.scroll_area,
            QScrollArea,
        )

    def test_scroll_area_resizable(self, page):
        assert page.scroll_area.widgetResizable()

    def test_scroll_area_content(self, page):
        assert page.scroll_area.widget() is page.content

    def test_grid_layout_exists(self, page):
        assert isinstance(
            page.cards_layout,
            QGridLayout,
        )

    def test_grid_column_stretch(self, page):
        assert page.cards_layout.columnStretch(0) == 1
        assert page.cards_layout.columnStretch(1) == 1

    def test_card_grid_positions(self, page):
        expected_positions = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (2, 0),
        ]

        for card, (row, column) in zip(
            page.cards,
            expected_positions,
        ):
            index = page.cards_layout.indexOf(card)

            actual_row, actual_column, _, _ = (
                page.cards_layout.getItemPosition(index)
            )

            assert (actual_row, actual_column) == (
                row,
                column,
            )


# ============================================================
# THEME TESTS
# ============================================================

class TestHomePageThemes:

    def test_light_theme(self, page):
        page.set_theme("light")

        assert page.current_theme == "light"
        assert "#f8fafc" in page.styleSheet()

    def test_dark_theme(self, page):
        page.set_theme("dark")

        assert page.current_theme == "dark"
        assert "#111827" in page.styleSheet()

    def test_theme_switching(self, page):
        page.set_theme("dark")
        assert page.current_theme == "dark"

        page.set_theme("light")
        assert page.current_theme == "light"

    def test_invalid_theme_defaults_to_light(self, page):
        page.set_theme("invalid")

        assert page.current_theme == "light"

    def test_case_insensitive_theme(self, page):
        page.set_theme("DARK")

        assert page.current_theme == "dark"

    def test_theme_preserves_cards(self, page):
        page.set_theme("dark")

        assert len(page.cards) == 5

        page.set_theme("light")

        assert len(page.cards) == 5


# ============================================================
# WIDGET VISIBILITY
# ============================================================

class TestHomePageVisibility:

    def test_home_page_visible(self, page):
        assert page.isVisible()

    def test_title_visible(self, page):
        assert page.title_label.isVisible()

    def test_scroll_area_visible(self, page):
        assert page.scroll_area.isVisible()

    def test_feature_cards_exist_in_layout(self, page):
        for card in page.cards:
            assert page.cards_layout.indexOf(card) >= 0

    def test_footer_exists(self, page):
        assert page.footer_label is not None
