import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                            QTextEdit, QScrollArea, QPushButton, QLineEdit, QVBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QKeyEvent, QFont
import random
from MockingTrip import TravelSimulator

travelTime = "2025.5.1-2025.5.7"
travelcompanion = ""
special_re=""
travelramdom = random.randint(1,5)

class TravelSetOff(QMainWindow):
    def __init__(self,cityname):
        super().__init__()
        self.cityname = cityname
        self.UI()
        self.show()

    def UI(self):
        self.setFixedSize(500, 400)
        self.setWindowTitle("旅行设置")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        

        # 时间输入部分
        time_layout = QVBoxLayout()
        time_label = QLabel("旅行时间：")
        time_label.setFont(QFont("Arial", 14))
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("请输入旅行的天数")
        self.time_input.setFont(QFont("Arial", 12))
        self.time_input.setFixedWidth(300)
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_input)
        main_layout.addLayout(time_layout)

        # 旅伴输入部分
        companion_layout = QVBoxLayout()
        companion_label = QLabel("旅行同伴：")
        companion_label.setFont(QFont("Arial", 14))
        self.companion_input = QLineEdit()
        self.companion_input.setPlaceholderText("你希望和谁一起旅行？")
        self.companion_input.setFont(QFont("Arial", 12))
        self.companion_input.setFixedWidth(300)
        companion_layout.addWidget(companion_label)
        companion_layout.addWidget(self.companion_input)
        main_layout.addLayout(companion_layout)

        #特殊需求输入
        re_layout = QVBoxLayout()
        re_label = QLabel("特殊需求：")
        re_label.setFont(QFont("Arial", 14))
        self.re_input = QLineEdit()
        self.re_input.setPlaceholderText("如果需要特别策划请畅所欲言！")
        self.re_input.setFont(QFont("Arial", 12))
        self.re_input.setFixedWidth(300)
        re_layout.addWidget(re_label)
        re_layout.addWidget(self.re_input)
        main_layout.addLayout(re_layout)

        # 提交按钮
        submit_btn = QPushButton("开始旅行！")
        submit_btn.setFont(QFont("Arial", 14, QFont.Bold))
        submit_btn.setFixedSize(200, 50)
        submit_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(submit_btn, alignment=Qt.AlignCenter)

        # 状态提示
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        # 设置背景

    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def save_settings(self):
        global travelTime, travelcompanion, special_re
        

        travelTime = self.time_input.text()

        travelcompanion = self.companion_input.text().strip()
        
        special_re = self.re_input.text()
        # 保存成功提示
        self.status_label.setStyleSheet("color: green;")
        

        self.next_window = TravelSimulator(self.cityname,travelTime,travelcompanion,special_re)
        self.next_window.show()
        self.hide()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TravelSetOff("name")
    sys.exit(app.exec_())