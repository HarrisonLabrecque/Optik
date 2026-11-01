from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


class Sidebar(QWidget):

    page_selected = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        title = QLabel("OPTIK")
        title.setObjectName("sidebarTitle")

        layout.addWidget(title)

        self.buttons = {}

        pages = {
            "Home": "home",
            "Reflection": "reflection",
            "Refraction": "refraction",
            "Settings": "settings",
        }

        for label, page_id in pages.items():

            button = QPushButton(label)
            button.setCheckable(True)

            button.clicked.connect(
                lambda checked=False, p=page_id: self.select_page(p)
            )

            self.buttons[page_id] = button

            layout.addWidget(button)

        layout.addStretch()

        self.select_page("home")

    def select_page(self, page_id):

        for key, button in self.buttons.items():
            button.setChecked(key == page_id)

        self.page_selected.emit(page_id)