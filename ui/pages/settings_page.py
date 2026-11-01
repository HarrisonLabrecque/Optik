from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Settings")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Application preferences and configuration."
        )

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addStretch()