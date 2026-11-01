import sys

from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow


def main() -> int:

    app = QApplication(sys.argv)

    app.setApplicationName("Optik")
    app.setApplicationVersion("0.1.0")

    stylesheet_path = (
        Path(__file__).resolve().parent
        / "ui"
        / "styles"
        / "main.qss"
    )

    if stylesheet_path.exists():
        app.setStyleSheet(
            stylesheet_path.read_text(encoding="utf-8")
        )

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())