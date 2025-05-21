from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, QPoint
from draggablelabel import DraggableLabel
from vehicle import Vehicle
from llm import LLM
from prompt import *

class SpotWidget(QWidget):
    def __init__(self, parent=None, spotname="", pre=None):
        super().__init__(parent)
        self.resize(1200, 686)
        self.cities = [] 
        self.spotname = spotname
        self.pre = pre
        self.labels = []
        self.vehicles = []

        # 修改左侧窗口的创建部分，确保正确显示
        self.left_widget = QWidget(self)
        self.left_widget.setGeometry(10, 10, 1000, 666)
        self.left_widget.setStyleSheet("background-color: white;")

        # 按钮参数
        button_width = 150
        button_height = 50
        x = 1200 - button_width - 20  # 右侧边距20px

        # 返回按钮
        self.btn_return = QPushButton("返回", self)
        self.btn_return.setFixedSize(button_width, button_height)        
        self.btn_return.clicked.connect(self.onReturnClicked)
        self.btn_return.move(x, 10)

        # 替换组件创建部分
        self.input_box = QTextEdit(self)
        self.input_box.setFixedSize(button_width, 200)  # 扩展高度
        self.input_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # 设置对齐
        self.input_box.move(x, 100)

        # 构建行程按钮
        self.btn_build = QPushButton("构建行程", self)
        self.btn_build.setFixedSize(button_width, button_height)
        self.btn_build.clicked.connect(self.onBuildClicked)
        self.btn_build.move(x, 350)  # 放在输入框下方

        # 演示按钮（下移避免遮挡）
        self.btn_show = QPushButton("演示行程", self)
        self.btn_show.setFixedSize(button_width, button_height)
        self.btn_show.clicked.connect(self.onShowClicked)
        self.btn_show.move(x, 400)  

        self.vehicle_queue = []  # 存储待执行的动画任务
        self.current_vehicle = None  # 当前正在执行的动画

    def onBuildClicked(self):
        # 使用 toPlainText() 获取多行文本内容
        input_content = self.input_box.toPlainText()
        for i in self.labels:
            i.close()
        self.labels.clear()
        self.vehicles.clear()
        agent = LLM(task = sys_prompt)
        agent.add("旅行行程如下：\n" + input_content)
        res1 = agent.response(prompt1)
        print(res1)
        list = res1.split('\n')
        list.pop()
        for j in list:
            i = j.split(' ')
            self.labels.append(DraggableLabel(
                parent=self.left_widget, position=QPoint(int(i[1]),int(i[2])), name=i[0]))
        for i in self.labels:
            i.show()
        res2 = agent.response(prompt2)
        print(res2)
        self.vehicles = res2.split('\n')
    # 保留原有返回逻辑
    def onReturnClicked(self):
        self.hide()
        self.pre.show()
    
    def onShowClicked(self):
        self.vehicle_queue = list(enumerate(self.vehicles))  # 转换为队列
        self._start_next_animation()  # 触发第一个动画

    def _start_next_animation(self):
        if not self.vehicle_queue:
            return  # 队列为空，结束

        i, vehicle = self.vehicle_queue.pop(0)  # 取出第一个任务
        pos1 = self.labels[i].pos()
        pos2 = self.labels[(i+1) % len(self.vehicles)].pos()
        
        # 创建 Vehicle 实例
        self.current_vehicle = Vehicle(
            parent=self.left_widget, 
            name=vehicle.strip(), 
            pos=(pos1.x(), pos1.y(), pos2.x(), pos2.y())
        )
        
        # 连接动画结束信号到下个动画启动
        self.current_vehicle.finished.connect(self._start_next_animation)