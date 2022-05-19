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
		self.show_pic(r'F:\H74\Trunk\Program\ClientWrapper\Client\Package\Repository\char_gh.local\Texture\03\{0337d571-592d-433b-b998-359675092870}\source.tga', "not found")

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
			graphics_pixmap.setTransformationMode(Qt.SmoothTransformation)
			
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