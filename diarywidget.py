from aibutton import AIButton
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from diaryapp import DiaryApp
from PyQt5.QtWidgets import *
import os, shutil, json

class DiaryWidget(QWidget):
    def __init__(self, province_name, name, turn, pre=None):
        super().__init__(None)
        self.setFixedSize(1200, 686)
        self.cities = []
        self.name = name
        self.province_name = province_name
        self.pre = pre
        self.dir = 'resources/data/'+province_name+name+'/'+str(turn)
        # 渐变背景
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#f5f7fa"))  # 浅灰蓝
        gradient.setColorAt(1, QColor("#c3cfe2"))  # 淡紫色
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # 日记区域
        self.diary = DiaryApp(dir = self.dir, parent=self)
        self.diary.move(100, 25)

        # 添加右侧按钮组（竖排）
        button_width = 150
        button_height = 50
        spacing = 20
        x = 1200 - button_width - 20  # 右侧边距20px

        # 返回按钮
        self.btn_return = QPushButton("返回", self)
        self.btn_return.setFixedSize(button_width, button_height)        
        self.btn_return.clicked.connect(self.onReturnClicked)
        self.btn_return.move(x, 10)

        # 保存按钮
        self.btn_intr = QPushButton("保存", self)
        self.btn_intr.setFixedSize(button_width, button_height)
        self.btn_intr.clicked.connect(self.diary.save_diary)
        self.btn_intr.move(x, 10 + button_height + spacing)

        self.del_intr = QPushButton("删除", self)
        self.del_intr.setFixedSize(button_width, button_height)
        self.del_intr.clicked.connect(self.onDeleteClicked)
        self.del_intr.move(x, 10 + 2 * (button_height + spacing) )

        # 创建AI按钮
        self.aibutton = AIButton(self)
        self.aibutton.move(1100, 540)


    #返回
    def onReturnClicked(self):
        self.hide()
        new = self.pre.new()
        new.show()

    # 删除功能
    def onDeleteClicked(self):
        # 添加确认对话框
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除该日记及其所有内容吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes and os.path.exists(self.dir):
            shutil.rmtree(self.dir)  # 删除整个目录
            self.upd_turn()
            self.onReturnClicked()

    def upd_turn(self):
        province_name = self.province_name
        name = self.name
        list = os.listdir('resources/data/'+ province_name+ name)
        nlist = []
        for i in list:
            try:
                number = int(i)
                nlist.append(number)
            except:
                continue
        with open('resources/data/'+province_name+'.json','r') as f:
            data = json.load(f)
        citys_number = len(data)
        if nlist:
            data[name] = 2
        else:
            data[name] = 0
        with open('resources/data/'+province_name+'.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        sum = 0
        for i in data:
            if data[i] != 0:
                sum += 1
        with open('resources/data/province.json','r') as f:
            data = json.load(f)
        if sum == 0:
            data[province_name] = 0
        elif sum * 5 > citys_number:
            data[province_name] = 2
        else:
            data[province_name] = 1
        with open('resources/data/province.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    a = DiaryWidget('重庆市','江北区')
    a.show()
    sys.exit(app.exec_())