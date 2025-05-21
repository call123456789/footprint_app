from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QBitmap, QIcon
from PyQt5.QtCore import Qt
from citywidget import CityWidget
from PyQt5.QtCore import pyqtSignal

class CityButton(QPushButton):
    mouse_entered = pyqtSignal(str)  # 携带省份名称的信号
    mouse_left = pyqtSignal(str)
    def __init__(self, parent, province_name, name, times= 0):
        super().__init__(parent)
        self.name = name
        self.province_name = province_name
        self.parent = parent
        self.times = times
        self.set_icon(self.times)
        self.clicked.connect(self.onButtonClicked)
    def set_icon(self, times):
        imagename = "resources/"+str(times)+"/" +self.province_name+ self.name+ ".png"
        originalPixmap = QPixmap(imagename)
        # 获取原始图片的宽高
        originalWidth = originalPixmap.width()
        originalHeight = originalPixmap.height()
        # 计算目标高度（保持宽高比）
        if originalWidth*0.7 > originalHeight:
            targetWidth = 920
            targetHeight = int(originalHeight * targetWidth / originalWidth)
        else:
            targetHeight = 600
            targetWidth = int(originalWidth * targetHeight / originalHeight)
        pixmap = originalPixmap.scaled(targetWidth, targetHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setFixedSize(pixmap.size())
        mask = pixmap.createMaskFromColor(Qt.transparent, Qt.MaskInColor)
        self.setMask(mask)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.size())
        self.setStyleSheet("QPushButton{border:none; background:yellow;}")
    def onButtonClicked(self):
        self.parent.hide()
        self.son = CityWidget(pre = self.parent, province_name=self.province_name, 
                              name=self.name, times = self.times)
        self.son.show()

    def enterEvent(self, event):
        self.mouse_entered.emit(self.name)  # 发射进入信号
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.mouse_left.emit(self.name)  # 发射离开信号
        super().leaveEvent(event)
