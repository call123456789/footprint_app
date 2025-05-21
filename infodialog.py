from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
import json
from PyQt5.QtCore import Qt

class InfoDialog(QDialog):
    def __init__(self, province_name, name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{name}介绍")
        self.setFixedSize(500, 400)  # 增大窗口尺寸
        
        layout = QVBoxLayout()
        
        # 从JSON文件读取介绍信息
        with open(f'resources/info/{province_name}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            intro = data.get(name, "## 信息暂未收录\n\n请稍后再试")
        
        # 使用与 ChatBubble 一致的 Markdown 渲染方式
        self.text_edit = QTextEdit()
        self.text_edit.setMarkdown(intro)  # 关键设置：解析Markdown
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                line-height: 1.6;
                border: none;
                background: #f8f9fa;
                padding: 12px;
            }
        """)
        self.text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background: #0078d4;
                color: white;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover { background: #006cbd; }
        """)
        
        layout.addWidget(self.text_edit)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)
        self.setLayout(layout)