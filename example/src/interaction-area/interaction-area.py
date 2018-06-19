#
# This is a demo application to showcase how you can use an
# interaction area (iarea). An iarea can be used to track mouse
# interactions over an specific space.
#
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Interaction area'

def main():
	frame = np.zeros((300, 600, 3), np.uint8)

	# Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# Render a rectangle on the screen.
		rectangle = cvui.Rect(50, 50, 100, 100)
		cvui.rect(frame, rectangle.x, rectangle.y, rectangle.width, rectangle.height, 0xff0000)

		# Check what is the current status of the mouse cursor
		# regarding the previously rendered rectangle.
		status = cvui.iarea(rectangle.x, rectangle.y, rectangle.width, rectangle.height);

		# cvui::iarea() will return the current mouse status:
		#  CLICK: mouse just clicked the interaction are
		#	DOWN: mouse button was pressed on the interaction area, but not released yet.
		#	OVER: mouse cursor is over the interaction area
		#	OUT: mouse cursor is outside the interaction area
		if status == cvui.CLICK:  print('Rectangle was clicked!')
		if status == cvui.DOWN:   cvui.printf(frame, 240, 70, "Mouse is: DOWN")
		if status == cvui.OVER:   cvui.printf(frame, 240, 70, "Mouse is: OVER")
		if status == cvui.OUT:	  cvui.printf(frame, 240, 70, "Mouse is: OUT")

		# Show the coordinates of the mouse pointer on the screen
		cvui.printf(frame, 240, 50, "Mouse pointer is at (%d,%d)", cvui.mouse().x, cvui.mouse().y)

		# This function must be called *AFTER* all UI components. It does
		# all the behind the scenes magic to handle mouse clicks, etc.
		cvui.update()

		# Show everything on the screen
		cv2.imshow(WINDOW_NAME, frame)

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
    main()
