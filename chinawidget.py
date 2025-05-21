from PyQt5.QtWidgets import QWidget, QLabel
from provincebutton import ProvinceButton
import json
from aibutton import AIButton

class ChinaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1200, 686)
        self.provinces = {}
        
        with open('resources/data/province.json', 'r', encoding='utf-8') as f:
            dict = json.load(f)

        for item in dict:
            button = ProvinceButton(self, item, dict[item])
            button.mouse_entered.connect(self.highlight_province)  # 连接信号
            button.mouse_left.connect(self.unhighlight_province)
            self.provinces[item] = button
            button.show()

        self.position_label = QLabel("", self)
        self.position_label.setFixedSize(200, 30)  # 足够容纳10个汉字
        self.position_label.move(1200 - 200 - 20, 686 - 30 - 20)  # 右下角坐标计算
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


    def highlight_province(self, name):        
        self.position_label.setText(f"当前位置：{name}")  # 更新文本框内容
        self.provinces[name].set_icon(3)

    def unhighlight_province(self, name):
        self.position_label.setText("当前位置：")
        self.provinces[name].set_icon(self.provinces[name].times)

    def resetprovince(self, name):
        with open('resources/data/province.json','r') as f:
            data = json.load(f)
        self.provinces[name].set_icon(data[name])
        self.provinces[name].times = data[name]
