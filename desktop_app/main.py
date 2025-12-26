"""
Open Textile Intelligence - Desktop Application
Main entry point for the native desktop application.

Usage:
    python main.py

For packaging with PyInstaller:
    pyinstaller --onefile --windowed --name="OpenTextileIntelligence" main.py
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Main application entry point."""

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Open Textile Intelligence")
    app.setOrganizationName("Bahattin Yunus Çetin")
    app.setApplicationVersion("1.0.0")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
