"""
Optik — Application Entry Point
Version: 0.1.0

Features:
    - Application initialization
    - Application metadata
    - Default font configuration
    - Persistent Light/Dark theme support
"""

import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow


def main() -> int:
    """Initialize and launch Optik."""

    app = QApplication(sys.argv)

    # Application metadata
    app.setOrganizationName("Optik")
    app.setApplicationName("Optik")
    app.setApplicationVersion("0.1.0")

    # Configure a valid point-sized font.
    app.setFont(QFont("Segoe UI", 10))

    # MainWindow loads the saved Light/Dark stylesheet.
    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())