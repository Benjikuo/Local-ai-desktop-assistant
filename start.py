# start.py
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize


class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(80, 80)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.button = QPushButton(self)
        self.button.setFixedSize(80, 80)
        self.button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(180, 200, 255, 150);
                border-radius: 40px;
            }
            QPushButton:pressed {
                background-color: #1F5FD6;
            }
        """
        )

        self.button.setIcon(QIcon("image/icon/edit.svg"))
        self.button.setIconSize(QSize(40, 40))

        self.move_to_bottom_right()
        self.button.clicked.connect(self.on_click)

    def move_to_bottom_right(self, margin=30):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - margin
        y = screen.bottom() - self.height() - margin
        self.move(x, y)

    def on_click(self):
        print("Launcher clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec())
