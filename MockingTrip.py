import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                            QTextEdit, QScrollArea, QPushButton,
                            QVBoxLayout, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QPoint
from PyQt5.QtGui import QPixmap, QCursor
from tool_LLM import*
import random

luckynumber=random.randint(1,5)
class EncounterWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.draggable = False
        self.expanded = False
        self.drag_position = QPoint()
        self.initUI(text)

    def initUI(self, text):
        # 窗口基础设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 主布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        # 完整模式界面
        self.content_widget = QWidget()
        self.content_widget.setVisible(True)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)  # 增加边距
        
        # 文本显示
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_label.setWordWrap(True)
        self.text_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.text_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #333;
                padding: 10px;
                qproperty-alignment: AlignCenter;
                qproperty-wordWrap: true;
                selection-background-color: #B2D7FF;  
                selection-color: #333;                
            }
        """)
        content_layout.addWidget(self.text_label)

        # 关闭按钮
        self.close_btn = QPushButton("知道了！")
        self.close_btn.setFixedSize(120, 40)
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: #ff4444;
                color: white;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #ff6666;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        content_layout.addWidget(self.close_btn, 0, Qt.AlignHCenter)

        self.content_widget.setLayout(content_layout)
        self.main_layout.addWidget(self.content_widget)

        self.setFixedSize(600, 400)  # 调整尺寸
        
        # 增强阴影效果
        self.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 15px;
                border: 1px solid #eee;
            }
            QWidget::content {
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            }
        """)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 无论是否展开都可拖动
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.draggable = True

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.draggable = False


