import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from llm import LLM

class ChatBubble(QWidget):
    def __init__(self, text, is_user=True):
        super().__init__()
        self.is_user = is_user
        self.setStyleSheet("background: transparent;")
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 使用 QTextEdit 替代 QLabel
        self.bubble = QTextEdit()
        self.bubble.setMarkdown(text)  # 关键设置：解析Markdown
        self.bubble.setReadOnly(True)
        self.bubble.setContentsMargins(12, 8, 12, 8)
        self.bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.bubble.setCursor(Qt.IBeamCursor)

        # 样式设置
        bg_color = '#e3f2fd' if is_user else '#f5f5f5'
        self.bubble.setStyleSheet(f"""
            QTextEdit {{
                background: {bg_color};
                color: black;
                border-radius: 15px;
                font-size: 14px;
                padding: 8px;
                margin: 4px;
                max-width: 600px;
                border: none;
            }}
        """)

        # 尺寸策略优化
        self.bubble.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.MinimumExpanding
        )
        self.bubble.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout.addWidget(self.bubble, alignment=Qt.AlignRight if is_user else Qt.AlignLeft)

    def sizeHint(self):
        # 将文档高度转换为整数
        doc_height = int(self.bubble.document().size().height())
        return QSize(
            min(self.bubble.width() + 80, 600),
            doc_height + 20  # 确保结果为整数
        )
# 新增工作线程类
class Worker(QThread):
    finished = pyqtSignal(str)  # 完成信号

    def __init__(self, user_input, llm):
        super().__init__()
        self.user_input = user_input
        self.llm = llm

    def run(self):
        ai_text = self.llm.response(self.user_input)  # 耗时操作
        self.finished.emit(ai_text)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.llm = LLM()
        self.initUI()
        self.setWindowTitle("AI 助手")
        self.setGeometry(700, 300, 500, 450)
        self.setFixedSize(500, 450) 
        # 新增加载提示项
        self.loading_item = None
        self.loading_bubble = None

    def initUI(self):
        # 简化布局设置
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.chat_area = QListWidget()
        self.chat_area.setStyleSheet("""
            QListWidget { 
                background: white; 
                border-radius: 10px; 
                border: 1px solid #ddd;
            }
        """)
        layout.addWidget(self.chat_area)

        # 输入区域优化
        self.input_field = QLineEdit(placeholderText="输入你的需求...（回车发送）")
        self.input_field.returnPressed.connect(self.send_message)
        self.new_chat_btn = QPushButton("新对话", clicked=self.new_chat)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.new_chat_btn)

        layout.addLayout(input_layout)

    def send_message(self):
        if text := self.input_field.text().strip():
            self.add_message(text, True)
            self.input_field.clear()
            self.show_loading()  # 显示加载提示
            
            # 创建工作线程
            self.worker = Worker(text, self.llm)
            self.worker.finished.connect(self.handle_response)
            self.worker.start()

    def add_message(self, text, is_user):
        item = QListWidgetItem()
        bubble = ChatBubble(text, is_user)
        self.chat_area.addItem(item)
        self.chat_area.setItemWidget(item, bubble)
        self.chat_area.scrollToBottom()
        QTimer.singleShot(50, lambda: item.setSizeHint(bubble.sizeHint()))
        return item

    def show_loading(self):
        """显示加载动画"""
        self.loading_item = self.add_message("⏳ AI正在思考中...", False)

    def handle_response(self, ai_text):
        """处理响应结果"""
        # 移除加载提示
        if self.loading_item:
            self.chat_area.takeItem(self.chat_area.row(self.loading_item))
        
        # 添加真实回复
        self.add_message(ai_text, False)

    def new_chat(self):
        """清空所有聊天记录"""
        self.chat_area.clear()     # 清除所有气泡
        self.input_field.clear()   # 清空输入框
        self.loading_item = None   # 重置加载状态
        self.llm = LLM()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())