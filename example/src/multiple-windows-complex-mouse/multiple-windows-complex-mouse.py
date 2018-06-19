#
# This demo shows how to use cvui in multiple windows, accessing information about
# the mouse cursor on each window.
# 
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW1_NAME = 'Window 1'
WINDOW2_NAME = 'Windows 2'
WINDOW3_NAME = 'Windows 3'

def main():
	# We have one mat for each window.
	frame1 = np.zeros((200, 500, 3), np.uint8)
	frame2 = np.zeros((200, 500, 3), np.uint8)
	frame3 = np.zeros((200, 500, 3), np.uint8)

	# Init cvui, instructing it to create 3 OpenCV windows.
	windows = [WINDOW1_NAME, WINDOW2_NAME, WINDOW3_NAME]
	cvui.init(windows, 3)

	while (True):
		# clear all frames
		frame1[:] = (49, 52, 49)
		frame2[:] = (49, 52, 49)
		frame3[:] = (49, 52, 49)

		# Inform cvui that all subsequent component calls and events are related to window 1.
		# We do that by calling cvui.context().
		cvui.context(WINDOW1_NAME)
		cvui.printf(frame1, 10, 10, 'In window1, mouse is at: %d,%d (obtained from window name)', cvui.mouse(WINDOW1_NAME).x, cvui.mouse(WINDOW1_NAME).y)
		if cvui.mouse(WINDOW1_NAME, cvui.LEFT_BUTTON, cvui.IS_DOWN):
			cvui.printf(frame1, 10, 30, 'In window1, mouse LEFT_BUTTON is DOWN')
		cvui.imshow(WINDOW1_NAME, frame1)

		# From this point on, we are going to render the second window. We need to inform cvui
		# that all updates and components from now on are connected to window 2.
		cvui.context(WINDOW2_NAME)
		cvui.printf(frame2, 10, 10, 'In window2, mouse is at: %d,%d (obtained from context)', cvui.mouse().x, cvui.mouse().y)
		if cvui.mouse(cvui.LEFT_BUTTON, cvui.IS_DOWN):
			cvui.printf(frame2, 10, 30, 'In window2, mouse LEFT_BUTTON is DOWN')
		cvui.imshow(WINDOW2_NAME, frame2)

		# Finally we are going to render the thrid window. Again we need to inform cvui
		# that all updates and components from now on are connected to window 3.
		cvui.context(WINDOW3_NAME)
		cvui.printf(frame3, 10, 10, 'In window1, mouse is at: %d,%d', cvui.mouse(WINDOW1_NAME).x, cvui.mouse(WINDOW1_NAME).y)
		cvui.printf(frame3, 10, 30, 'In window2, mouse is at: %d,%d', cvui.mouse(WINDOW2_NAME).x, cvui.mouse(WINDOW2_NAME).y)
		cvui.printf(frame3, 10, 50, 'In window3, mouse is at: %d,%d', cvui.mouse(WINDOW3_NAME).x, cvui.mouse(WINDOW3_NAME).y)
		if cvui.mouse(WINDOW1_NAME, cvui.LEFT_BUTTON, cvui.IS_DOWN):
			cvui.printf(frame3, 10, 90, 'window1: LEFT_BUTTON is DOWN')
		if cvui.mouse(WINDOW2_NAME, cvui.LEFT_BUTTON, cvui.IS_DOWN):
			cvui.printf(frame3, 10, 110, 'window2: LEFT_BUTTON is DOWN')
		if cvui.mouse(WINDOW3_NAME, cvui.LEFT_BUTTON, cvui.IS_DOWN):
			cvui.printf(frame3, 10, 130, 'window3: LEFT_BUTTON is DOWN')
		cvui.imshow(WINDOW3_NAME, frame3)

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
	main()