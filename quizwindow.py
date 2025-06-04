from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from llm_knowledge import LLM_knowledge

class QuizWindow(QWidget):
    def __init__(self, provincename):
        super().__init__()
        self.provincename = provincename
        self.childwidget = QWidget(self)
        self.initUI()
        self.checkwidget = self.CheckWidget('')
        self.checkwidget.hide()
        self.llm = LLM_knowledge()
        self.prompt = f"随机生成一个关于{self.provincename}文化风俗地理的问题，每次都不相同，提供一个正确答案和两个错误答案，千万注意一定要有三个可选答案，不多不少。\
        要求输出是一个字典，并且包含 \"question\"、\"options\" 和 \"correct_answer\" 键。\
        options里面一定是答案的文字本身，而不包含ABC选项，同理correct_answer也是一样\
        千万不得输出字典之外的任何内容"
        self.waitlabel = QLabel(self)
        self.waitlabel.setText('问题正在生成中')
        self.waitlabel.setStyleSheet("""
            QLabel{
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        # 添加等待标签到主布局（自动居中）
        self.waitlabel.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.waitlabel)
        main_layout.addWidget(self.childwidget)
        self.make_quiz()

    class CheckWidget(QWidget):
        def __init__(self, txt):
            super().__init__(None)
            # 设置窗口尺寸
            self.setFixedSize(300, 200)
            
            # 创建垂直布局
            layout = QVBoxLayout()
            layout.setContentsMargins(20, 20, 20, 20)  # 设置边距使界面紧凑
            
            # 创建标签
            self.label = QLabel(txt)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 30px;
                }
            """)
            self.label.setWordWrap(True)  # 允许文本换行
            
            # 创建按钮
            self.retry_btn = QPushButton("再来一题")
            self.retry_btn.setFixedSize(120, 40)  # 保持与其他按钮一致的尺寸
            self.retry_btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            
            # 添加控件到布局
            layout.addWidget(self.label)
            layout.addWidget(self.retry_btn, alignment=Qt.AlignCenter)  # 按钮居中
            
            self.setLayout(layout)

    class Worker(QThread):
        finished = pyqtSignal(dict)  # 完成信号

        def __init__(self, user_input, llm):
            super().__init__()
            self.user_input = user_input
            self.llm = llm
        def run(self):
            ai_text = self.llm.response(self.user_input)  # 耗时操作
            self.finished.emit(ai_text)

    def initUI(self):
        self.setWindowTitle("知识问答")
        self.setGeometry(500, 200, 600, 400)
        layout = QVBoxLayout()
            
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True) 
        self.question_label.setStyleSheet("""
            QLabel{
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        self.question_label.setFixedWidth(500)
        layout.addWidget(self.question_label)

        # 显示选项
        self.options_layout = QHBoxLayout()
        self.option_buttons = []
        for _ in range(3):
            button = QPushButton()
            button.setFixedSize(160, 60)
            button.clicked.connect(self.check_answer)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 15px;
                    margin: 5px;
                }
            """)
            self.option_buttons.append(button)
            self.options_layout.addWidget(button)
        layout.addLayout(self.options_layout)
        self.childwidget.setLayout(layout)
        self.childwidget.hide()
        
    def check_answer(self):
        sender = self.sender()
        check = '回答正确'
        if sender.text() != self.quiz_data["correct_answer"]:
            check = f"回答错误！正确答案是：{self.quiz_data['correct_answer']}"
        self.checkwidget = self.CheckWidget(check)
        self.checkwidget.show()
        self.checkwidget.retry_btn.clicked.connect(self.make_quiz)

    def make_quiz(self):
        self.checkwidget.hide()
        self.childwidget.hide()
        self.layout().invalidate() 
        self.waitlabel.show()
        self.worker = self.Worker(self.prompt,self.llm)
        self.worker.finished.connect(self.write_quiz)
        self.worker.start()

    def write_quiz(self,quiz):
        self.prompt = '再生成一个和之前每个问题都不同的问题，一定确保不相同，输出格式照旧'
        self.quiz_data = quiz
        if "question" in self.quiz_data:
            self.question_label.setText(self.quiz_data["question"])
        if "options" in self.quiz_data:
            for i in range(3):
                self.option_buttons[i].setText(self.quiz_data["options"][i])
        self.waitlabel.hide()
        self.childwidget.show()