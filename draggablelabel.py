from PyQt5.QtWidgets import  QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap

class DraggableLabel(QLabel):
    def __init__(self, name, position, parent=None):
        super().__init__(parent)
        # 初始化时加载图片并设置位置
        image_path = "resources/"+name+".png"
        self.load_image(image_path)
        self.move(position)  # 设置组件初始位置
        self.drag_start_position = QPoint()
        self.is_dragging = False
        

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # 缩放图片并设置尺寸
            self.setAttribute(Qt.WA_TranslucentBackground, True)  # 关键属性
            self.setStyleSheet("background: transparent;")        # 样式表
            scaled_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
            self.setFixedSize(scaled_pixmap.size())  # 关键：调整标签大小到图片尺寸
        else:
            print(f"无法加载图片: {image_path}")

    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()) and event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.is_dragging = True
        else:
            self.is_dragging = False

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() & Qt.LeftButton:
            self.move(self.mapToParent(event.pos() - self.drag_start_position))

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
