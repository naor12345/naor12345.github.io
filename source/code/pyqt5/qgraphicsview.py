# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
import os
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


class MyGraphicsView(QtWidgets.QGraphicsView):
	pass


class MainWindows(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindows, self).__init__()
		self.resize(800, 600)
		central_widget = QtWidgets.QWidget(self)
		
		vertical_layout = QtWidgets.QVBoxLayout(central_widget)
		self.graphics_view = MyGraphicsView()
		self.line_edit = QtWidgets.QLineEdit()
		self.show_pic_button = QtWidgets.QPushButton()
		vertical_layout.addWidget(self.graphics_view)
		vertical_layout.addWidget(self.line_edit)
		vertical_layout.addWidget(self.show_pic_button)
		central_widget.setLayout(vertical_layout)
		# 如果手写界面（不用qt designer），需要注意
		# 对于QMainWindow，需要造一个central_widget再调用setCentralWidget
		# 否则任何界面不会显示
		self.setCentralWidget(central_widget)
		
		# 查看图片配置
		self.graphics_scene = QtWidgets.QGraphicsScene()
		self.graphics_view.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
		self.graphics_view.setScene(self.graphics_scene)
		
		# 按钮查看
		self.show_pic_button.clicked.connect(lambda: self.show_pic(self.line_edit.text(), "not found"))

	def show_pic(self, tga_path, error_text):
		if os.path.isfile(tga_path):
			im = Image.open(tga_path)
			im2 = im.convert("RGBA")
			data = im2.tobytes("raw", "BGRA")
			qim = QtGui.QImage(data, im.width, im.height, QtGui.QImage.Format_ARGB32)
			pixmap = QtGui.QPixmap.fromImage(qim)
			pixmap_image = QtGui.QPixmap(pixmap)
			graphics_pixmap = QtWidgets.QGraphicsPixmapItem(pixmap_image)
			self.graphics_scene.clear()
			self.graphics_scene.addItem(graphics_pixmap)
			# print(graphics_pixmap.boundingRect().size())
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