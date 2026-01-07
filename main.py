import sys
from PySide6 import QtWidgets, QtCore, QtGui

from chat_bubble import ChatBubble

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = ChatWindow()
    win.resize(CHAT_WIDTH, CHAT_HEIGHT)

    screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
    win.move(
        screen.center().x() - win.width() // 2,
        screen.center().y() - win.height() // 2 + 150,
    )

    win.show()
    sys.exit(app.exec())
