from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from ui.widgets.sidebar import Sidebar

from ui.pages.home_page import HomePage
from ui.pages.reflection_page import ReflectionPage
from ui.pages.refraction_page import RefractionPage
from ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optik — Optical Engineering")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)

        central = QWidget()
        layout = QHBoxLayout(central)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()

        self.stack = QStackedWidget()

        self.pages = {
            "home": HomePage(),
            "reflection": ReflectionPage(),
            "refraction": RefractionPage(),
            "settings": SettingsPage(),
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

        self.setCentralWidget(central)

        self.sidebar.page_selected.connect(self.change_page)

        self.change_page("home")

    def change_page(self, page_id):

        page = self.pages.get(page_id)

        if page is not None:
            self.stack.setCurrentWidget(page)