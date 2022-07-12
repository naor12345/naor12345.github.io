---
title: PyQt5多线程Example
date: 2022-05-23 22:35:42
copyright: false
categories: "PyQt5"
tags: 
    - "PyQt5"
---

**一般地，不会在UI主线程里处理耗时逻辑。需要另外开一个线程。**
示例代码摘自 https://stackoverflow.com/questions/6783194/background-thread-with-qthread-in-pyqt
<!-- more -->
```python
# worker.py
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
import sys

class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)

    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        for i in range(1, 100):
            time.sleep(1)
            self.intReady.emit(i)
        self.finished.emit()


class Form(QWidget):
    def __init__(self):
       super().__init__()
       self.label = QLabel("0")

       # 1 - create Worker and Thread inside the Form
       self.obj = Worker()  # no parent!
       self.thread = QThread()  # no parent!

       # 2 - Connect Worker`s Signals to Form method slots to post data.
       self.obj.intReady.connect(self.onIntReady)

       # 3 - Move the Worker object to the Thread object
       self.obj.moveToThread(self.thread)

       # 4 - Connect Worker Signals to the Thread slots
       self.obj.finished.connect(self.thread.quit)

       # 5 - Connect Thread started signal to Worker operational slot method
       self.thread.started.connect(self.obj.procCounter)

       # * - Thread finished signal will close the app if you want!
       #self.thread.finished.connect(app.exit)

       # 6 - Start the thread
       self.thread.start()

       # 7 - Start the form
       self.initUI()


    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.label,0,0)

        self.move(300, 150)
        self.setWindowTitle('thread test')
        self.show()

    def onIntReady(self, i):
        self.label.setText("{}".format(i))
        #print(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())
```