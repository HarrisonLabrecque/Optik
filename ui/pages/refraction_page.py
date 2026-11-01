from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class RefractionPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Refraction Calculator")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Calculate light refraction using Snell's law."
        )

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addStretch()