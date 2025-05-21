from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPoint

class AIButton(QLabel):
    aiwindow = None
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.dragging = False
        self.offset = QPoint()
        
        # 加载图像，替换为你的图像路径
        pixmap = QPixmap("resources/icon/AI.png")    
        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)
        self.setFixedSize(scaled_pixmap.size()) 
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            self.mouse_press_pos = event.globalPos()  # 记录按下位置
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            # 判断是否为点击（移动距离小于5像素视为点击）
            if (event.globalPos() - self.mouse_press_pos).manhattanLength() < 5:
                self.aiwindow.show()
                self.aiwindow.raise_()  # 将窗口提升到堆叠顺序顶部
                self.aiwindow.activateWindow()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToParent(event.pos() - self.offset))
            event.accept()
            