---
title: PyQt5使用QGraphicsView显示TGA图片
date: 2022-05-17 09:29:15
description: PyQt5用例总结
categories: "PyQt5"
tags: 
    - "PyQt5"
---


# pycharm构建pyuic和qt designer环境
# 用这两个构建（类的提升）


## 序
在游戏行业，常常需要将某些处理流程以一种工具化的方式确定下来，比如贴图压缩预览器。工具一般使用pyqt进行开发。但是，游戏行业常见的贴图格式是tga，这是pyqt5不支持的。所以需要做一些转换。

## 破
环境：Python 3.7，PyQt5.
为了让pyqt读取tga文件，需要Pillow模块。
```python
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

im = Image.open(tga_path)
im2 = im.convert("RGBA")
data = im2.tobytes("raw", "BGRA")
qim = QImage(data, im.width, im.height, QImage.Format_ARGB32)  # 这里需要做一波转换
pixmap = QPixmap.fromImage(qim)
pixmap_image = QPixmap(pixmap)
graphics_pixmap = QGraphicsPixmapItem(pixmap_image)
target_view = target_scene.views()[0]  # QGraphicsView
target_scene.clear()
target_scene.addItem(graphics_pixmap)
target_view.fitInView(graphics_pixmap.boundingRect(), Qt.KeepAspectRatio)
target_view.setViewportMargins(-2, -2, -2, -2)
target_view.setFrameStyle(QFrame.NoFrame)
target_scene.update()
```
