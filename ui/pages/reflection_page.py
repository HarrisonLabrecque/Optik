from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ReflectionPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Reflection Calculator")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Calculate reflection angles using the law of reflection."
        )

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addStretch()