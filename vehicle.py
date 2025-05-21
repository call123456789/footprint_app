import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
import math

class Vehicle(QLabel):
    finished = pyqtSignal()
    def __init__(self,parent,name,pos):
        super().__init__(parent)
        scale_factor = 0.4
        self._pixmap = QPixmap('resources/'+name+'.png')
        scaled_size = self._pixmap.size() * scale_factor
        self._pixmap = self._pixmap.scaled(
            scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 关键属性
        self.setStyleSheet("background: transparent;")        # 样式表
        
        # 创建标签并设置图片
        self.setPixmap(self._pixmap)
        self.setFixedSize(self._pixmap.size())
        
        # 设置初始位置
        self.start_x, self.start_y, self.target_x, self.target_y = pos

        self.move(self.start_x, self.start_y)
        
        # 设置动画参数
        self.current_x = self.start_x
        self.current_y = self.start_y
        self.step = 3  # 每帧移动的像素
        
        # 计算移动方向和角度
        dx = self.target_x - self.start_x
        dy = self.target_y - self.start_y
        
        # 处理从右到左的移动（水平翻转图片）
        if dx < 0:
            transform = QTransform()
            transform.scale(-1, 1)  # 水平翻转
            self._pixmap = self._pixmap.transformed(transform)
            self.setPixmap(self._pixmap)
        
        # 计算移动角度（如果需要旋转）
        if dx != 0 or dy != 0:
            angle = 0
            if dx < 0 and dy == 0:
                angle = 0  # 向左移动
            elif dx > 0 and dy == 0:
                angle = 0    # 向右移动
            elif dx == 0 and dy < 0:
                angle = 270  # 向上移动
            elif dx == 0 and dy > 0:
                angle = 90   # 向下移动
            else:
                # 计算对角线移动角度
                angle = (180 / 3.1415926) * math.atan(dy / dx)
                '''if dx < 0:
                    angle += 180'''
            
            # 应用旋转变换
            transform = QTransform().rotate(angle)
            rotated_pixmap = self._pixmap.transformed(transform, Qt.SmoothTransformation)
            self.setPixmap(rotated_pixmap)
            self.setFixedSize(rotated_pixmap.size())
        
        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # 约60FPS
        
        self.show()
    
    def animate(self):
        dx = self.target_x - self.current_x
        dy = self.target_y - self.current_y
        
        # 计算欧几里得距离
        distance = math.sqrt(dx**2 + dy**2)
        
        # 距离足够近时停止动画
        if distance < self.step:
            self.current_x = self.target_x
            self.current_y = self.target_y
            self.move(self.current_x, self.current_y)
            self.timer.stop()
            self.close()
            self.finished.emit()  # 发射信号
            return
        
        # 归一化方向向量（单位向量）
        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance
            
            # 按比例移动
            self.current_x += direction_x * self.step
            self.current_y += direction_y * self.step
            
            # 强制整数像素坐标
            self.move(int(self.current_x), int(self.current_y))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setGeometry(300, 300, 800, 500)
    bike = Vehicle(parent=widget,name='自行车',pos=(0,0,300,300))
    widget.show()
    sys.exit(app.exec_())    