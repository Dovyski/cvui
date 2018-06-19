#
# This demo shows how to use cvui in multiple windows, using rows and colums.
# Additionally a custom error window (an OpenCV window) is dynamically opened/closed
# based on UI buttons.
# 
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui
import random

GUI_WINDOW1_NAME = 'Window 1'
GUI_WINDOW2_NAME = 'Windows 2'
ERROR_WINDOW_NAME = 'Error window'

# Check if an OpenCV window is open.
# From: https:#stackoverflow.com/a/48055987/29827
def isWindowOpen(name):
	return cv2.getWindowProperty(name, cv2.WND_PROP_AUTOSIZE) != -1

# Open a new OpenCV window and watch it using cvui
def openWindow(name):
	cv2.namedWindow(name)
	cvui.watch(name)

# Open an OpenCV window
def closeWindow(name):
	cv2.destroyWindow(name)

	# Ensure OpenCV window event queue is processed, otherwise the window
	# will not be closed.
	cv2.waitKey(1)

def main():
	# We have one mat for each window.
	frame1 = np.zeros((150, 600, 3), np.uint8)
	frame2 = np.zeros((150, 600, 3), np.uint8)
	error_frame = np.zeros((100, 300, 3), np.uint8)

	# Flag to control if we should show an error window.
	error = False

	# Create two OpenCV windows
	cv2.namedWindow(GUI_WINDOW1_NAME)
	cv2.namedWindow(GUI_WINDOW2_NAME)
	
	# Init cvui and inform it to use the first window as the default one.
	# cvui.init() will automatically watch the informed window.
	cvui.init(GUI_WINDOW1_NAME)

	# Tell cvui to keep track of mouse events in window2 as well.
	cvui.watch(GUI_WINDOW2_NAME)

	while (True):
		# Inform cvui that all subsequent component calls and events are related to window 1.
		cvui.context(GUI_WINDOW1_NAME)

		# Fill the frame with a nice color
		frame1[:] = (49, 52, 49)

		cvui.beginColumn(frame1, 50, 20, -1, -1, 10)
		cvui.text('[Win1] Use the buttons below to control the error window')
			
		if cvui.button('Close'):
			closeWindow(ERROR_WINDOW_NAME)

		# If the button is clicked, we open the error window.
		# The content and rendering of such error window will be performed
		# after we handled all other windows.
		if cvui.button('Open'):
			error = True
			openWindow(ERROR_WINDOW_NAME)
		cvui.endColumn()

		# Update all components of window1, e.g. mouse clicks, and show it.
		cvui.update(GUI_WINDOW1_NAME)
		cv2.imshow(GUI_WINDOW1_NAME, frame1)

		# From this point on, we are going to render the second window. We need to inform cvui
		# that all updates and components from now on are connected to window 2.
		# We do that by calling cvui.context().
		cvui.context(GUI_WINDOW2_NAME)
		frame2[:] = (49, 52, 49)
		
		cvui.beginColumn(frame2, 50, 20, -1, -1, 10)
		cvui.text('[Win2] Use the buttons below to control the error window')

		if cvui.button('Close'):
			closeWindow(ERROR_WINDOW_NAME)

		# If the button is clicked, we open the error window.
		# The content and rendering of such error window will be performed
		# after we handled all other windows.
		if cvui.button('Open'):
			openWindow(ERROR_WINDOW_NAME)
			error = True
		cvui.endColumn()

		# Update all components of window2, e.g. mouse clicks, and show it.
		cvui.update(GUI_WINDOW2_NAME)
		cv2.imshow(GUI_WINDOW2_NAME, frame2)

		# Handle the content and rendering of the error window,
		# if we have un active error and the window is actually open.
		if error and isWindowOpen(ERROR_WINDOW_NAME):
			# Inform cvui that all subsequent component calls and events are
			# related to the error window from now on
			cvui.context(ERROR_WINDOW_NAME)

			# Fill the error window if a vibrant color
			error_frame[:] = (10, 10, 49)

			cvui.text(error_frame, 70, 20, 'This is an error message', 0.4, 0xff0000)

			if cvui.button(error_frame, 110, 40, 'Close'):
				error = False

			if error:
				# We still have an active error.
				# Update all components of the error window, e.g. mouse clicks, and show it.
				cvui.update(ERROR_WINDOW_NAME)
				cv2.imshow(ERROR_WINDOW_NAME, error_frame)
			else:
				# No more active error. Let's close the error window.
				closeWindow(ERROR_WINDOW_NAME)

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
	main()