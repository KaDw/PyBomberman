import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyApp(QWidget):
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self,*args,**kwargs)
        self.current_timer = None
        self.layout = QVBoxLayout(self)
        self.button = QPushButton('start timer')
        self.button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.button)

    def start_timer(self):
        if self.current_timer:
            self.current_timer.stop()
            self.current_timer.deleteLater()
        self.current_timer = QTimer()
        self.current_timer.timeout.connect(self.print_hello)
        self.current_timer.setSingleShot(True)
        self.current_timer.start(3000)

    def print_hello(self):
        print('hello')


# Create QApplication and QWidget
qapp = QApplication(sys.argv)
app = MyApp()
app.show()
qapp.exec_()