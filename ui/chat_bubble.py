# type: ignore
import sys
from PySide6 import QtWidgets, QtCore, QtGui

CHAT_WIDTH = 800
CHAT_HEIGHT = 550


# =======================
# 單一聊天氣泡
# =======================
class ChatBubble(QtWidgets.QFrame):
    def __init__(self, text: str, is_user: bool = False):
        super().__init__()

        self.setMaximumWidth(CHAT_WIDTH * 5 / 8)

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {"rgba(180, 200, 255, 150)" if is_user else "rgba(60, 60, 60, 150)"};
                border-radius: 14px;
            }}
            """
        )

        label = QtWidgets.QLabel(text)
        label.setFont(QtGui.QFont("Microsoft JhengHei", 12))
        label.setWordWrap(True)
        label.setStyleSheet("color: white; background-color: rgba(0,0,0,2)")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.addWidget(label)


# =======================
# Alpha Fade（真正扣 alpha）
# =======================
class AlphaFade(QtWidgets.QWidget):
    def __init__(self, *, top: bool, height: int, parent=None):
        super().__init__(parent)
        self.top = top
        self.setFixedHeight(height)

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # 關鍵：DestinationOut 直接吃掉 alpha
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_DestinationOut)

        gradient = QtGui.QLinearGradient(0, 0, 0, self.height())

        if self.top:
            gradient.setColorAt(0.0, QtGui.QColor(0, 0, 0, 255))
            gradient.setColorAt(0.4, QtGui.QColor(0, 0, 0, 255))
            gradient.setColorAt(1.0, QtGui.QColor(0, 0, 0, 0))
        else:
            gradient.setColorAt(0.0, QtGui.QColor(0, 0, 0, 0))
            gradient.setColorAt(0.6, QtGui.QColor(0, 0, 0, 255))
            gradient.setColorAt(1.0, QtGui.QColor(0, 0, 0, 255))

        painter.fillRect(self.rect(), gradient)


# =======================
# 主聊天視窗
# =======================
class ChatWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # ===== 參數 =====
        self.fade_height = 80

        # ===== 視窗本體 =====
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
            | QtCore.Qt.WindowStaysOnBottomHint
        )

        # ======================
        # 半透明面板
        # ======================
        self.panel = QtWidgets.QWidget(self)
        self.panel.setStyleSheet(
            """
            background-color: rgba(0, 0, 0, 20);
            border-radius: 18px;
            """
        )

        # ======================
        # Scroll Area
        # ======================
        self.scroll = QtWidgets.QScrollArea(self.panel)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("QScrollArea { background: transparent; }")

        self.scroll.viewport().installEventFilter(self)

        # ======================
        # 聊天內容容器
        # ======================
        self.container = QtWidgets.QWidget()
        self.container.setStyleSheet("background: transparent;")

        self.vbox = QtWidgets.QVBoxLayout(self.container)
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.vbox.setSpacing(12)

        # 🔑 關鍵修正：為 fade 預留安全距離
        self.vbox.setContentsMargins(
            0,
            self.fade_height / 2,
            0,
            self.fade_height / 2,
        )

        self.scroll.setWidget(self.container)

        # ======================
        # Layout
        # ======================
        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self.panel)

        inner = QtWidgets.QVBoxLayout(self.panel)
        inner.setContentsMargins(16, 16, 16, 16)
        inner.addWidget(self.scroll)

        # ======================
        # Alpha Fade（上下）
        # ======================
        self.top_fade = AlphaFade(
            top=True,
            height=self.fade_height,
            parent=self.panel,
        )
        self.bottom_fade = AlphaFade(
            top=False,
            height=self.fade_height,
            parent=self.panel,
        )

        self.populate_messages()
        self.update_fade_visibility()

    # ======================
    # 固定 fade 位置
    # ======================
    def resizeEvent(self, event):
        self.top_fade.setGeometry(0, 0, self.panel.width(), self.fade_height)
        self.bottom_fade.setGeometry(
            0,
            self.panel.height() - self.fade_height,
            self.panel.width(),
            self.fade_height,
        )

    # ======================
    # 空白區也能滾
    # ======================
    def eventFilter(self, obj, event):
        if obj == self.scroll.viewport() and event.type() == QtCore.QEvent.Wheel:
            self.scroll.verticalScrollBar().event(event)
            return True
        return super().eventFilter(obj, event)

    # ======================
    # 是否需要顯示 fade
    # ======================
    def update_fade_visibility(self):
        bar = self.scroll.verticalScrollBar()
        need = bar.maximum() > 0
        self.top_fade.setVisible(need)
        self.bottom_fade.setVisible(need)

    # ======================
    # 測試訊息
    # ======================
    def populate_messages(self):
        messages = [
            "請你按照設定(System Prompt)的樣式, 思維與風格去翻譯文本. Sy詞, 反義詞, 例句給列出來; 如果是一行文字或多行文字, 把它整句翻譯即可, 翻譯一句話不需要接續輸出同義詞或反義詞. \\ 顯示方式: 適時使用表格作為比較, 排序等用途. 句子或單字的翻譯必須≥2個(正式, 口語, 特殊時機或其他風格), 每個翻譯給出AI輸出答案準確度(幾%). \\ 注意: 你的主要目標是翻譯文本, 我給你資料只是為了方便你翻譯, 不是每一筆資料都要解釋.}",
            "這是真正的 alp請你按照設定(System Pro論章節目次, 最後要總結",
            "靠近邊界會自然消失",
            "請你按照設定(System Prompt)的樣式, 思維與風 格去總結我給的資訊. System Prompt = {目標: 扮演報告者, 說明資料的主題與接下來的討論章節目次, 最後要總結資料. 不要給其他資料. 說明簡短. \\ 語言: 根據資料適時使用繁體中文或英文. \\ 顯示方式: 從我給你的資料選出一個最恰當的題目, 列出目次, 根據目次顯示各項內容, 條列式說明. 不用給我額外資料或網站資訊. \\ 注意: 你的主要目標是解釋提供資訊以外問題, 我給你資料只是為了方便你判斷, 不是每一筆資料都要解釋. 如果資料不足或只是一行敘述, 自行補充資料; 如果我提供的資料夠完整, 用我的資料做報告!!! 須註明那些資料是你自己補充的, 補充資料需要≥2個來源引用, 標明AI輸出答案準確度(幾%).}",
            "請你按照設定(System Prompt)的樣式, 思維與風 格去總結我給的資訊. System Prompt = {目標: 扮演報告者, 說明資料的主題與接下來的討論章節目次, 最後要總結",
            "右邊是請你按照設定(System Promp = {目標: 扮演報告者, 說明資料的主題與接下來的討論章節目次, 最後要總結",
            "這套結構可以設定(System Prompt)的樣式去總結我給的資訊. System Prompt = {目標: 扮演報告者, 說明資料的主題與接下來的討論章節目次, 最後要總結資料. 不要給其他資料. 說明簡短. \\ 語言: 根據資料適時使用繁體中直接接 Ollama",
        ] * 4

        for i, text in enumerate(messages):
            row = QtWidgets.QHBoxLayout()
            bubble = ChatBubble(text, is_user=(i % 2 == 1))

            if i % 2 == 1:
                row.addWidget(bubble, alignment=QtCore.Qt.AlignRight)
            else:
                row.addWidget(bubble, alignment=QtCore.Qt.AlignLeft)

            self.vbox.addLayout(row)

        self.vbox.addStretch()

        QtCore.QTimer.singleShot(
            50,
            lambda: self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            ),
        )


# =======================
# 進入點
# =======================
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
