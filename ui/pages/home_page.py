from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Optik Dashboard")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Scientific tools for optics and photonics."
        )

        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addStretch()