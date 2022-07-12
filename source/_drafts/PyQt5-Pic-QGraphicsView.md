---
title: PyQt5使用QGraphicsView显示TGA图片
date: 2022-05-17 09:29:15
categories: "PyQt5"
tags: 
    - "PyQt5"
---


## 前言
在游戏行业，常常需要将某些处理流程以一种工具化的方式确定下来，比如贴图压缩预览器。工具一般使用pyqt进行开发。但是，游戏行业常见的贴图格式是tga，这是pyqt5不支持的格式。所以需要做一些转换。
<!-- more -->
## 显示tga
环境：Python 3.7，PyQt5.
为了让pyqt读取tga文件，需要Pillow模块。核心代码如下：
```python
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

im = Image.open(tga_path)
im2 = im.convert("RGBA")
data = im2.tobytes("raw", "BGRA")
# 读取各通道信息，然后做转换
qim = QImage(data, im.width, im.height, QImage.Format_ARGB32)
# 转换成qt支持的QPixmap
pixmap = QPixmap.fromImage(qim)
pixmap_image = QPixmap(pixmap)
# 转换成QGraphicsPixmapItem
graphics_pixmap = QGraphicsPixmapItem(pixmap_image)
# 设定缩放模式，根据文档
# - FastTransformation是最简单的模式
# - SmoothTransformation会应用双线性滤波（bilinear filtering），有反锯齿的效果
graphics_pixmap.setTransformationMode(Qt.SmoothTransformation)

graphics_scene.clear()
graphics_scene.addItem(graphics_pixmap)
graphics_view.fitInView(graphics_pixmap.boundingRect(), Qt.KeepAspectRatio)
graphics_view.setViewportMargins(-2, -2, -2, -2)
graphics_view.setFrameStyle(QFrame.NoFrame)
graphics_scene.update()
```

## 滚轮缩放功能
贴图查看器常用功能：以鼠标所在位置为锚点，通过滚轮缩放。需要继承`QGraphicsView`类，实现以下函数。
```python
class MyGraphicsView(QtWidgets.QGraphicsView):
    def wheelEvent(self, event):
        '''
        以鼠标所在位置为锚点，通过滚轮缩放
        '''
        anchor = self.transformationAnchor()
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        angle = event.angleDelta().y()
        if angle > 0:
            factor = 1.1
        else:
            factor = 0.9
        self.scale(factor, factor)
        self.setTransformationAnchor(anchor)
```

如果用qt designer，右击QGraphicsView，选择`提升为...`。
![](promoted.png)
然后选择基类`QGraphicsView`，提升的类名和头文件。对于pyqt，头文件对应规则是`from <头文件路径（斜杠替换为点）> import <类名>`，比如图里的类相当于`from views.my_widgets import MyGraphicsView`。
![](promoted_class.png)

## TransformationMode
QGraphicsPixmapItem可通过setTransformationMode设定缩放模式，主要区别是图像放大后是否开启反锯齿，根据应用场景设定。

![](anti-aliasing.png)
<center>SmoothTransformation，反锯齿效果</center>

![](no-anti-aliasing.png)
<center>FastTransformation，未开启反锯齿。可看清每个像素的实际颜色</center>


## 完整代码
```python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
import os
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class MyGraphicsView(QtWidgets.QGraphicsView):
    def wheelEvent(self, event):
        '''
        以鼠标所在位置为锚点，通过滚轮缩放
        '''
        anchor = self.transformationAnchor()
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        angle = event.angleDelta().y()
        if angle > 0:
            factor = 1.1
        else:
            factor = 0.9
        self.scale(factor, factor)
        self.setTransformationAnchor(anchor)


class MainWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.resize(800, 600)
        central_widget = QtWidgets.QWidget(self)
        vertical_layout = QtWidgets.QVBoxLayout(central_widget)
        self.graphics_view = MyGraphicsView()
        vertical_layout.addWidget(self.graphics_view)
        central_widget.setLayout(vertical_layout)
        self.setCentralWidget(central_widget)
        
        # 查看图片配置
        self.graphics_scene = QtWidgets.QGraphicsScene()
        self.graphics_view.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.graphics_view.setScene(self.graphics_scene)
        # 显示图片
        self.show_pic(r'F:\source.tga', "not found")

    def show_pic(self, tga_path, error_text):
        if os.path.isfile(tga_path):
            im = Image.open(tga_path)
            im2 = im.convert("RGBA")
            data = im2.tobytes("raw", "BGRA")
            qim = QtGui.QImage(data, im.width, im.height, QtGui.QImage.Format_ARGB32)
            pixmap = QtGui.QPixmap.fromImage(qim)
            pixmap_image = QtGui.QPixmap(pixmap)
            graphics_pixmap = QtWidgets.QGraphicsPixmapItem(pixmap_image)
            
            # 反锯齿
            # graphics_pixmap.setTransformationMode(Qt.SmoothTransformation)
            
            self.graphics_scene.clear()
            self.graphics_scene.addItem(graphics_pixmap)
            self.graphics_view.fitInView(graphics_pixmap.boundingRect(), Qt.KeepAspectRatio)
            self.graphics_view.setViewportMargins(-2, -2, -2, -2)
            self.graphics_view.setFrameStyle(QtWidgets.QFrame.NoFrame)
            self.graphics_scene.update()
        else:
            text = QtWidgets.QGraphicsTextItem()
            text.setPlainText(error_text)
            self.graphics_scene.clear()
            self.graphics_scene.addItem(text)
            self.graphics_view.fitInView(self.graphics_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            self.graphics_scene.update()


if __name__ == '__main__':
    class App(QtWidgets.QApplication):
        def __init__(self, sys_argv):
            super(App, self).__init__(sys_argv)
            self.view = MainWindows()
            self.view.show()

    app = App(sys.argv)
    sys.exit(app.exec_())
```