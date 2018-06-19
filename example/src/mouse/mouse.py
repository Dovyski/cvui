#
# This is application shows the mouse API of cvui. It shows a rectangle on the
# screen everytime the user clicks and drags the mouse cursor around.
#
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Mouse'

def main():
	frame = np.zeros((300, 600, 3), np.uint8)

	# Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME);

	# Rectangle to be rendered according to mouse interactions.
	rectangle = cvui.Rect(0, 0, 0, 0)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# Show the coordinates of the mouse pointer on the screen
		cvui.text(frame, 10, 30, 'Click (any) mouse button and drag the pointer around to select an area.')
		cvui.printf(frame, 10, 50, 'Mouse pointer is at (%d,%d)', cvui.mouse().x, cvui.mouse().y)

		# The function "bool cvui.mouse(int query)" allows you to query the mouse for events.
		# E.g. cvui.mouse(cvui.DOWN)
		#
		# Available queries:
		#	- cvui.DOWN: any mouse button was pressed. cvui.mouse() returns true for a single frame only.
		#	- cvui.UP: any mouse button was released. cvui.mouse() returns true for a single frame only.
		#	- cvui.CLICK: any mouse button was clicked (went down then up, no matter the amount of frames in between). cvui.mouse() returns true for a single frame only.
		#	- cvui.IS_DOWN: any mouse button is currently pressed. cvui.mouse() returns true for as long as the button is down/pressed.

		# Did any mouse button go down?
		if cvui.mouse(cvui.DOWN):
			# Position the rectangle at the mouse pointer.
			rectangle.x = cvui.mouse().x
			rectangle.y = cvui.mouse().y

		# Is any mouse button down (pressed)?
		if cvui.mouse(cvui.IS_DOWN):
			# Adjust rectangle dimensions according to mouse pointer
			rectangle.width = cvui.mouse().x - rectangle.x
			rectangle.height = cvui.mouse().y - rectangle.y

			# Show the rectangle coordinates and size
			cvui.printf(frame, rectangle.x + 5, rectangle.y + 5, 0.3, 0xff0000, '(%d,%d)', rectangle.x, rectangle.y)
			cvui.printf(frame, cvui.mouse().x + 5, cvui.mouse().y + 5, 0.3, 0xff0000, 'w:%d, h:%d', rectangle.width, rectangle.height)

		# Did any mouse button go up?
		if cvui.mouse(cvui.UP):
			# Hide the rectangle
			rectangle.x = 0
			rectangle.y = 0
			rectangle.width = 0
			rectangle.height = 0

		# Was the mouse clicked (any button went down then up)?
		if cvui.mouse(cvui.CLICK):
			cvui.text(frame, 10, 70, 'Mouse was clicked!')

		# Render the rectangle
		cvui.rect(frame, rectangle.x, rectangle.y, rectangle.width, rectangle.height, 0xff0000)

		# This function must be called *AFTER* all UI components. It does
		# all the behind the scenes magic to handle mouse clicks, etc, then
		# shows the frame in a window like cv2.imshow() does.
		cvui.imshow(WINDOW_NAME, frame)

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
	main()