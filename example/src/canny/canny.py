#
# This demo showcases some components of cvui being used to control
# the application of the Canny edge algorithm to a loaded image.
#
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'CVUI Canny Edge'

def main():
	lena = cv2.imread('lena.jpg', cv2.IMREAD_COLOR)
	frame = np.zeros(lena.shape, np.uint8)
	low_threshold = [50]
	high_threshold = [150]
	use_canny = [False]

	# Init cvui and tell it to create a OpenCV window, i.e. cv2.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Should we apply Canny edge?
		if use_canny[0]:
			# Yes, we should apply it.
			frame = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)
			frame = cv2.Canny(frame, low_threshold[0], high_threshold[0], 3)
			frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
		else: 
			# No, so just copy the original image to the displaying frame.
			frame[:] = lena[:]

		# Render the settings window to house the checkbox
		# and the trackbars below.
		cvui.window(frame, 10, 50, 180, 180, 'Settings')
		
		# Checkbox to enable/disable the use of Canny edge
		cvui.checkbox(frame, 15, 80, 'Use Canny Edge', use_canny)
		
		# Two trackbars to control the low and high threshold values
		# for the Canny edge algorithm.
		cvui.trackbar(frame, 15, 110, 165, low_threshold, 5, 150)
		cvui.trackbar(frame, 15, 180, 165, high_threshold, 80, 300)

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