class TravelSimulator(QMainWindow):

    def __init__(self,cityname,travelTime,travelcompanion,special_re):

        self.cityname=cityname
        self.travelTime=travelTime
        self.travelcompanion=travelcompanion
        self.special_re=special_re
        self.InitInfo="旅行的总时间是"+travelTime+"天，这次旅行是和"+travelcompanion+"一起，旅行的地点是"+cityname
        if luckynumber<=2:
            self.InitInfo+="，接下来的event中你可以给出一些不太愉快的事件，但不要对旅行的安全造成影响。\n"
        else:
            self.InitInfo+="，接下来的event中你要给出有趣且令人开心的事件,但偶尔也可以有很少的曲折。\n"
        
        if(self.special_re!=""):
            self.InitInfo+=("最后"+self.special_re)

        super().__init__()
        self.initUI()
        self.history = []
        self.eventllm=tool_LLM(0.3,self.InitInfo)
        self.dic = {}
        self.btn_send.clicked.connect(self.send_message)
        self.show()
        

    def initUI(self):
        # 窗口基础设置
        self.setFixedSize(1200, 800)
        self.setWindowTitle("模拟旅行")

        # 创建滚动区域
        self.scroll = QScrollArea(self)
        self.scroll.setGeometry(0, 100, 1200, 560)
        self.scroll.setWidgetResizable(True)
        
        # 滚动内容容器
        self.container = QWidget()
        self.scroll.setWidget(self.container)

        # 添加标题
        self.title = QLabel("模拟旅行", self)
        self.title.setGeometry(50, 30, 1100, 60)
        self.title.setStyleSheet("""
            font-family: "Arial";
            font-size: 48px;
            font-weight: bold;
            color: white;
            background-color: rgba(0, 0, 0, 150);
            padding: 10px;
            border-radius: 30px;
        """)

        # 初始化文本框
        self.init_text_boxes()


        # 添加底部输入框
        self.bottom_input = QTextEdit(self)
        self.bottom_input.setGeometry(30,680,1140,100)
        self.bottom_input.setStyleSheet("""
            QTextEdit {
                background-color: rgba(200, 200, 200, 220);
                border: 2px solid #666;
                border-radius: 30px;
                padding: 25px;
                font-size: 18px;
            }
            QTextEdit:focus {
                background-color: rgba(200, 200, 200, 220);
            }
        """)
        self.bottom_input.setPlaceholderText("输入消息...")
        # 发送按钮
        self.btn_send = QPushButton("发送", self)
        self.btn_send.setGeometry(1050, 700, 100, 50)
        self.btn_send.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 25px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    def init_text_boxes(self):
        text_style = """
            QTextEdit {
                background-color: rgba(200, 200, 200, 255);
                border: 2px solid #333;
                border-radius: 20px;
                padding: 15px;
                font-size: 16px;
            }
            QTextEdit:focus {
                background-color: rgba(200, 200, 200, 255);
                border: 2px solid #666;
            }
        """
        # 地点信息框
        self.text_base = QTextEdit(self.container)
        self.text_base.setGeometry(50,20,300,60)
        self.text_base.setStyleSheet(text_style)
        self.text_base.setReadOnly(True)
        self.text_base.setText('地点：'+self.cityname)

        # 时间信息框
        self.text_time = QTextEdit(self.container)
        self.text_time.setGeometry(50,120,300,60)
        self.text_time.setStyleSheet(text_style)
        self.text_time.setReadOnly(True)

        # 场景文本框
        self.text_up = QTextEdit(self.container)
        self.text_up.setGeometry(390, 20, 750, 100)
        self.text_up.setStyleSheet(text_style)
        self.text_up.setReadOnly(True)

        # 输入记录文本框
        self.text_down = QTextEdit(self.container)
        self.text_down.setGeometry(50, 220, 300, 300)
        self.text_down.setStyleSheet(text_style)
        self.text_down.setReadOnly(True)

        # 添加图片显示区域
        self.image_label = QLabel(self.container)
        self.image_label.setGeometry(390, 150, 600, 350)  # 右侧位置
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px solid #333;
                border-radius: 0px;
                background-color: rgba(255, 255, 255, 200);
            }
        """)
        self.image_label.hide()
        # 设置初始背景
        
        # 事件按钮
        self.btn_event = QPushButton("事件", self.container)
        self.btn_event.setGeometry(1050, 500, 100, 50)
        self.btn_event.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;  /* 主红色 */
                color: white;
                border-radius: 25px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FF6666;  /* 悬停浅红色 */
            }
        """)
        self.btn_event.clicked.connect(self.showEncounter)
        self.btn_event.hide()
    def onReturnClicked(self):
        self.close()
    def update_image(self):
        """更新右侧图片显示"""
        try:
            # 加载并处理图片
            pixmap = QPixmap("resources/icon/travel.png")
            if not pixmap.isNull():

                scaled_pixmap = pixmap.scaledToWidth(
                    750, 
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setFixedSize(scaled_pixmap.size())
                self.image_label.show()
        except Exception as e:
            print(f"图片加载失败: {str(e)}")
            self.image_label.hide()


    def showInfo(self):
        Info1=self.dic["time"]
        Info2=self.dic["scene"]
        self.text_time.setText('时间：'+Info1)
        self.text_up.setText(Info2)

    def showEncounter(self):
        self.window = EncounterWindow(
            self.dic["event"]+"\n\n接下来你想要？\n\n"+' / '.join(self.dic["choice"])
            )
        self.window.show()

    class AIWorker(QThread):
        ai_response = pyqtSignal(dict)  # 信号参数：(上方内容, 下方内容)

        def __init__(self, prompt, city, days, companion , eventllm):
            super().__init__()
            self.prompt = prompt
            self.city = city
            self.days = days
            self.companion = companion
            self.eventllm = eventllm


        def run(self):
            try:
                # 调用大模型接口（示例调用） 
                full_response = self.eventllm.response(
                    self.prompt
                )
                self.ai_response.emit(full_response)


            except Exception as e:
                error_msg = f"请求失败：{str(e)}"
                print(error_msg)
            

    def send_message(self):
        """处理消息发送"""
        message = self.bottom_input.toPlainText().strip()
        if not message:
            return
    # 显示用户消息
        self.text_down.append(f"你：{message}\n")
    
    # 清空输入框
        self.bottom_input.clear()
    
    # 创建并启动AI工作线程
        self.ai_thread = self.AIWorker(
            prompt=message,
            city=self.cityname,
            days=self.travelTime,
            companion=self.travelcompanion,
            eventllm=self.eventllm
        )
        self.ai_thread.ai_response.connect(self.handle_ai_response)
        self.ai_thread.start()

    def handle_ai_response(self,full_response):
        self.dic = full_response
        """处理AI响应"""
        self.showInfo()
        
        if 'event' in full_response:
            self.btn_event.show()
        self.update_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TravelSimulator("城市名称",'','','')
    sys.exit(app.exec_())