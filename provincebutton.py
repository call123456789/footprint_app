from PyQt5.QtWidgets import  QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from provincewidget import ProvinceWidget
from PyQt5.QtCore import pyqtSignal

class ProvinceButton(QPushButton):
    mouse_entered = pyqtSignal(str)  # 携带省份名称的信号
    mouse_left = pyqtSignal(str)
    def __init__(self, parent, name, times = 0):
        super().__init__(parent)
        self.name = name
        self.parent = parent
        self.times = times
        self.son = None
        self.set_icon(self.times)
        self.clicked.connect(self.onButtonClicked)
    def set_icon(self, times):
        imagename = "resources/"+str(times)+f"/{self.name}.png"
        originalPixmap = QPixmap(imagename)
        targetSize = (1000, 686)
        pixmap = originalPixmap.scaled(targetSize[0], targetSize[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setFixedSize(pixmap.size())
        mask = pixmap.createMaskFromColor(Qt.transparent, Qt.MaskInColor)
        self.setMask(mask)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.size())
        self.setStyleSheet("QPushButton{border:none; background:yellow;}")
    def onButtonClicked(self):
        if self.son == None:
            self.son = ProvinceWidget(None, self.name, self.parent)
        self.son.show()
        self.parent.hide()

    def enterEvent(self, event):
        self.mouse_entered.emit(self.name)  # 发射进入信号
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.mouse_left.emit(self.name)  # 发射离开信号
        super().leaveEvent(event)

    def update_times(self):
        self.times += 1
        self.set_icon(self.times)
