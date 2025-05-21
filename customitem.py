import sys, os, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from diarywidget import DiaryWidget

class CustomItem(QWidget):
    def __init__(self, province_name, name, turn, parent=None):
        super().__init__(parent)
        # 设置长方形边框
        self.setStyleSheet("""
            border: 1px solid gray; 
            margin: 5px;
            background-color: #FFF8DC;  /* 淡黄色 */
        """)
        self.parent = parent
        self.province_name = province_name
        self.turn = turn
        self.name = name
        # 主水平布局
        layout = QHBoxLayout()
        layout.setSpacing(0)  # 关键设置：消除部件间距
        layout.setContentsMargins(0, 0, 0, 0)  # 消除布局边距

        dir = 'resources/data/'+province_name +name+'/'+str(turn)
        # 图片部分
        image_label = QLabel()
        picture_name = 'resources/icon/无图片.png'
        exit = os.path.exists(dir)
        if exit:
            with open(dir+'/info.json') as f:
                words = json.load(f)
            if words['images']:
                picture_name = words['images'][0]
        pixmap = QPixmap(picture_name)
        image_label.setPixmap(pixmap.scaled(70, 60))
        image_label.setFixedSize(70, 60)
        layout.addWidget(image_label)
        
        # 文字部分
        if exit:
            with open(dir+'/info.json') as f:
                words = json.load(f)
            text_label = QLabel("时间："  +words['time']+ "\n地点："+words["location"])
        else:
            text_label = QLabel("待添加")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFixedHeight(60)
        layout.addWidget(text_label, stretch=1)
        
        # 按钮部分
        if exit:
            self.button = QPushButton("查看\n详情")
        else:
            self.button = QPushButton("点此\n添加")
        self.button.setStyleSheet("""
            QPushButton {
                min-width: 48px;
                min-height: 48px;
                margin: 0;  /* 消除按钮外边距 */
                padding: 0; /* 消除按钮内边距 */
            }
        """)
        self.button.setFixedHeight(48)
        self.button.clicked.connect(self.button_clicked)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def button_clicked(self):
        self.son = DiaryWidget(name = self.name, province_name = self.province_name
                               ,pre = self.parent, turn = self.turn)
        self.son.show()
        self.parent.hide()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 设置主窗口尺寸
        self.setGeometry(100, 100, 800, 600)  # 位置(100,100) 尺寸800x600
        self.setWindowTitle('项目列表')
                # 返回按钮
        self.btn_return = QPushButton("返回", self)
        self.btn_return.setFixedSize(100,20)        
        self.btn_return.move(600, 50)
        self.initUI()

    def initUI(self):
        # 主布局容器（替代QMainWindow的centralWidget）
        main_layout = QVBoxLayout(self)  # 关键点1：直接设置主布局
        main_layout.setContentsMargins(100, 100, 100, 100)  # 窗口边距

        # 滚动区域层（主体内容）
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)  # 新增样式表设置
        scroll.viewport().setStyleSheet("background: transparent;")
        
        # 内容容器配置
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)

        province_name = '重庆市'
        name = '江北区'
        list = os.listdir('resources/data/'+province_name+name)
        nlist = [int(i) for i in list]
        if nlist:
            nlist.append(max(nlist) + 1)
        else:
            nlist.append(1)
        for i in nlist:
            item = CustomItem(name = province_name+name, turn = i)
            content_layout.addWidget(item, alignment=Qt.AlignTop)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)  # 关键点2：直接添加滚动区域到主布局

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())