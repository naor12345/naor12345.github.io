---
title: PyQt5构建基础界面
date: 2022-05-17 09:29:15
categories: "PyQt5"
tags: 
    - "PyQt5"
---


**pyqt适合搞各种小工具，快速高效。**

正规做法，需要配置pycharm、qt designer、pyuic的环境。qt designer生成ui文件，通过pyuic转换成py文件。对于界面简单的小工具，可以直接coding界面。

Qt的主窗体继承自`QtWidgets.QMainWindow`类。该类需要设定一个central_widget（`self.setCentralWidget(central_widget)`），各layout和widget需要放到该central_widget里面。

代码如下：

```python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets


class MainWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.resize(800, 600)
        '''
        如果手写界面（不用qt designer），需要注意
        对于QMainWindow，需要造一个central_widget再调用setCentralWidget
        否则任何界面不会显示
        '''
        # 创建central_widget
        central_widget = QtWidgets.QWidget(self)
        # 创建layout，将各种widget添加到layout里
        vertical_layout = QtWidgets.QVBoxLayout(central_widget)
        line_edit = QtWidgets.QLineEdit()
        push_button = QtWidgets.QPushButton()
        vertical_layout.addWidget(line_edit)
        vertical_layout.addWidget(push_button)
        # 将layout添加到central_widget
        central_widget.setLayout(vertical_layout)
        # mainwindows设置central_widget
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    class App(QtWidgets.QApplication):
        def __init__(self, sys_argv):
            super(App, self).__init__(sys_argv)
            self.view = MainWindows()
            self.view.show()

    app = App(sys.argv)
    sys.exit(app.exec_())

```