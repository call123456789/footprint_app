from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from citybutton import CityButton
from PyQt5.QtCore import Qt
import json
from infodialog import InfoDialog
from aibutton import AIButton
from llm_knowledge import LLM_knowledge
from quizwindow import QuizWindow

class ProvinceWidget(QWidget):
    def __init__(self, parent=None, provincename="",pre=None):
        super().__init__(parent)
        self.setFixedSize(1200, 686)
        self.cities = {} 
        self.provincename = provincename
        self.pre = pre

        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("resources/background/"+provincename+".png").scaled(  # 添加缩放处理
            self.size(), 
            Qt.IgnoreAspectRatio,  # 忽略宽高比
            Qt.SmoothTransformation  # 启用平滑缩放
        )
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        # 添加右侧按钮组（竖排）
        button_width = 150
        button_height = 50
        spacing = 20
        x = 1200 - button_width - 20  # 右侧边距20px

        btns = []
        # 返回按钮
        self.btn_return = QPushButton("返回", self)
        self.btn_return.setFixedSize(button_width, button_height)        
        self.btn_return.clicked.connect(self.onReturnClicked)
        self.btn_return.move(x, 10)
        btns.append(self.btn_return)

        # 介绍按钮
        self.btn_intr = QPushButton("介绍", self)
        self.btn_intr.setFixedSize(button_width, button_height)
        self.btn_intr.clicked.connect(self.onIntroduceClicked)
        self.btn_intr.move(x, 10 + button_height + spacing)
        btns.append(self.btn_intr)

        # 知识问答按钮
        self.btn_quiz = QPushButton("知识问答", self)
        self.btn_quiz.setFixedSize(button_width, button_height) 
        self.btn_quiz.clicked.connect(self.onQuizClicked)
        self.btn_quiz.move(x, 10 + 2*(button_height + spacing))
        btns.append(self.btn_quiz)

        for btn in btns:
            btn.setStyleSheet("""
                QPushButton {
                    border-radius: 15px;
                    border: 2px solid black;
                    color: black;
                    background-color: white;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                    border: 2px solid #404040;
                }
                QPushButton:pressed {
                    background-color: #e0e0e0;
                }
            """)

        # 加载城市按钮逻辑
        with open('resources/data/'+provincename+'.json', 'r', encoding='utf-8') as f:
            dict = json.load(f)

        for item in dict:
            button = CityButton(self, provincename, item, dict[item])
            button.mouse_entered.connect(self.highlight_city)  # 连接信号
            button.mouse_left.connect(self.unhighlight_city)
            self.cities[item] = button
            button.show()

        self.position_label = QLabel("鼠标位置：", self)
        self.position_label.setFixedSize(230, 30)  # 足够容纳10个汉字
        self.position_label.move(1200 - 230 - 20, 686 - 30 - 20)  # 右下角坐标计算
        self.position_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: #333333;
            }
            """)
        self.position_label.setText("当前位置：")  # 初始无内容

        # 创建AI按钮
        self.aibutton = AIButton(self)
        self.aibutton.move(1100, 540)

    # 保留原有返回逻辑
    def onReturnClicked(self):
        self.hide()
        if self.pre:
            self.pre.resetprovince(self.provincename)
            self.pre.show()

    # 介绍功能
    def onIntroduceClicked(self):
        dialog = InfoDialog(self.provincename, self.provincename, self)
        dialog.exec_()
        
    # 知识问答功能
    def onQuizClicked(self):
        self.quiz_window = QuizWindow(self.provincename)
        self.quiz_window.show()

    def highlight_city(self, name):
        self.position_label.setText(f"当前位置：{name}")  # 更新文本框内容
        self.cities[name].set_icon(3)

    def unhighlight_city(self, name):
        self.position_label.setText("当前位置：")
        self.cities[name].set_icon(self.cities[name].times)

    def resetcity(self, cityname):
        with open('resources/data/'+self.provincename+'.json','r',encoding='utf-8') as f:
            data = json.load(f)
        self.cities[cityname].set_icon(data[cityname])
        self.cities[cityname].times = data[cityname]
