from infodialog import InfoDialog
from aibutton import AIButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from customitem import CustomItem
from PyQt5.QtWidgets import *
from MockingTrip import *
from MockingSetOff import *
import os

class CityWidget(QWidget):
    def __init__(self, province_name, name, pre=None, times = 0):
        super().__init__(None)
        self.setFixedSize(1200, 686)
        self.cities = []
        self.name = name
        self.times = times
        self.province_name = province_name
        self.pre = pre

        self.initUI()

        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("resources/background/"+province_name+".png").scaled(  # 添加缩放处理
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

        #模拟旅行按钮
        self.btn_mock = QPushButton("模拟旅行", self)
        self.btn_mock.setFixedSize(button_width, button_height) 
        self.btn_mock.clicked.connect(self.onMockClicked)
        self.btn_mock.move(x, 10 + 2*(button_height + spacing))
        btns.append(self.btn_mock)

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

        # 创建AI按钮
        self.aibutton = AIButton(self)
        self.aibutton.move(1100, 540)

    def initUI(self):
        # 主布局容器（替代QMainWindow的centralWidget）
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(190, 120, 190, 120)  # 窗口边距

        # 滚动区域层（主体内容）
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.viewport().setStyleSheet("background: transparent;")
        
        # 内容容器配置
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)
        list = os.listdir('resources/data/'+self.province_name + self.name)
        nlist = []
        for i in list:
            try:
                number = int(i)
                nlist.append(number)
            except:
                continue
        if nlist:
            nlist.append(max(nlist) + 1)
        else:
            nlist.append(1)
        for i in nlist:
            item = CustomItem(province_name = self.province_name, name = self.name, turn = i, parent=self)
            content_layout.addWidget(item, alignment=Qt.AlignTop)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    #返回
    def onReturnClicked(self):
        self.hide()
        self.pre.resetcity(self.name)
        self.pre.show()

    # 介绍功能
    def onIntroduceClicked(self):
        dialog = InfoDialog(self.province_name, self.name, self)
        dialog.exec_()

    #模拟旅行
    def onMockClicked(self):
        self.travel_window = TravelSetOff(self.province_name+self.name)
        self.travel_window.show()
        CityWidget.show(self)
    
    def new(self):
        a = CityWidget(province_name = self.province_name, name = self.name,
                       pre = self.pre)
        return a