import sys
from PyQt5.QtWidgets import QApplication
from chinawidget import ChinaWidget
from aibutton import AIButton
from chatwindow import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    AIButton.aiwindow = ChatWindow()
    AIButton.aiwindow.hide()
    chinawidget = ChinaWidget()
    chinawidget.show()
    sys.exit(app.exec_())