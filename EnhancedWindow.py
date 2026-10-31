# 
# This class enhances the window component of cvui by making it movable and minimizable.
# 
# Authors:
# 	ShengYu - https://github.com/shengyu7697
# 	Amaury Breheret - https://github.com/abreheret
# 
# Contributions:
# 	Fernando Bevilacqua <dovyski@gmail.com>
# 
# Copyright (c) 2018 Authors and Contributors
# Code licensed under the MIT license.
# 

import cvui

class EnhancedWindow:
	def __init__(self, x, y, width, height, title, minimizable = True):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__heightNotMinimized = height
		self.__title = title
		self.__deltaY = 0
		self.__deltaX = 0
		self.__isMoving = False
		self.__minimized = False;
		self.__minimizable = minimizable

	def begin(self, frame):
		mouseInsideTitleArea = cvui.mouse().inside(cvui.Rect(self.__x, self.__y, self.__width, 20))
		self.__height = 20 if self.__minimized else self.__heightNotMinimized

		if self.__isMoving == False and cvui.mouse(cvui.DOWN) and mouseInsideTitleArea:
			self.__deltaX = cvui.mouse().x - self.__x
			self.__deltaY = cvui.mouse().y - self.__y
			self.__isMoving = True

		elif self.__isMoving and cvui.mouse(cvui.IS_DOWN):
			self.__x = cvui.mouse().x - self.__deltaX
			self.__y = cvui.mouse().y - self.__deltaY

		else:
			frameRows,frameCols,frameChannels = frame.shape
			self.__isMoving = False
			self.__x = max(0, self.__x)
			self.__y = max(0, self.__y)
			self.__x = min(frameCols - self.__width, self.__x)
			self.__y = min(frameRows - 20, self.__y)

		cvui.window(frame, self.__x, self.__y, self.__width, self.__height, self.__title)

		if self.__minimizable and cvui.button(frame, self.__x + self.__width - 20, self.__y + 1, 18, 18, '+' if self.__minimized else '-'):
			self.__minimized = not self.__minimized

		cvui.beginRow(frame, self.__x + 10, self.__y + 30, self.__width - 20, self.__height - 20)
		cvui.beginColumn(self.__width - 10, self.__height - 20)


	def end(self):
		cvui.endColumn()
		cvui.endRow()

	def width(self):
		return self.__width

	def height(self):
		return self.__height

	def setWidth(self, w):
		self.__width = w

	def setHeight(self, h):
		self.__height = h
		self.__heightNotMinimized = h

	def isMinimized(self):
		return self.__minimized
