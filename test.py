from PySide6 import QtWidgets, QtCore, QtGui


class InputBar(QtWidgets.QFrame):
    textSubmitted = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("InputBar")
        self.setStyleSheet(
            """
        QFrame#InputBar {
            background-color: rgba(40, 40, 40, 200);
            border-radius: 16px;
        }
        """
        )

        # ===== 輸入框 =====
        self.edit = QtWidgets.QTextEdit()
        self.edit.setPlaceholderText("輸入訊息，Enter 送出，Shift+Enter 換行")
        self.edit.setFont(QtGui.QFont("Microsoft JhengHei", 12))
        self.edit.setFixedHeight(44)
        self.edit.setStyleSheet(
            """
        QTextEdit {
            background: transparent;
            color: white;
            border: none;
        }
        """
        )

        self.edit.installEventFilter(self)

        # ===== 送出按鈕 =====
        self.send_btn = QtWidgets.QPushButton("➤")
        self.send_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.send_btn.setFixedSize(36, 36)
        self.send_btn.setStyleSheet(
            """
        QPushButton {
            background-color: rgba(90, 90, 90, 180);
            border-radius: 18px;
            color: white;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: rgba(120, 120, 120, 200);
        }
        """
        )

        self.send_btn.clicked.connect(self._emit_text)

        # ===== Layout =====
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 8, 6)
        layout.setSpacing(8)
        layout.addWidget(self.edit)
        layout.addWidget(self.send_btn)

    # ======================
    # Enter / Shift+Enter
    # ======================
    def eventFilter(self, obj, event):
        if obj is self.edit and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                if event.modifiers() & QtCore.Qt.ShiftModifier:
                    return False  # 換行
                else:
                    self._emit_text()
                    return True
        return super().eventFilter(obj, event)

    def _emit_text(self):
        text = self.edit.toPlainText().strip()
        if not text:
            return
        self.textSubmitted.emit(text)
        self.edit.clear()
